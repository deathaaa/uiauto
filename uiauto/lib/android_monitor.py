# -*- coding: utf-8 -*-
import logging
import os
import time

from uiauto.lib.android_init import AndroidInit
from uiauto.lib.base_monitor import BaseMonitor

try:
    from appium import webdriver
except Exception, e:
    logging.error(e)

__author__ = 'litang.wang'


class AndroidMonitor(BaseMonitor):
    def __init__(self, config):
        BaseMonitor.__init__(self, config)

        self.desired_caps = {
            'browserName': '',
            'platformName': self.config.platformName,
            'version': self.config.version,
            'app-package': self.config.app_package,
            'app-activity': self.config.app_activity
        }
        self.server_port = self.config.server_port

        self.executor_path = r'http://127.0.0.1:' + str(self.server_port) + '/wd/hub'

    def set_up_module(self):
        AndroidInit.init(self.config.appium_path, self.config.app_path, self.server_port, self.config.bootstrap_port,
                         self.desired_caps['app-package'], self.config.device_num, self.config.need_uninstall,
                         self.config.need_install)
        for i in range(0, 10, 1):
            try:
                time.sleep(5)
                self.driver = webdriver.Remote(self.executor_path, self.desired_caps)

                # time.sleep(10)
                self.driver.close_app()
                break
            except Exception, e:
                logging.error(e)
                logging.error("webdriver.Remote except")
                if i == 4:
                    print os.popen('adb -s %s reboot' % self.config.device_num).read()
                    time.sleep(30)
                if i >= 9:
                    raise Exception()
                time.sleep(10)

    def tear_down_module(self):
        try:
            self.driver.quit()
        except Exception, e:
            logging.error(e)

    def set_up(self):
        try:
            self.driver.launch_app()
        except Exception, e:
            logging.error(e)
            logging.error("set up except")

    def tear_down(self):
        try:
            time.sleep(2)
            self.driver.close_app()
            time.sleep(2)
        except Exception, e:
            logging.error(e)
            logging.error("tear down except")
