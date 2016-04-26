# coding=utf-8
import ConfigParser

__author__ = 'litang.wang'


class ConfigWriter:
    def __init__(self, filename):
        self.filename = filename

    def write(self, option, value, section='release'):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        config.set(section, option, value.decode('GBK').encode('utf_8'))
        config.write(open(self.filename, "w"))
