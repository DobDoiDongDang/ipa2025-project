import requests
import urllib3
import json
from get_data import get_data
from save_data import save_config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def add_interface(router_ip, data, database_id):
    router_data = get_data(router_ip)
    username = router_data["username"]
    password = router_data["password"]
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    for interface in data:
        intf = interface["interface"]
        ip = interface["ip"]
        subnet = interface["subnet"]
        description = interface["description"]
        if interface["status"] == "up":
           status = True
        else:
            status = False
        if "Loopback" in intf:
            payload = {
                "ietf-interfaces:interface": {
                    "name": f"{intf}",
                    "description": f"{description}",
                    "type": "iana-if-type:softwareLoopback",
                    "enabled": status,
                    "ietf-ip:ipv4": {
                        "address": [{
                            "ip": f"{ip}",
                            "netmask": f"{subnet}"
                        }]
                }}
                }
        url = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface={intf}"
        response = requests.put(
            url,
            data=json.dumps(payload),
            auth=(username, password),
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
    save_config(database_id["$oid"])


#def config_ip_loopback(ip, username, password, new_ip):

