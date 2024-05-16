# MySQL Installation Playbook

This playbook provides a comprehensive approach to installing and configuring MySQL on a Linux RHEL server using Ansible.


Requirements
------------

AN EC2 RHEL machine 


Role Variables
--------------

## General Variables

- **`download_folder`**
  - Description: The directory where MySQL RPM packages will be downloaded.
  - Example: `/opt/mysql_downloads`

- **`mysql_repo_url`**
  - Description: The base URL for the MySQL repository where the RPM package can be downloaded.
  - Example: `https://repo.mysql.com`

- **`mysql_rmp`**
  - Description: The specific RPM file to download for MySQL installation.
  - Example: `mysql-community-server-minimal-8.0.22-1.el8.x86_64.rpm`

- **`mysql_root_password`**
  - Description: The desired password for the MySQL root user.
  - Example: `secure_password`

## Download and Installation Variables

- **`download_result`**
  - Description: Variable used to register the outcome of the MySQL download task. This variable is then used to conditionally perform other tasks based on the success or failure of the download.
  - Example: `register: download_result`

## Configuration and Service Management

- **`mysql_rmp`**
  - Description: Name of the MySQL RPM file stored locally after being downloaded, used during installation.
  - Example: `/path/to/downloaded/mysql.rpm`

- **`login_unix_socket`**
  - Description: Specifies the Unix socket file used for MySQL service. This can be used for tasks that require logging in to the MySQL service.
  - Example: `/var/lib/mysql/mysql.sock`

- **`my.cnf.j2`**
  - Description: The Jinja2 template file for MySQL configuration. This file is used to generate the `/etc/my.cnf` configuration file for MySQL.
  - Example: `templates/my.cnf.j2`

## Initial Setup Variables

- **`initial_setup.sql`**
  - Description: SQL script for initial configuration and setup of MySQL databases and settings.
  - Example: `/tmp/initial_setup.sql`

## Error Handling and Debugging

- **`epel_install`**
  - Description: Variable used to register the outcome of the EPEL repository installation, to check if manual configuration is needed.
  - Example: `register: epel_install`

## Handlers

- **`restart mysql`**
  - Description: Handler used to restart MySQL service when configuration changes are made that require a restart.

These variables should be customized based on your server configuration and operational needs.

Dependencies
------------

This role uses the below dependencies:
openssl-libs
ansible.builtin.rpm_key
epel-release
python3
python3-pip
pymysql




Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: ec2
  roles:
    - mysql_install

## Initial Setup Tasks

1. **Clean Yum Cache**
    - Cleans the yum cache to ensure the latest packages are available.
    - `update_cache: yes`

2. **Install Necessary OpenSSL Libraries**
    - Installs required OpenSSL libraries for secure operations.
    - Packages: `openssl-libs`

3. **Import MySQL GPG Key**
    - Ensures that the MySQL GPG key is present for verifying package integrity.

4. **Attempt to Install EPEL Release**
    - Tries to install the EPEL repository from default repositories.

5. **Manually Configure the EPEL Repository if Needed**
    - Sets up the EPEL repository manually if the default installation fails.

6. **Install Python 3 and pip**
    - Installs Python3 and pip which are required for running Python scripts.

7. **Install PyMySQL**
    - Installs PyMySQL, a Python MySQL client library, needed for MySQL management via Python.

## MySQL Installation and Configuration

1. **Prepare Install Folder**
    - Creates and navigates to the installation folder.

2. **Download MySQL**
    - Downloads the MySQL RPM package from the specified repository.

3. **Rescue Block**
    - Captures any errors during the download and provides a debug message.

4. **Install MySQL Repository from Local File**
    - Installs MySQL using the locally downloaded RPM file if the download was successful.

5. **Configure MySQL**
    - Configures MySQL using a templated configuration file.

6. **Flush Handlers**
    - Ensures that MySQL is restarted before continuing if any changes that require a restart were made.

7. **Start and Enable MySQL Service**
    - Starts and enables the MySQL service to ensure it's running and set to start on boot.

8. **Set MySQL Root Password**
    - Configures the MySQL root password as specified.

9. **Run Initial MySQL Setup Script**
    - Executes a SQL script for initial setup tasks.

## Handlers

- **Restart MySQL**
    - Restarts MySQL service whenever necessary to apply configuration changes.

## Tags

- `initial_setup`
- `download_mysql`
- `install_mysql`
- `mysql_configuration`
- `mysql_service`
- `configuration`
- `mysql_init`

The playbook allows you to selectively run parts of the configuration based on these tags. Ensure you have the necessary variables and files defined in your playbook or inventory for successful execution.


License
---------------

BSD

Author Information
------------------
Saba Shaheen
An optional section for the role authors to include contact information, or a website (HTML is not allowed).
