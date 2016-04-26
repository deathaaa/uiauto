# -*- coding: utf-8 -*-
import logging
import thread
import time

from selenium import webdriver

from uiauto.lib.pc_monitor import PCMonitor

__author__ = 'litang.wang'

lock = thread.allocate_lock()


class PCFirefoxMonitor(PCMonitor):
    def __init__(self, conf_file, ):
        PCMonitor.__init__(self, conf_file)

    def set_up_module(self):
        for i in range(1, 5, 1):
            try:
                lock.acquire()
                self.driver = webdriver.Firefox()
                lock.release()
                time.sleep(2)
                self.driver.delete_all_cookies()
                time.sleep(5)
                break
            except Exception, e:
                logging.error(e)
                time.sleep(5)
                logging.error("webdriver.Remote except")
