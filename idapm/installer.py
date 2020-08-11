#!/usr/bin/env python3
# coding: UTF-8

import glob
import os
import platform
import shutil

from colorama import Fore


def install_from_local(dir_name):
    if platform.system() == 'Darwin':
        ida_root_list = glob.glob('/Applications/IDA*')
        if len(ida_root_list) == 1:
            ida_root_path = ida_root_list[0]
            ida_plugins_path = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            py_file_list = glob.glob(os.path.join(dir_name, '*.py'))
            # TODO: Improved the accuracy of searching Python files
            for py_file_path in py_file_list:
                py_file_name = os.path.basename(py_file_path)
                plugin_file_path = os.path.join(ida_plugins_path, py_file_name)
                shutil.copyfile(py_file_path, plugin_file_path)
                print('Copy to {0} from {1}'.format(plugin_file_path, py_file_path))
            
            print(Fore.CYAN + 'Installed successfully!')

    else:
        print(Fore.RED + 'Your OS is unsupported...')

'''
def install_from_github(dir_name):
'''

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
            ida_plugins_path = os.path.join(ida_root_path, 'ida.app/Contents/MacOS/plugins')
            added_plugins = set(os.listdir(ida_plugins_path)) - exclude_files
            print(Fore.CYAN + 'List of files in IDA plugin directory')
            if len(added_plugins) == 0:
                print('None')
            else:
                for plugin in added_plugins:
                    print(plugin)

            print(Fore.CYAN + '\nList of files in config')
    else:
        print('Your OS is unsupported...')