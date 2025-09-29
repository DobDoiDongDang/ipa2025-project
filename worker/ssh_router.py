from netmiko import ConnectHandler


def create_device(ip, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "use_keys": False,
        "disabled_algorithms": dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
    }
    return device


def get_int_data(ip, username, password):
    device = create_device(ip, username, password)
    router_connect = ConnectHandler(**device)
    output = router_connect.send_command("show ip int brief", use_textfsm=True)
    return output


if __name__ == "__main__":
    print(get_int_data("192.168.86.141", "admin", "admin"))
