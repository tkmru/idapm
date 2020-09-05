#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
import json
import os

from . import installer
from . import config
from colorama import Fore


def cmd_check(args):
    print('IDA plugin dir:    {0}'.format(installer.get_plugin_dir()))
    c = config.Config()
    print('idapm config path: {0}'.format(c.config_path))


def cmd_init(args):
    c = config.Config()
    if not c.check_exists():
        try:
            c.make_config()
            print(Fore.CYAN + '~/idapm.json was created successfully!')

        except:
            print(Fore.RED + 'Creation of ~/idapm.json failed...')

    else:
        print('~/idapm.json already exists...')
        while True:
            input_pattern = {'y': True, 'yes': True, 'n': False, 'no': False}
            try:
                key = input('Do you want to install a plugin written in ~/idapm.json? [Y/n]: ').lower()
                if input_pattern[key]:
                    plugin_repos = c.list_plugins()
                    for plugin in plugin_repos:
                        print('----------------------')
                        try:
                            repo_url = 'https://github.com/{0}.git'.format(repo_name)
                            print('Try: git clone {0}'.format(repo_url))
                            installer.install_from_github(plugin, repo_url)

                        except:
                            repo_url = 'git@github.com:{0}.git'.format(repo_name)
                            print('Try: git clone {0}'.format(repo_url))
                            installer.install_from_github(plugin, repo_url)
                break

            except:
                pass


def cmd_install(args):
    if args.local:
        installer.install_from_local(args.plugin_name)
    else:
        c = config.Config()
        if c.check_duplicate(args.plugin_name):
            print(Fore.RED + '{0} already exists in config'.format(args.plugin_name))
            input_pattern = {'y': True, 'yes': True, 'n': False, 'no': False}
            key = input('Do you want to reinstall {0}? [Y/n]: '.format(args.plugin_name)).lower()
            if not input_pattern[key]:
                return

        print('----------------------')
        repo_https_url = 'https://github.com/{0}.git'.format(args.plugin_name)
        print('Try: git clone {0}'.format(repo_https_url))
        if installer.install_from_github(args.plugin_name, repo_https_url):
            c.add_plugin(args.plugin_name)

        else:
            repo_ssh_url = 'git@github.com:{0}.git'.format(args.plugin_name)
            print('Try: git clone {0}'.format(repo_ssh_url))
            if installer.install_from_github(args.plugin_name, repo_ssh_url):
                c.add_plugin(args.plugin_name)


def cmd_list(args):
    installer.list_plugins()


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='IDA Plugin Manager')
    subparsers = parser.add_subparsers()

    parser_check = subparsers.add_parser('check', help='')
    parser_check.set_defaults(handler=cmd_check)

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
