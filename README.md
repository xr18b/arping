# ARPING
ARPING is a tool that lists all devices answering to ARP requests on the local network.

The MAC addresses can be print on different format (Unix, Windows and Cisco).

Optionally, you can also have it try to perform a reverse-lookup to print the hostname of found devices (-n, --name).

## Usage
```bash
./arping.py

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
                 Limit the scan to specific interface
```

