import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_int_data(ip, username, password):
    url = f"https://{ip}:443/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    response = requests.get(
        url,
        auth=(username, password),
        headers=headers,
        verify=False,
    )

    response.raise_for_status()

    data = response.json()
    count = 0
    interfaces_list = []
    for interface in data["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
        if interface["name"] == "Control Plane":
            continue
        status = "up" if interface.get("admin-status") == "if-state-up" else "down"
        protocol = (
            "up" if interface.get("oper-status") == "if-oper-state-ready" else "down"
        )

        ip_address = "unassigned"
        ip_subnet = "unassigned"
        if "ipv4" in interface and "ipv4-subnet-mask" in interface:
            ip_address = interface["ipv4"]
            ip_subnet = interface["ipv4-subnet-mask"]

        interfaces_list.append(
            {
                "interface": interface["name"],
                "ip_address": ip_address,
                "subnet": ip_subnet,
                "mac_address": interface["phys-address"],
                "status": status,
                "protocol": protocol,
                "description": interface["description"],
                "index": count,
            }
        )
        count += 1
    return interfaces_list


if __name__ == "__main__":
    print(get_int_data_restconf("192.168.86.141", "admin", "cisco"))
