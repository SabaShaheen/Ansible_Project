#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests

def check_dns_record(api_url, headers, record_name, module):
    """ Check if the DNS record exists, handling potential errors. """
    try:
        response = requests.get(f"{api_url}/dns_records/{record_name}", headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()  # Assuming the API returns JSON
    except requests.exceptions.HTTPError as e:
        module.fail_json(msg="API returned an error: " + str(e))
    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Failed to connect to API: " + str(e))
    return None

def create_dns_record(api_url, headers, record_name, record_value, module):
    """ Create a DNS record, handling potential errors. """
    payload = {
        'name': record_name,
        'value': record_value
    }
    try:
        response = requests.post(f"{api_url}/dns_records", headers=headers, json=payload)
        response.raise_for_status()
        if response.status_code == 201:
            return response.json()
    except requests.exceptions.HTTPError as e:
        module.fail_json(msg="Failed to create DNS record: " + response.text)
    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Failed to connect to API: " + str(e))
    return None

def main():
    module_args = dict(
        api_url=dict(type='str', required=True),
        api_key=dict(type='str', required=True, no_log=True),
        record_name=dict(type='str', required=True),
        record_value=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    headers = {
        "Authorization": "Bearer " + module.params['api_key'],
        "Content-Type": "application/json"
    }

    existing_record = check_dns_record(module.params['api_url'], headers, module.params['record_name'], module)
    if existing_record:
        module.exit_json(changed=False, dns_record=existing_record)

    if module.check_mode:
        module.exit_json(changed=True, msg="DNS record will be created.")

    result = create_dns_record(module.params['api_url'], headers, module.params['record_name'], module.params['record_value'], module)
    if result:
        module.exit_json(changed=True, dns_record=result)
    else:
        
        module.fail_json(msg="Unknown error occurred while creating DNS record.")

if __name__ == '__main__':
    main()
