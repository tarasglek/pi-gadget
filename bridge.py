#!/usr/bin/env python3
import json
import subprocess
import time

def run(cmd, collect_output=False):
    print(cmd)
    if not collect_output:
       subprocess.check_call(cmd, shell=True)
    else:
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

def main():
    addrls = json.loads(run("ip -j addr show wlan0", collect_output=True))
    ip_addr = None
    prefixlen = 0
    while not ip_addr:
        for addr in addrls:
            if addr.get('ifname') == 'wlan0':
                for ip in addr.get('addr_info', []):
                    ip_addr = ip.get('local')
                    prefixlen = ip.get('prefixlen', 0)
        if not ip_addr:
            print("Waiting for wlan0 to get ip")
            time.sleep(1)
    run("ip addr flush usb0")
    run(f"ip addr add {ip_addr}/{prefixlen} dev usb0")
    run("pkill -9 parprouted")
    run("ip link set wlan0 promisc on")
    run("parprouted usb0 wlan0")
    run("pkill dhcp-helper")
    run("dhcp-helper -i usb0 -b wlan0")
main()
