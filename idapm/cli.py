#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
import json
import os

from colorama import Fore
from . import installer


def cmd_init(args):
    home_dir = os.environ['HOME']
    config_path = home_dir + '/idapm.json'
    if not os.path.isfile(config_path):
        config_list = ['{',  '  "plugins": []', '}']
        with open(config_path, 'w') as f:
            f.write("\n".join(config_list))
        print(Fore.CYAN + '~/idapm.json was created successfully')
    else:
        with open(config_path, 'r') as f:
            config_json = json.load(f)
            plugin_repos = config_json['plugins']    
            for plugin in plugin_repos:
                installer.install_from_github(plugin) 


def cmd_install(args):
    if args.local:
        installer.install_from_local(args.dir_name)
    else:
        installer.install_from_github(args.repo_name) 


def cmd_list(args):
    installer.list_plugins()


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='IDA Plugin Manager')
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='')
    parser_init.set_defaults(handler=cmd_init)

    parser_install = subparsers.add_parser('install', aliases=['i'], help='')
    parser_install.add_argument('dir_name', help='')
    parser_install.add_argument('--local', '-l', action='store_true')
    parser_install.set_defaults(handler=cmd_install)

    parser_list = subparsers.add_parser('list', help='')
    parser_list.set_defaults(handler=cmd_list)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
