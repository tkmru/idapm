#!/usr/bin/env python3
# coding: UTF-8

import json
import os


class Config(object):

    def __init__(self):
        home_dir = os.environ['HOME']
        self.config_path = home_dir + '/idapm.json'

    def check_exists(self):
        return os.path.isfile(self.config_path)

    def make_config(self):
        config_json = {'plugins': []}
        with open(self.config_path, 'w') as f:
            json.dump(config_json, f, indent=2)

    def add_plugin(self, plugin_repo):
        with open(self.config_path, 'r+') as f:
            config_json = json.load(f)
            if plugin_repo not in config_json['plugins']:
                config_json['plugins'].append(plugin_repo)
                f.seek(0)
                json.dump(config_json, f, indent=2)
                return True

            else:
                return False

    def list_plugins(self):
        with open(self.config_path, 'r+') as f:
            config_json = json.load(f)
            no_duplicate_plugins = list(set(config_json['plugins']))
            config_json['plugins'] = no_duplicate_plugins
            f.seek(0)
            json.dump(config_json, f, indent=2)
            return no_duplicate_plugins
