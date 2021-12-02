#!/usr/bin/env python3

import json
import os
import argparse
import re

from nagiode import Nagios

def parse_cmd_args(args):
    cmd_args = {}
    for a in args:
        ret = re.match("([^=]+)=(.*)", a)
        if ret:
            cmd_args[ret.group(1)] = ret.group(2)
    return cmd_args


def main():
    parser = argparse.ArgumentParser(description="Nagiode v0.1")
    parser.add_argument("-c", "--command", help="Nagios Command to use. Use -l to list available commands", default=None)
    parser.add_argument("-l", "--list", help="List available commands. If used with -c list arguments for command.", action="store_true", default=False)
    parser.add_argument("-a", "--arg", action="append", default=[])
    parser.add_argument("-H", "--host", help="Nagios Host", default=os.environ.get("NAGIOS_HOST"))
    parser.add_argument("-U", "--username", help="Nagios Username", default=os.environ.get("NAGIOS_USER"))
    parser.add_argument("-P", "--password", help="Nagios Password", default=os.environ.get("NAGIOS_PASS"))
    parser.add_argument("-s", "--status", help="Get Host status. Requires -a host=<host>", action="store_true", default=False)
    parser.add_argument("-G", "--cgi", help="Nagios CGI Path", default=os.environ.get("NAGIOS_CGI"))
    parser.add_argument("-d", "--debug", help="Print url and args and exit without executing", action="store_true", default=False)

    args = parser.parse_args()

    nagios = Nagios(args.host, args.username, args.password, cgi_path=args.cgi, debug=args.debug)

    if args.command and args.list:
        print(json.dumps(nagios.list_arguments(args.command)))
    elif args.list:
        print(json.dumps(nagios.list_commands()))
    elif args.command:
        cmd_args = parse_cmd_args(args.arg)
        print(nagios.cmd(args.command, **cmd_args))
    elif args.status:
        cmd_args = parse_cmd_args(args.arg)
        print(json.dumps(nagios.status(**cmd_args)))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
