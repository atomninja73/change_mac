#!/usr/bin/env python

import subprocess
import re
import time


def get_self_mac(interface):
    output = subprocess.check_output(["ifconfig", interface])
    output = str(output)
    mac_addr = re.findall("[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}", output)
    return mac_addr[0]


def get_fake_mac():
    mac_address_list = ["b8:c8:eb:16:37:62", "b0:45:30:db:6f:68", "00:00:4b:08:f5:00"]
    fake_mac = mac_address_list[0]
    return fake_mac


def change_mac(interface):
    original_mac = get_self_mac(interface)
    updated_mac = get_fake_mac()
    try:
        print("\r[+] Changing MAC address to ...", updated_mac, "\n")
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", updated_mac])
        subprocess.call(["ifconfig", interface, "up"])
        while True:
            subprocess.call(["ifconfig", interface, "hw", "ether", updated_mac])
            time.sleep(20)
    except KeyboardInterrupt:
        print("\r[+] Setting MAC address to original...", original_mac,"\n")
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", original_mac])
        subprocess.call(["ifconfig", interface, "up"])


inter_face = "eth0"
change_mac(inter_face)
