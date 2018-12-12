#!/usr/bin/env python

"""MariaDB slave status checker"""

import argparse
import sys

from nagios_plugin import SlaveStatusCheck


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='MariaDB slave status checker')
    parser.add_argument('--hostname', default='localhost', type=str,
                        help="MariaDB hostname")
    parser.add_argument('--username', type=str, help="MariaDB username")
    parser.add_argument('--password', type=str, help="MariaDB password")
    parser.add_argument('--connection', required=True, type=str,
                        help="MariaDB slave connection name")
    parser.add_argument('--mode', type=str, required=True,
                        choices=SlaveStatusCheck.MODES,
                        help="slave state to check")
    parser.add_argument('-w', '--warning', type=int, default=None,
                        help="warning limit")
    parser.add_argument('-c', '--critical', type=int, default=None,
                        help="critical limit")
    parser.add_argument('--verbose', action='store_true', default=False,
                        help="enable verbose mode")
    parser.add_argument('-H', '--human-readable', action='store_true',
                        default=False, help="human readable replication lag")

    args = parser.parse_args(args)
    ssc = SlaveStatusCheck(args.hostname, args.username, args.password,
                           args.connection, args.mode, args.verbose,
                           args.warning, args.critical, args.human_readable)
    ssc.get_slave_status()
    ssc.run_check()

if __name__ == '__main__':
    main() # pragma: no cover
