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

    try:
        response = requests.get(
            url,
            auth=(username, password),
            headers=headers,
            verify=False,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {ip} for interfaces: {e}")
        return []

    data = response.json()
    count = 0
    interfaces_list = []
    
    if "Cisco-IOS-XE-interfaces-oper:interfaces" not in data or "interface" not in data["Cisco-IOS-XE-interfaces-oper:interfaces"]:
        print("Could not find 'interface' list in the response data.")
        return []

    for interface in data["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
        if interface["name"] == "Control Plane":
            continue
        status = "up" if interface.get("admin-status") == "if-state-up" else "down"
        protocol = (
            "up" if interface.get("oper-status") == "if-oper-state-ready" else "down"
        )

        ip_address = "unassigned"
        ip_subnet = "unassigned"
        if interface.get("ipv4") and interface.get("ipv4-subnet-mask"):
            ip_address = interface["ipv4"]
            ip_subnet = interface["ipv4-subnet-mask"]

        interfaces_list.append(
            {
                "interface": interface.get("name", "N/A"),
                "ip_address": ip_address,
                "subnet": ip_subnet,
                "mac_address": interface.get("phys-address", "N/A"),
                "status": status,
                "protocol": protocol,
                "description": interface.get("description", ""),
                "index": count,
            }
        )
        count += 1
    return interfaces_list


def get_routing_data(ip, username, password):
    url = f"https://{ip}:443/restconf/data/ietf-routing:routing-state/routing-instance=default/ribs/rib=ipv4-default"
    
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    try:
        response = requests.get(
            url,
            auth=(username, password),
            headers=headers,
            verify=False,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {ip} for routing data: {e}")
        return []

    data = response.json()
    routing_table = []

    if "ietf-routing:rib" not in data or "routes" not in data["ietf-routing:rib"] or "route" not in data["ietf-routing:rib"]["routes"]:
        print("Could not find 'route' list in the routing data response.")
        print("Received data:", json.dumps(data, indent=2))
        return []
    
    for route in data["ietf-routing:rib"]["routes"]["route"]:
        
        prefix = route.get("destination-prefix", "N/A")
        
        protocol_raw = route.get("source-protocol", "N/A")
        protocol = protocol_raw.split(":")[-1] if ":" in protocol_raw else protocol_raw

        metric = route.get("metric", "N/A")
        ad = route.get("route-preference", "N/A")

        next_hop_ip = "N/A"
        outgoing_interface = "N/A"

        next_hop_data = route.get("next-hop")
        if next_hop_data:
            next_hop_ip = next_hop_data.get("next-hop-address", "N/A")
            outgoing_interface = next_hop_data.get("outgoing-interface", "N/A")
        
        if protocol == "direct":
             next_hop_ip = "Connected"


        routing_table.append(
            {
                "prefix": prefix,
                "protocol": protocol,
                "ad": ad,
                "metric": metric,
                "next_hop": next_hop_ip,
                "interface": outgoing_interface,
            }
        )

    return routing_table


if __name__ == "__main__":
    ROUTER_IP = "192.168.230.131"
    USERNAME = "admin"
    PASSWORD = "cisco"

    print("--- 1. Getting Interface Data ---")
    int_data = get_int_data(ROUTER_IP, USERNAME, PASSWORD)
    print(json.dumps(int_data, indent=2))
    print("-" * 30)

    print("\n--- 2. Getting Routing Data (Using ietf-routing) ---")
    route_data = get_routing_data(ROUTER_IP, USERNAME, PASSWORD)
    print(json.dumps(route_data, indent=2))
    print("-" * 30)
