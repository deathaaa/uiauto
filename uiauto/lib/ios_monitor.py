# -*- coding: utf-8 -*-
import logging
import os
import time

from uiauto.lib.base_monitor import BaseMonitor

try:
    from appium import webdriver
except Exception, e:
    logging.error(e)

__author__ = 'litang.wang'


class IosMonitor(BaseMonitor):
    def __init__(self, config):
        BaseMonitor.__init__(self, config)
        self.desired_caps = {
            'browserName': '',
            'platformName': self.config.platformName,
            'platformVersion': self.config.platformVersion,
            'deviceName': self.config.deviceName,
            'app': self.config.app,
        }

        self.server_port = self.config.server_port
        self.executor_path = r'http://127.0.0.1:' + str(self.server_port) + '/wd/hub'

    def set_up_module(self):
        os.system('ios_init.sh %s %s' % (self.config.device_num, self.config.app))
        for i in range(0, 5, 1):
            try:
                time.sleep(3)
                self.driver = webdriver.Remote(self.executor_path, self.desired_caps)
                self.driver.close_app()
                break
            except Exception, e:
                print e
                time.sleep(3)
                logging.error("webdriver.Remote except")

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
            self.driver.close_app()
        except Exception, e:
            logging.error(e)
            logging.error("tear down except")
