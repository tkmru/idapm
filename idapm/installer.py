#!/usr/bin/env python3
# coding: UTF-8

import copy
import glob
import json
import os
import platform
import shlex
import shutil
import subprocess

from . import config
from colorama import Fore
from os.path import expanduser


def get_plugin_dir():
    platform_name = platform.system()
    if platform_name == 'Darwin':
        ida_root_list = glob.glob('/Applications/IDA*')
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            return ida_plugins_dir

    elif platform_name == 'Windows':
        ida_dir_list = ['C:\Program Files\IDA*', 'C:\Program Files (x86)\IDA*']
        ida_root_list = []

        for ida_dir in ida_dir_list:
            ida_root_list.extend(glob.glob(ida_dir))
            if len(ida_root_list) == 1:
                ida_root_path = ida_root_list[0]
                ida_plugins_dir = os.path.join(ida_root_path, 'plugins')
                return ida_plugins_dir
    
    elif platform_name == 'Linux':
        home_dir = expanduser("~")
        ida_root_list = glob.glob(os.path.join(home_dir, 'ida*'))
        ida_root_list = [i for i in ida_root_list if not i.endswith('idapm.json')]
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'plugins')
            return ida_plugins_dir

    return None


def get_top_py_dir(py_path_list, ida_plugins_dir):
    result_dir = '.'
    flag = False
    for py_path in py_path_list:
        p = py_path.replace(ida_plugins_dir, '').replace('\\', '/').split('/')[3:]
        if len(p) == 2:
            flag = True
        else:
            if (p[1] != 'test') and (p[1] != 'tests'):
                result_dir = p[1]
    
    if flag:
        return None
    else:
        return result_dir


def install_from_local(dir_name):
    ida_plugins_dir = get_plugin_dir()
    if ida_plugins_dir is None:
        print(Fore.RED + 'Your OS is unsupported...')
        return False
    
    py_file_list = glob.glob(os.path.join(dir_name, '**/*.py'), recursive=True)
    for py_file_path in py_file_list:
        py_file_name = os.path.basename(py_file_path)
        plugin_file_path = os.path.join(ida_plugins_dir, py_file_name)
        shutil.copyfile(py_file_path, plugin_file_path)
        print('Copy to {0} from {1}'.format(plugin_file_path, py_file_path))

    print(Fore.CYAN + 'Installed successfully!')
    return True


def install_from_github(repo_name, repo_url):
    '''
    After git clone plugin in ida_plugins_dir/idapm, and create a symbolic link to the python file from ida_plugins_dir
    '''
    ida_plugins_dir = get_plugin_dir()
    if ida_plugins_dir is not None:
        repo_name = shlex.quote(repo_name)  # Countermeasures for command injection
        installed_path = os.path.join(ida_plugins_dir, 'idapm', repo_name)
        proc = subprocess.Popen(['git', 'clone', repo_url, installed_path], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            msg = outs.decode('ascii').replace('\n', '')
            print(msg)

        if (errs is not None) and (len(errs) != 0):
            msg = errs.decode('ascii').replace('\n', '')
            print(msg)
            if 'Repository not found' in msg:
                return False

        py_file_list = glob.glob(os.path.join(installed_path, '**/*.py'), recursive=True)
        top_dir = get_top_py_dir(py_file_list, ida_plugins_dir)
        for py_file_path in py_file_list:
            py_file_path = py_file_path.replace('\\', '/')
            py_file_name = os.path.basename(py_file_path)
            symlink_dir = os.path.dirname(py_file_path)
            symlink_dir_list = symlink_dir.split('/')
            if (symlink_dir_list[-1] != 'test') and (symlink_dir_list[-1] != 'tests'):
                symlink_dir = symlink_dir.replace('/'+repo_name, '').replace('/idapm', '')
                if top_dir is not None:
                   symlink_dir = symlink_dir.replace('/'+top_dir, '')
                symlink_path = os.path.join(symlink_dir, py_file_name)
                if not os.path.exists(symlink_path):
                    parent_dir = os.path.dirname(py_file_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                    os.symlink(py_file_path, symlink_path)
                    print('Symbolic link has been created ({0}).'.format(symlink_path))

        print(Fore.CYAN + 'Installed successfully!')
        return True

    else:
        print(Fore.RED + 'Your OS is unsupported...')
        return False


def list_plugins():
    platform_name = platform.system()
    if platform_name == 'Darwin':
        exclude_files = {
            'plugins.cfg', 'hexrays_sdk', 'bochs', 'idapm'
        }
        ida_root_list = glob.glob('/Applications/IDA*')
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            added_plugins = set(os.listdir(ida_plugins_dir)) - exclude_files
            added_plugins = [i for i in added_plugins if (not i.endswith('.dylib')) and (not i.endswith('.h'))]
            print(Fore.CYAN + 'List of scripts in IDA plugin directory')
            if len(added_plugins) == 0:
                print('None')
            else:
                for plugin in added_plugins:
                    print(plugin)

            print(Fore.CYAN + '\nList of plugins in config')
            c = config.Config()
            plugin_repos = c.list_plugins()
            if len(plugin_repos) == 0:
                print('None')
            else:
                for plugin in plugin_repos:
                    print(plugin)

    elif platform_name == 'Windows':
        exclude_files = {
            'plugins.cfg', 'idapm'
        }
        ida_dir_list = ['C:\Program Files\IDA*', 'C:\Program Files (x86)\IDA*']
        ida_root_list = []
        for ida_dir in ida_dir_list:
            ida_root_list.extend(glob.glob(ida_dir))

        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'plugins')
            added_plugins = set(os.listdir(ida_plugins_dir)) - exclude_files
            added_plugins = [i for i in added_plugins if not i.endswith('.dll')]
            print(Fore.CYAN + 'List of scripts in IDA plugin directory')
            if len(added_plugins) == 0:
                print('None')
            else:
                for plugin in added_plugins:
                    print(plugin)

            print(Fore.CYAN + '\nList of plugins in config')
            c = config.Config()
            plugin_repos = c.list_plugins()
            if len(plugin_repos) == 0:
                print('None')
            else:
                for plugin in plugin_repos:
                    print(plugin)
    
    elif platform_name == 'Linux':
        exclude_files = {
            'platformthemes', 'platforms', 'plugins.cfg', 'idapm'
        }
        home_dir = expanduser("~")
        ida_root_list = glob.glob(os.path.join(home_dir, 'ida*'))
        ida_root_list = [i for i in ida_root_list if not i.endswith('idapm.json')]
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'plugins')
            added_plugins = set(os.listdir(ida_plugins_dir)) - exclude_files
            added_plugins = [i for i in added_plugins if not i.endswith('.so')]
            print(Fore.CYAN + 'List of scripts in IDA plugin directory')
            if len(added_plugins) == 0:
                print('None')
            else:
                for plugin in added_plugins:
                    print(plugin)

            print(Fore.CYAN + '\nList of plugins in config')
            c = config.Config()
            plugin_repos = c.list_plugins()
            if len(plugin_repos) == 0:
                print('None')
            else:
                for plugin in plugin_repos:
                    print(plugin)
    else:
        print('Your OS is unsupported...')
