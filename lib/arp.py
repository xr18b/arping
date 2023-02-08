#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

from scapy.all import srp,Ether,ARP,conf
import netaddr
import socket

def get_host(ip):
    try:
        return ' ({0})'.format(socket.gethostbyaddr(ip)[0])
    except:
        return None


def pingsweep(net, do_lookup = False) -> list:
    conf.verb=0

    _answer,_unanswer=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(net.cidr)),timeout=2)

    hosts = []

    for snd,rcv in _answer:
        mac = netaddr.EUI(rcv[Ether].src)
        mac.dialect = netaddr.mac_unix
        ip = rcv[ARP].psrc

        _host = {"ip": ip, "mac": mac}

        if do_lookup:
            _hostname = get_host(ip)
            if _hostname:
                _host["hostname"] = _hostname

        hosts.append(_host)

    return sorted(hosts, key=lambda d: d['ip'])
