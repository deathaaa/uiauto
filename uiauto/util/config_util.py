# -*- coding: utf-8 -*-
from uiauto.util.config_reader import ConfigReader

__author__ = 'litang.wang'


class ConfigUtil:
    def __init__(self):
        pass

    @staticmethod
    def get_config(config_path, config_class):
        config_reader = ConfigReader(config_path)
        type = config_reader.read('type', 'config')
        config = config_class()
        items = config_reader.items(type)
        for (key, value) in items:
            setattr(config, key, value)
        setattr(config, 'conf_file', config_path)
        setattr(config, 'type', type)
        return config
