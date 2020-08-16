#!/usr/bin/env python3
# coding: UTF-8

import json
import os

home_dir = os.environ['HOME']
config_path = home_dir + '/idapm.json'

def check_exists():
    return os.path.isfile(config_path)


def make_config():
    config_json = {'plugins': []}
    with open(config_path, 'w') as f:
        json.dump(config_json, f, indent=2)


def add_plugin(plugin_repo):
    with open(config_path, 'r+') as f:
        config_json = json.load(f)
        if plugin_repo not in config_json['plugins']:
            config_json['plugins'].append(plugin_repo)
            f.seek(0)
            json.dump(config_json, f, indent=2)
            return True

        else:
            print('{0} already exists'.format(plugin_repo))
            return False


def list_plugins():
    with open(config_path, 'r') as f:
        config_json = json.load(f)
        return config_json['plugins']
