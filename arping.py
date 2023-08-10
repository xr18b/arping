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
                 Acceptable values are: unix (default), win, cisco
    -t VALUE, --timeout VALUE
                 Time in seconds to wait for response
                 Default is 2
    -i VALUE, --interface VALUE
                 Limit the scan to specific interface'''.format(sys.argv[0]))


def main(argv) -> None:
    do_lookup = False
    mac_format = 'unix'
    timeout = 5

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

    if '-t' in argv:
        timeout = argv[argv.index('-t')+1]
        try:
            timeout = int(timeout)
        except ValueError:
            print('ERROR - timeout should be an integer')
            sys.exit(1)

    if '--timeout' in argv:
        timeout = argv[argv.index('--timeout')+1]
        try:
            timeout = int(timeout)
        except ValueError:
            print('ERROR - timeout should be an integer')
            sys.exit(1)

    ifaces = platform.ip_interfaces()

    # Create a list with all interfaces name to be able to verify if the filtered interface exists
    ifaces_names = []
    for _iface in ifaces:
        ifaces_names.append(_iface.name)

    if '-i' in argv:
        try:
            limit_iface = argv[argv.index('-i')+1]
        except IndexError:
            print('ERROR - missing argument to `-i`')
            sys.exit(1)
        if limit_iface not in ifaces_names:
            print('ERROR - {0}: no such interface'.format(limit_iface))
            sys.exit(1)

    if '--interface' in argv:
        try:
            limit_iface = argv[argv.index('--interface')+1]
        except IndexError:
            print('ERROR - missing argument to `--interface`')
            sys.exit(1)
        if limit_iface not in ifaces_names:
            print('ERROR - {0}: no such interface'.format(limit_iface))
            sys.exit(1)

    if not platform.is_root():
        print('Need to be root')
        sys.exit(1)

    for _iface in ifaces:
        if limit_iface != _iface.name:
            continue

        print('Scanning interface {0}, with IP {1}:'.format(_iface.name, _iface.subnet))
        hosts = arp.pingsweep(net = _iface.subnet, do_lookup = do_lookup, mac_format = mac_format, timeout = timeout)

        for _host in hosts:
            print('\t{0:<15} {1} {2}'.format(
                _host['ip'],
                _host['mac'],
                _host['hostname'] if 'hostname' in _host else "")
            )

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
