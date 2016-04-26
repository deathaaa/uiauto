# -*- coding: utf-8 -*-
import inspect
import logging

__author__ = 'litang.wang'


class BaseCase:
    def __init__(self, monitor):
        self.driver = monitor.driver
        self.conf_file = monitor.conf_file
        self.config_writer = monitor.config_writer
        self.config_reader = monitor.config_reader
        self.driver.implicitly_wait(10)

    def find_element_by_id(self, param, attr='text'):
        element = self.driver.find_element_by_id(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_element_by_name(self, param, attr='text'):
        element = self.driver.find_element_by_name(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_element_by_tag_name(self, param, attr='text'):
        element = self.driver.find_element_by_tag_name(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_element_by_class_name(self, param, attr='text'):
        element = self.driver.find_element_by_class_name(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_element_by_css_selector(self, param, attr='text'):
        element = self.driver.find_element_by_css_selector(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_element_by_xpath(self, param, attr='text'):
        element = self.driver.find_element_by_xpath(param)
        if attr:
            self.get_element_attribute(element, param, attr)
        return element

    def find_elements_by_id(self, param):
        elements = self.driver.find_elements_by_id(param)
        return elements

    def find_elements_by_name(self, param):
        elements = self.driver.find_elements_by_name(param)
        return elements

    def find_elements_by_tag_name(self, param):
        elements = self.driver.find_elements_by_tag_name(param)
        return elements

    def find_elements_by_class_name(self, param):
        elements = self.driver.find_elements_by_class_name(param)
        return elements

    def find_elements_by_css_selector(self, param):
        elements = self.driver.find_elements_by_css_selector(param)
        return elements

    def find_elements_by_xpath(self, param):
        elements = self.driver.find_elements_by_xpath(param)
        return elements

    @staticmethod
    def get_element_attribute(element, param, attr='text'):

        if hasattr(element, attr):
            item = getattr(element, attr)
            logging.info('func: %s ,param:%s,%s:%s' % (inspect.stack()[1][3], param, attr, item))
            return item
