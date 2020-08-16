#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
import json
import os

from . import config
from . import installer
from colorama import Fore


def cmd_init(args):
    if not config.check_exists():
        config_list = ['{',  '  "plugins": []', '}']
        with open(config_path, 'w') as f:
            f.write("\n".join(config_list))
        print(Fore.CYAN + '~/idapm.json was created successfully')
    else:
        plugin_repos = config.list_plugins()
        for plugin in plugin_repos:
            installer.install_from_github(plugin) 


def cmd_install(args):
    if args.local:
        installer.install_from_local(args.plugin_name)
    else:
        if config.add_plugin(args.plugin_name):
            installer.install_from_github(args.plugin_name) 


def cmd_list(args):
    installer.list_plugins()


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='IDA Plugin Manager')
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='')
    parser_init.set_defaults(handler=cmd_init)

    parser_install = subparsers.add_parser('install', aliases=['i'], help='')
    parser_install.add_argument('plugin_name', help='')
    parser_install.add_argument('--local', '-l', action='store_true')
    parser_install.set_defaults(handler=cmd_install)

    parser_list = subparsers.add_parser('list', help='')
    parser_list.set_defaults(handler=cmd_list)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
