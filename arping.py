#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import sys
from lib import platform, arp


_supported_mac_format = ['win', 'unix', 'cisco']


def usage() -> None:
    """
    Print help message and exit
    """
    print('''usage: {0} [-h] [-n] [-f FORMAT]

Optional arguments:
    -h, --help   Show this help message and exit
    -n, --name   Try to perform a reverse-lookup on found IP addresses
    -f FORMAT, --format FORMAT
                 Format to use to display MAC addresses.
                 Acceptable values are: unix (default), win, cisco'''.format(sys.argv[0]))


def main(argv) -> None:
    do_lookup = False
    mac_format = 'unix'

    if '-h' in argv or '--help' in argv:
        usage()
        sys.exit(0)

    if '-n' in argv or '--name' in argv:
        do_lookup = True

    if '-f' in argv:
        try:
            mac_format = argv[argv.index('-f')+1]
        except IndexError:
            print('ERROR - missing argument to `-f`')
            sys.exit(1)
        if mac_format not in _supported_mac_format:
            print('ERROR - Unknown format `{0}`'.format(mac_format))
            sys.exit(1)

    if '--format' in argv:
        try:
            mac_format = argv[argv.index('--format')+1]
        except IndexError:
            print('ERROR - missing argument to `--format`')
            sys.exit(1)
        if mac_format not in _supported_mac_format:
            print('ERROR - Unknown format `{0}`'.format(mac_format))
            sys.exit(1)

    if not platform.is_root():
        print('Need to be root')
        sys.exit(1)

    ifaces = platform.ip_interfaces()

    for _iface in ifaces:
        print('Scanning interface {0}, with IP {1}:'.format(_iface.name, _iface.subnet))
        hosts = arp.pingsweep(net = _iface.subnet, do_lookup = do_lookup, mac_format = mac_format)

        for _host in hosts:
            print('\t{0:<15} {1} {2}'.format(
                _host['ip'],
                _host['mac'],
                _host['hostname'] if 'hostname' in _host else "")
            )

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
