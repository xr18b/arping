#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import sys
from lib import platform, arp


_supported_mac_format = ['win', 'unix', 'cisco']
_default_timeout = 2


def usage() -> None:
    """
    Print help message and exit
    """
    print(f"""usage: {sys.argv[0]} [-h] [-n] [-f FORMAT]

Optional arguments:
    -h, --help   Show this help message and exit
    -n, --name   Try to perform a reverse-lookup on found IP addresses
    -f FORMAT, --format FORMAT
                 Format to use to display MAC addresses.
                 Acceptable values are: unix (default), win, cisco
    -t VALUE, --timeout VALUE
                 Time in seconds to wait for response
                 Default is {_default_timeout}
    -i VALUE, --interface VALUE
                 Limit the scan to specific interface""")


def main(argv) -> None:
    do_lookup = False
    mac_format = 'unix'
    timeout = _default_timeout

    if '-h' in argv or '--help' in argv:
        usage()
        sys.exit(0)

    if '-n' in argv or '--name' in argv:
        do_lookup = True

    if '-f' in argv:
        try:
            mac_format = argv[argv.index('-f')+1]
        except IndexError:
            print("ERROR - missing argument to `-f`")
            sys.exit(1)
        if mac_format not in _supported_mac_format:
            print(f"ERROR - Unknown format `{mac_format}`")
            sys.exit(1)

    if '--format' in argv:
        try:
            mac_format = argv[argv.index('--format')+1]
        except IndexError:
            print("ERROR - missing argument to `--format`")
            sys.exit(1)
        if mac_format not in _supported_mac_format:
            print(f"ERROR - Unknown format `{mac_format}`")
            sys.exit(1)

    if '-t' in argv:
        timeout = argv[argv.index('-t')+1]
        try:
            timeout = int(timeout)
        except ValueError:
            print("ERROR - timeout should be an integer")
            sys.exit(1)

    if '--timeout' in argv:
        timeout = argv[argv.index('--timeout')+1]
        try:
            timeout = int(timeout)
        except ValueError:
            print("ERROR - timeout should be an integer")
            sys.exit(1)

    ifaces = platform.ip_interfaces()

    # Create a list with all interfaces name to be able to verify against it
    ifaces_names = []
    for _iface in ifaces:
        ifaces_names.append(_iface.name)

    if '-i' in argv:
        try:
            limit_iface = argv[argv.index('-i')+1]
        except IndexError:
            print("ERROR - missing argument to `-i`")
            sys.exit(1)
        if limit_iface not in ifaces_names:
            print(f"ERROR - {limit_iface}: no such interface")
            sys.exit(1)

    if '--interface' in argv:
        try:
            limit_iface = argv[argv.index('--interface')+1]
        except IndexError:
            print("ERROR - missing argument to `--interface`")
            sys.exit(1)
        if limit_iface not in ifaces_names:
            print(f"ERROR - {limit_iface}: no such interface")
            sys.exit(1)

    if not platform.is_root():
        print("Need to be root")
        sys.exit(1)

    for _iface in ifaces:
        if limit_iface != _iface.name:
            continue

        print(f"Scanning interface {_iface.name}, with IP {_iface.subnet}:")
        hosts = arp.pingsweep(
            net = _iface.subnet,
            do_lookup = do_lookup,
            mac_format = mac_format,
            timeout = timeout
        )

        for _host in hosts:
            _hostname = _host['hostname'] if 'hostname' in _host else ""
            print(f"\t{_host['ip']:<15} {_host['mac']} {_hostname}")

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
