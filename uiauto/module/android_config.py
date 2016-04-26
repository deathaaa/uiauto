# -*- coding: utf-8 -*-
import os

from uiauto.module.base_config import BaseConfig
from uiauto.util.android_util import AndroidUtil

__author__ = 'litang.wang'


def path(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class AndroidConfig(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        self.app_path = path(os.getcwd() + os.sep + 'resource' + os.sep + 'Qunar.apk')
        self.platformName = 'Android'
        self.version = '4.3'
        self.app_package = 'com.Qunar'
        self.app_activity = 'com.Qunar.NoteActivity'
        self.appium_path = r'C:\Appium\node_modules\appium\bin\appium.js'
        self.server_port = '4723'
        self.device_num = ''
        self.bootstrap_port = '4724'
        self.need_install = 'True'
        self.need_uninstall = 'True'
        self.thread_count = len(AndroidUtil.get_device_nums())
