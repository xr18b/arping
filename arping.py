#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import sys
from lib import platform, arp


def main(argv) -> None:
    if not platform.is_root():
        print('Need to be root')
        sys.exit(1)

    ifaces = platform.ip_interfaces()

    for _iface in ifaces:
        print('Scanning interface {0}, with IP {1}:'.format(_iface.name, _iface.subnet))
        hosts = arp.pingsweep(_iface.subnet)
        for _host in hosts:
            print('\t{0} - {1}{2}'.format(_host[0], _host[1], _host[2]))

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
