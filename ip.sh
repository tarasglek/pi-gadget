#!/bin/bash
set -x
ip addr flush dev usb0
ip addr add 10.10.10.1/24 dev usb0


iptables -F; iptables -t nat -F; iptables -t mangle -F
/sbin/iptables -t nat -A POSTROUTING -s 10.10.10.0/24  -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -o wlan0 -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward

pkill dnsmasq
dnsmasq --dhcp-range=usb0,10.10.10.10,10.10.10.20,4h
