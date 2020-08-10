#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama

from . import util


def cmd_install(args):
    util.install(args.dir_name)


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='installer for IDA plugin')
    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser('install', aliases=['i'], help='')
    parser_build.add_argument('dir_name', help='')
    parser_build.set_defaults(handler=cmd_install)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
