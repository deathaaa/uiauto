# -*- coding: utf-8 -*-
from uiauto.module.base_config import BaseConfig

__author__ = 'litang.wang'


class PCConfig(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        self.chromedriver_path = self.root_path + 'resource/chromedriver.exe'
        self.iedriver_path = self.root_path + 'resource/IEDriverServer.exe'
        self.first_url = 'http://tuan.qunar.com'
        self.thread_count = 1
