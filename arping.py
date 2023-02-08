#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import sys
from lib import platform, arp


def usage() -> None:
    print('''usage: {0} [-h] [-n]

Optional arguments:
    -h, --help   Show this help message and exit
    -n, --name   Try to perform a reverse-lookup on found IP addresses'''.format(sys.argv[0]))


def main(argv) -> None:
    do_lookup = False

    if '-h' in argv or '--help' in argv:
        usage()
        sys.exit(0)

    if '-n' in argv or '--name' in argv:
        do_lookup = True

    if not platform.is_root():
        print('Need to be root')
        sys.exit(1)

    ifaces = platform.ip_interfaces()

    for _iface in ifaces:
        print('Scanning interface {0}, with IP {1}:'.format(_iface.name, _iface.subnet))
        hosts = arp.pingsweep(net = _iface.subnet, do_lookup = do_lookup)

        for _host in hosts:
            print('\t{0} - {1}{2}'.format(
                _host['ip'],
                _host['mac'],
                _host['hostname'] if 'hostname' in _host else "")
            )

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
