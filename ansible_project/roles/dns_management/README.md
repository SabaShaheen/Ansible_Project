# DNS Record Management Role

## Description
This role manages DNS records by checking for the existence of a DNS record and creating it if it does not exist.

## Requirements


Python3.x should be installed and python virtual environment should be configured
 

## Role Variables
- `api_url`: The URL to the DNS management API.
- `api_key`: API key for authentication.
- `record_name`: The name of the DNS record.
- `record_value`: The value for the DNS record.

## Dependencies
requests library should be installed on the machine where this playbook will execute
pip install requests

ansible.module_utils.basic 

Custom module : dns_record_manager


## Example Playbook
```yaml
- hosts: localhost
  gather_facts: no
  roles:
    - dns_management

