# Jenkins Pipeline Setup 

## Step 1: Prepare Jenkins Environment

### Install Jenkins

- Install Jenkins on a server. Download it from [jenkins.io](https://jenkins.io).

### Install Necessary Plugins

- **Git plugin**: This is usually installed by default, but make sure it's there because it allows Jenkins to interact with Git repositories.
- **Ansible plugin**: Install this plugin to enable Jenkins to run Ansible playbooks. These plugins can be installed from **Manage Jenkins > Manage Plugins > Available tab**.

### Configure System

- Go to **Manage Jenkins > Configure System**.
- Under **Global Tool Configuration**, add configurations for Git and Ansible. For Ansible, specify the path to the Ansible executable.

### Set Up Credentials

- Go to **Manage Jenkins > Manage Credentials**.
- Add Git credentials (username and password or SSH key) that will be used to access the repository.

## Step 2: Create the Jenkins Pipeline

### Create New Item

- In Jenkins, go to the dashboard and click on **New Item**.
- Provide name for the pipeline (e.g., "Ansible Deployment") and select **Pipeline** then click **OK**.

### Configure the Pipeline

- In the pipeline configuration page, scroll down to the **Pipeline** section.
- We can either write the pipeline script directly in the Jenkins web interface or pull it from your SCM (Source Code Management) like Git.
- Choose **Pipeline script** to write it directly or **Pipeline script from SCM** to pull it.

## Step 3: Write the Jenkins Pipeline Script

Below is pipeline script that demonstrates how to clone a Git repository and run an Ansible playbook:





pipeline {
	node{
	label agent_label
	}
    }
	
	options { 
		disableConcurrentBuilds()
	}



    // Define parameters for dynamic runtime inputs
    parameters {
        
        choice(name: 'ACTION', choices: ['ec2_provision', 'mysql_install', 'dns_management', 'python_venv_setup'], description: 'Action to perform')
    }
	
	parameters {
	
       choice(
	   name: 'target_server',
	   choices: ['dev','sit','uat','prod'],
	   description: 'Environment to deploy to'
    }

    stages {
        stage('Initialization') {
            steps {
                echo "Pipeline execution started for ${params.DEPLOY_ENV} environment"
            }
        }

        stage('Checkout') {
            steps {
                // Checkout the Git repository
                git credentialsId: 'git-credentials-id', url: 'https://your-git-repository-url.git'
            }
        }


        stage('Execute Ansible Playbook') {
		
		agent { label params.target_server == prod ? 'prod_agent' : 'non-prod_agent'
		}
            steps {
                sh '''
				chmod 750 ./pipelines/jenkins_RunAnsibleScripts.ksh
				./pipelines/jenkins_RunAnsibleScripts.ksh /ansible_project/site.yml /ansible_project/environments/"${target_server}"/inventory/hosts target_env=\'${target_server}\'
            }
        }

        //  add parallel testing or other stages here
        stage('Parallel Stage') {
            parallel {
                stage('Test 1') {
                    steps {
                        echo "Running first test set"
                    }
                }
                stage('Test 2') {
                    steps {
                        echo "Running second test set"
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
        }
        failure {
            slackSend (color: '#FF0000', message: "FAILED: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
        }
        always {
            cleanWs()
            echo "Cleanup workspace after the build"
        }
    }
}









# Alternate Script:


pipeline {
    agent any

    tools {
        
        ansible 'Ansible'
    }



    // Define parameters for dynamic runtime inputs
    parameters {
        string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Deployment environment')
        choice(name: 'ACTION', choices: ['ec2_provision', 'mysql_install', 'dns_management', 'python_venv_setup'], description: 'Action to perform')
    }

    stages {
        stage('Initialization') {
            steps {
                echo "Pipeline execution started for ${params.DEPLOY_ENV} environment"
            }
        }

        stage('Checkout') {
            steps {
                // Checkout the Git repository
                git credentialsId: 'git-credentials-id', url: 'https://your-git-repository-url.git'
            }
        }

        stage('Select Environment') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        env.DEPLOY_ENV = 'production'
                    } else {
                        env.DEPLOY_ENV = 'staging'
                    }
                    echo "Environment set to ${env.DEPLOY_ENV}"
                }
            }
        }

        stage('Execute Ansible Playbook') {
            steps {
                script {
                    def playbookPath = ''
                    if (params.ACTION == 'ec2_provision') {
                        playbookPath = 'ec2_provision.yml'
                    } else if (params.ACTION == 'mysql_install') {
                        playbookPath = 'playbooks/mysql_install.yml'
                    } else if (params.ACTION == 'dns_management') {
                        playbookPath = 'playbooks/dns_management.yml'
                    } else if (params.ACTION == 'python_venv_setup') {
                        playbookPath = 'playbooks/python_venv_setup.yml'
                    }
                    
                    if (playbookPath) {
                        ansiblePlaybook(
                            playbook: "/ansible_project/playbooks/${playbookPath}",
                            inventory: "/ansible_project/inventory/${env.DEPLOY_ENV}/hosts",
                            credentialsId: 'ansible-vault-credential-id',
                            extras: "-e @path/to/extra-vars.yml -e env=${env.DEPLOY_ENV}" // Add extra vars if necessary
                        )
                    } else {
                        echo "No playbook selected or invalid action provided."
                    }
                }
            }
        }

        // Optionally, add parallel testing or other stages here
        stage('Parallel Stage') {
            parallel {
                stage('Test 1') {
                    steps {
                        echo "Running first test set"
                    }
                }
                stage('Test 2') {
                    steps {
                        echo "Running second test set"
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
        }
        failure {
            slackSend (color: '#FF0000', message: "FAILED: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
        }
        always {
            cleanWs()
            echo "Cleanup workspace after the build"
        }
    }
}
