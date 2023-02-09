#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

from scapy.all import srp,Ether,ARP,conf
import netaddr
import socket

def get_host(ip):
    """
    Try to perform reverse lookup of the given IP address

    :param ip:  IP address to look for
    :return:    Str containing the hostname between brackets, or empty if no result
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None


def pingsweep(net, do_lookup = False, mac_format = 'unix') -> list:
    """
    Will perform ARP request for every ip addresses in the given range
    
    :param net:  IP range
    :do_lookup:  Set to 'True' to try reverse lookup on responding IP addresses
                 Default it 'False'
    :return:     List of dictionnaries containing IP, MAC and Hostname of replying hosts
    """
    conf.verb=0

    _answer,_unanswer=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(net.cidr)),timeout=2)

    hosts = []

    for snd,rcv in _answer:
        mac = netaddr.EUI(rcv[Ether].src)
        ip = rcv[ARP].psrc
        if mac_format == 'cisco':
            mac.dialect = netaddr.mac_cisco
        elif mac_format == 'unix': 
            mac.dialect = netaddr.mac_unix_expanded

        _host = {"ip": ip, "mac": mac}

        if do_lookup:
            _hostname = get_host(ip)
            if _hostname:
                _host["hostname"] = _hostname

        hosts.append(_host)

    return sorted(hosts, key=lambda d: d['ip'])
