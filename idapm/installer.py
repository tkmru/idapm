#!/usr/bin/env python3
# coding: UTF-8

import glob
import json
import os
import platform
import shlex
import shutil
import subprocess
from pathlib import Path

from colorama import Fore


def get_plugin_dir():
    if platform.system() == 'Darwin':
        ida_root_list = glob.glob('/Applications/IDA*')
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            return ida_plugins_dir

    return None


def install_from_local(dir_name):
    ida_plugins_dir = get_plugin_dir()
    if ida_plugins_dir is not None:
        py_file_list = glob.glob(os.path.join(dir_name, '*.py'))
        for py_file_path in py_file_list:
            py_file_name = os.path.basename(py_file_path)
            plugin_file_path = os.path.join(ida_plugins_dir, py_file_name)
            shutil.copyfile(py_file_path, plugin_file_path)
            print('Copy to {0} from {1}'.format(plugin_file_path, py_file_path))
        
        print(Fore.CYAN + 'Installed successfully!')

    else:
        print(Fore.RED + 'Your OS is unsupported...')


def install_from_github(repo_name):
    '''
    After git clone plugin in ida_plugins_dir/idapm, and create a symbolic link to the python file from ida_plugins_dir
    '''
    ida_plugins_dir = get_plugin_dir()
    if ida_plugins_dir is not None:
        repo_name = shlex.quote(repo_name) # Countermeasures for command injection
        repo_url = 'git@github.com:{0}.git'.format(repo_name)
        installed_path = os.path.join(ida_plugins_dir, 'idapm', repo_name)
        proc = subprocess.Popen(['git', 'clone', repo_url, installed_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'))

        py_file_list = glob.glob(os.path.join(installed_path, '*.py'))
        for py_file_path in py_file_list:
            p = Path(py_file_path)
            symlink_path = os.path.join(ida_plugins_dir, p.parts[-1])
            if not os.path.exists(symlink_path):
                parent_dir = str(p.parent)
                if (len(p.parts) > 1) and (not os.path.exists(parent_dir)):
                    os.makedirs(parent_dir)
                os.symlink(py_file_path, os.path.join(ida_plugins_dir, symlink_path))

        print(Fore.CYAN + 'Installed successfully!')

    else:
        print(Fore.RED + 'Your OS is unsupported...')


def list_plugins():
    if platform.system() == 'Darwin':
        exclude_files = {
            'hexarm64.dylib', 'svdimport.dylib', 'dbg.dylib', 'pdb.dylib', 'callee64.dylib', 
            'objc64.dylib', 'pdb64.dylib', 'tds.dylib', 'defs.h', 'mac_stub.dylib', 'idapython3.dylib', 
            'eh_parse64.dylib', 'pin_user64.dylib', 'mac_user64.dylib', 'idapython3_64.dylib', 
            'idapython2_64.dylib', 'mac_user.dylib', 'dscu.dylib', 'eh_parse.dylib', 'swift64.dylib', 
            'uiswitch64.dylib', 'uiswitch.dylib', 'rtti64.dylib', 'comhelper64.dylib', 'unpack64.dylib', 
            'bochs_user.dylib', 'dalvik_user64.dylib', 'plugins.cfg', 'nextfix.dylib', 'tds64.dylib', 'pin_user.dylib', 
            'nextfix64.dylib', 'idapython2.dylib', 'samaout64.dylib', 'dscu64.dylib', 'strings.dylib', 'samaout.dylib', 
            'gdb_user64.dylib', 'mac_stub64.dylib', 'unpack.dylib', 'ios_user64.dylib', 'replay_user.dylib', 
            'makeidt.dylib', 'strings64.dylib', 'objc.dylib', 'hexrays_sdk', 'dbg64.dylib', 'linux_stub.dylib', 
            'xnu_user64.dylib', 'comhelper.dylib', 'dwarf.dylib', 'callee.dylib', 'dalvik_user.dylib', 'bdescr.dylib', 
            'linux_stub64.dylib', 'armlinux_stub.dylib', 'replay_user64.dylib', 'dwarf64.dylib', 'gdb_user.dylib', 
            'bochs_user64.dylib', 'win32_stub64.dylib', 'armlinux_stub64.dylib', 'ios_user.dylib', 'rtti.dylib', 
            'bochs', 'win32_stub.dylib', 'swift.dylib', 'svdimport64.dylib', 'bdescr64.dylib', 'makeidt64.dylib'
        }
        ida_root_list = glob.glob('/Applications/IDA*')
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_dir = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            added_plugins = set(os.listdir(ida_plugins_dir)) - exclude_files
            print(Fore.CYAN + 'List of files in IDA plugin directory')
            if len(added_plugins) == 0:
                print('None')
            else:
                for plugin in added_plugins:
                    print(plugin)

            print(Fore.CYAN + '\nList of files in config')
            home_dir = os.environ['HOME']
            config_path = home_dir + '/idapm.json'
            with open(config_path, 'r') as f:
                config_json = json.load(f)
                plugin_repos = config_json['plugins']
                if len(plugin_repos) == 0:
                    print('None')
                else:
                    for plugin in plugin_repos:
                        print(plugin)

    else:
        print('Your OS is unsupported...')