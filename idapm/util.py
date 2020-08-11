#!/usr/bin/env python3
# coding: UTF-8

import glob
import os
import platform
import shutil

from colorama import Fore


def install(dir_name):
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
        print('Your OS is unsupported...')
