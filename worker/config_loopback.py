import requests
import urllib3
import json
from get_data import get_data
from save_data import save_config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def add_loopback_interface(router_ip, data, database_id):
    router_data = get_data(router_ip)
    username = router_data["username"]
    password = router_data["password"]
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    print(data["interface"])
    intf = data["interface"]
    ip = data["ip"]
    subnet = data["subnet"]
    description = data["description"]
    if data["status"] == "up":
        status = True
    else:
        status = False
    payload = {
        "ietf-interfaces:interface": {
            "name": f"{intf}",
            "description": f"{description}",
            "type": "iana-if-type:softwareLoopback",
            "enabled": status,
            "ietf-ip:ipv4": {
                "address": [{"ip": f"{ip}", "netmask": f"{subnet}"}]
            },
        }
    }
    url = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface={intf}"
    response = requests.put(
        url,
        data=json.dumps(payload),
        auth=(username, password),
        headers=headers,
        verify=False,
    )
    response.raise_for_status()
    print(f"Status Code: {response.status_code}")
    print(database_id)
    save_config(database_id["$oid"])


def delete_loopback_interface(router_ip, data, database_id):
    router_data = get_data(router_ip)
    username = router_data["username"]
    password = router_data["password"]
    headers = {
        "Accept": "application/yang-data+json",
    }
    intf = data["interface"]
    if "Loopback" in intf:
        url = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface={intf}"
        print(f"Attempting to delete interface: {intf}...")
        try:
            response = requests.delete(
                url,
                auth=(username, password),
                headers=headers,
                verify=False,
            )
            response.raise_for_status()

            print(
                f"Successfully deleted {intf}. Status Code: {response.status_code}"
            )
            deleted_something = True

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(
                    f"Interface {intf} not found (maybe already deleted?). Status: 404"
                )
            else:
                print(f"Error deleting interface {intf}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error while deleting {intf}: {e}")
    save_config(database_id["$oid"])
