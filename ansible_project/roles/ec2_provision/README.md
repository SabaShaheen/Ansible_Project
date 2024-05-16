# Provision EC2
=========

This ansible script demonstrates a comprehensive approach to managing EC2 instances with Ansible, including creation, configuration, and dynamic inventory management, which are critical for scalable cloud operations.

## Requirements

Security and Credentials: The playbook expects AWS credentials (`aws_access_key`, `aws_secret_key`) to be securely provided via Ansible Vault, to interact with AWS resources securely.

### Install the required local software

The software required on the machine where this playbook will execute includes:

- Python
- Pip
- boto
- boto3
- ansible

```bash
sudo apt install python         # Install Python
sudo apt install python-pip     # Install pip
pip install boto boto3 ansible  # Install boto, boto3, and ansible

The versions of python and pip can be verified (python 3.9+ is preferable),

python --version  # Check python version
pip --version     # Check pip version

## Generate SSH keys

Generate SSH keys (to SSH into provisioned EC2 instances) with below command:

### 1. This creates a public (.pub) and private key in the ~/.ssh/ directory
ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_aws
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):  # Can be left blank

### 2. Ensure private key is not publicly viewable
chmod 400 ~/.ssh/my_aws

## Setup Ansible Vault 

### Method 1: Manually enter password
Create an Ansible vault called pass.yml in the group_vars/all/ directory with the following command,

#### 1. Create an ansible vault
ansible-vault create group_vars/all/pass.yml

#### 2. There's a prompt for a password, it's needed for playbook execution/edit
New Vault password:
Confirm New Vault password:
With this method, prompt will display for a password every time playbooks are executed or pass.yml is edited.

### Method 2: Automate password access


#### 1. Create a hashed password file vault.pass in the root directory
openssl rand -base64 2048 > vault.pass

# 2. Create an ansible vault. 'vault.pass' is referenced with '--vault-password-file' option
ansible-vault create group_vars/all/pass.yml --vault-password-file vault.pass
With this method, --vault-password-file must now always be used when running the playbook or editing pass.yml, for example,

# Editing 'pass.yaml'
ansible-vault edit group_vars/all/pass.yml --vault-password-file vault.pass

Add AWS Access/Secret to Ansible Vault
Edit pass.yml to include  AWS access key and secret access key,

ansible-vault edit group_vars/all/pass.yml --vault-password-file vault.pass

# 2. This opens up the 'vim' editor, press 'i' or 'a' to edit, then 'esc' ':wq' to save and exit
# Add this text in using your own access and secret key
ec2_access_key: AAAAAAAAAAAAAABBBBBBBBBBBB                                      
ec2_secret_key: afjdfadgf$fgajk5ragesfjgjsfdbtirhf

Role Variables
--------------

# Variables for EC2 Provisioning Role

This document outlines all variables used in the `ec2_provision` role. These variables are crucial for the setup and management of AWS EC2 instances.

## General Variables

- **region**: AWS region where the resources will be created. Example: `us-east-1`.
- **ec2_access_key**: AWS access key, recommended to be stored securely in Ansible Vault.
- **ec2_secret_key**: AWS secret key, recommended to be stored securely in Ansible Vault.

## Security Group and Key Pair Variables

- **sec_group**: The name of the security group to be used or created for the EC2 instances.
- **security_group_rules**: Rules that define the allowed traffic for the security group, specified in a list format.
- **key_name**: Name of the SSH key pair to be used or created for the EC2 instance.
- **ssh_public_key**: Path to the public SSH key file used to create the key pair.

## Instance Configuration Variables

- **instance_type**: Type of the EC2 instance (e.g., `t2.micro`).
- **image**: ID of the AMI used to launch the instance.
- **old_key_name**: (For updates) The name of the old key pair to be removed.
  
## Output and Configuration Files

- **debug_info_conf**: Destination path for debug information configuration file generated from a template.
- **security_group_conf**: Destination path for security group configuration file generated from a template.

## Operational Tags

- **tags**: Used to categorize tasks within Ansible playbooks, such as `create_ec2` and `update_ec2`, which can be used to selectively run certain parts of your infrastructure code.

## Notifications and Handlers

- **notify**: Used in tasks to trigger handler activities like `cleanup key pairs` and `revoke sec group rules` upon task completion. Handlers should be defined in the `handlers` directory of the role.

## Instance Connectivity and Setup

- **wait_for**: Configuration parameters for the `wait_for` module to ensure the instance is ready before proceeding with further configurations.

## Debugging and Instance Information

- **result**: Variable used to register and store information about EC2 instances, such as their IDs, states, and public DNS names, which can be critical for dynamic inventory and operational monitoring.



# Dependencies
------------

The main ansible modules used are:

amazon.aws.ec2_instance
amazon.aws.ec2_security_group
amazon.aws.ec2_key


# Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         -  role: ec2_provision 



# Task Breakdown

## 1. Provision EC2 Instance Block
This block handles the initial setup and provisioning of an EC2 instance:

- **Create Security Group**: This task uses the `amazon.aws.ec2_security_group` module to create a security group with specified rules, which define the allowed inbound traffic for the instances.

- **Create Key Pair**: The `amazon.aws.ec2_key` module creates an SSH key pair needed to securely access the EC2 instances. The key material (public key) is provided from a specified file.

- **Start an Instance with a Public IP Address**: The `amazon.aws.ec2_instance` module launches an EC2 instance with the previously created key pair and security group. It also assigns a public IP address to the instance and sets an environment tag.

- **Debug EC2 Instance Information**: Uses the debug module to print the details of the launched instance(s).

- **Generate Debug Information Configuration from Template**: This task generates a file from a Jinja2 template (`debug_info.yml.j2`) and saves it to a defined destination. It's typically used for creating configuration files dynamically based on the instance's state.

- **Create Security Group Configuration from Template**: Similar to the previous template task, but for security group configuration.

- **Add New Instance to Host Group**: This task dynamically adds the new instance to the Ansible in-memory inventory under the group `ec2`, making it easier to target this group in subsequent playbook runs.

- **Wait for Instance to be Ready**: Uses the `wait_for` module to pause the playbook until the SSH service on the new instance is reachable, ensuring the instance is fully started and ready for connections.

## 2. Update EC2 Instance Block
This block is tagged to never run by default (`tags: ['never', 'update_ec2']`) and includes tasks that might be used for updating or modifying instances:

- **Remove Old Key Pair**: This task deletes an old key pair using the `amazon.aws.ec2_key` module, potentially as part of a key rotation strategy.

- **Modify Security Group Rules**: Updates or reaffirms the security group rules using the same `amazon.aws.ec2_security_group` module, which can be useful for dynamically changing firewall rules.

## 3. Facts Block
This block is always executed (`tags: always`) and gathers detailed facts about the instances:

- **Get Instances Facts**: Fetches detailed information about all instances using the `ec2_instance_info` module, which can be used for audit, compliance, or other operational tasks.

- **Instances ID Debug**: Outputs the instance IDs, their state, and public DNS names using the debug module, helping in tracking and managing instances post-provisioning.

## Additional Notes
- **Tags**: The script uses tags to control the execution of specific blocks (`create_ec2`, `update_ec2`, `always`). This allows selective running of parts of the playbook based on the tags specified during the command line invocation.

- **Handlers**: Some tasks include `notify` to trigger handlers (cleanup key pairs, revoke sec group rules). Handlers are special tasks in Ansible that run at the end of a play if notified by another task, commonly used for restarting services or any action that needs to be taken after a configuration change.


License
-------

BSD

Author Information
------------------

Explanation of the Test Tasks
Check if Security Group Exists: This task uses ec2_group_info to fetch information about the specified security group and then asserts its existence.
Check if EC2 Instance is Running: This task checks if there is at least one running instance with the specified environment tag.
Attempt SSH Connection: This uses wait_for to check if SSH to the instance is possible within the timeout period.
Running Tests
You can run these tests by including them in your CI/CD pipeline or manually executing them after deploying your resources to verify the setup. To execute the tests, run:

ansible-playbook ec2_provision/tests/main.yml -i your_inventory_file
Make sure to provide the correct inventory and variable files that supply necessary credentials and configuration details.

These tests help ensure that your Ansible role for provisioning EC2 instances functions correctly and adheres to your infrastructure specifications. Adjust the specific details of the tests to match your environment and requirements.
