#!/usr/bin/env python3
# -*-coding:UTF-8 -*-

import sys
import argparse
from lib import platform, arp


_supported_mac_format = ['win', 'unix', 'cisco']
_default_timeout = 2


def main() -> int:
    parser = argparse.ArgumentParser(
        prog='arping',
        description='Scan local network using ARP requests',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-n', '--name',
        help='Try to perform a reverse-lookup on found IP addresses',
        dest='do_name_lookup',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-f', '--format',
        help='Format to use to display MAC addressess\r\n'
             f'Supported values are: {_supported_mac_format}'
             f' (default: \'unix\')',
        dest='mac_format',
        type=str,
        required=False,
        choices=_supported_mac_format,
        default='unix'
    )

    parser.add_argument(
        '-t', '--timeout',
        help='Time, in second, to wait for a response\r\n'
             f'Default is {_default_timeout}',
        dest='timeout',
        type=int,
        default=_default_timeout,
        required=False
    )

    parser.add_argument(
        '-i', '--interface',
        help='Network interface to use for the scan',
        dest='interface',
        type=str,
        required=True
    )

    args = parser.parse_args()

    ifaces = platform.ip_interfaces()

    if not platform.is_root():
        print("Need to be root")
        return 1
    
    for _iface in ifaces:
        if args.interface != _iface.name:
            continue
        
        print(f"Scanning interface {_iface.name}, with IP {_iface.subnet}:")
        hosts = arp.pingsweep(
            net = _iface.subnet,
            do_lookup = args.do_name_lookup,
            mac_format = args.mac_format,
            timeout = args.timeout
        )

        for _host in hosts:
            _hostname = _host['hostname'] if 'hostname' in _host else ""
            print(f"\t{_host['ip']:<15} {_host['mac']} {_hostname}")
        
        return 0
    
    print(f"ERROR - {args.interface}: no such interface")
    return 1


if __name__ == '__main__':
    sys.exit(main())
