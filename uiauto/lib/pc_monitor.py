# -*- coding: utf-8 -*-
import logging
import time

from uiauto.lib.base_monitor import BaseMonitor

__author__ = 'litang.wang'


class PCMonitor(BaseMonitor):
    def __init__(self, config):
        BaseMonitor.__init__(self, config)
        self.chromedriver_path = config.chromedriver_path
        self.iedriver_path = config.iedriver_path
        self.first_url = config.first_url

    def tear_down_module(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception, e:
            logging.error(e)

    def set_up(self):
        try:
            self.driver.get(self.first_url)
            self.driver.maximize_window()
            time.sleep(2)
        except Exception, e:
            logging.error(e)
            logging.error("set up except")

    def tear_down(self):
        try:
            time.sleep(2)
        except Exception, e:
            logging.error(e)
            logging.error("tear down except")
