# coding=utf-8
import ConfigParser
import codecs

__author__ = 'litang.wang'


class ConfigReader:
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.ConfigParser()

    def read_chinese(self, option, section='release', default=None):
        self.config.readfp(codecs.open(self.filename, "r", "utf-8-sig"))
        if self.config.has_option(section, option):
            default = self.config.get(section, option)
        elif default is not None:
            pass
        else:
            raise Exception('section [%s] has not option [%s]' % (section, option))
        return default

    def read(self, option, section='release', default=None):
        self.config.read(self.filename)
        if self.config.has_option(section, option):
            default = self.config.get(section, option)
        elif default is not None:
            pass
        else:
            raise Exception('section [%s] has not option [%s]' % (section, option))
        return default

    def items(self, section):
        self.config.read(self.filename)
        return self.config.items(section)
