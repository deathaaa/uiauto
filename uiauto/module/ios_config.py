# -*- coding: utf-8 -*-
from uiauto.module.base_config import BaseConfig

__author__ = 'litang.wang'


class IosConfig(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        self.platformName = 'ios'
        self.platformVersion = '8.1'
        self.deviceName = 'iPhone 5'
        self.app = 'com.Qunar.des.test'
        self.server_port = '4723'
