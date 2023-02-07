#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import os
import netifaces
import netaddr


LOCALHOST_ADDR = ['127.0.0.1', 'localhost']


class Interface:
    def __init__(self, name):
        self.name = name
        self.ifaddresses = None
        self.ip = None
        self.subnet = None
        self.netmask = None
        self.get_data()

    def get_data(self) -> None:
        try:
            self.ifaddresses = netifaces.ifaddresses(self.name)[netifaces.AF_INET][0]
            self.ip = netaddr.IPAddress(self.ifaddresses['addr'])
            self.netmask = netaddr.IPAddress(self.ifaddresses['netmask'])
            self.subnet = netaddr.IPNetwork('{0}/{1}'.format(self.ip, self.netmask))
        except KeyError:
            pass

    def has_ip(self) -> str:
        return self.ip

    def not_localhost(self):
        return str(self.ip) not in LOCALHOST_ADDR


def is_root() -> bool:
    """Verifies if the current user is root"""
    return not os.getuid()


def interfaces() -> list:
    return [Interface(i) for i in netifaces.interfaces()]


def ip_interfaces() -> list:
    ifaces = []

    for _iface in interfaces():
        if _iface.has_ip() and _iface.not_localhost():
            ifaces.append(_iface)

    return ifaces
