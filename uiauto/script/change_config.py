#!/usr/bin/env python
# coding=utf-8
import getopt
import sys

from uiauto.util.config_reader import ConfigReader
from uiauto.util.config_writer import ConfigWriter

__author__ = 'litang.wang'


def usage():
    print """
        Usage :
            -k, --key=       key
            -v, --value=     value
            -f, --file=      file
    """
    sys.exit()


def get_opt():
    try:
        options, args = getopt.getopt(sys.argv[1:], "k:v:f:", ["key=", "value=", "file="])
        opt = {}
        for option, arg in options:
            if option in ('-k', '--key'):
                opt['key'] = arg
            if option in ('-v', '--value'):
                opt['value'] = arg
            if option in ('-f', '--file'):
                opt['file'] = arg
        return opt['key'], opt['value'], opt['file']
    except:
        usage()


if __name__ == '__main__':
    option = get_opt()
    filename = option[2]
    config_writer = ConfigWriter(filename)
    config_reader = ConfigReader(filename)
    key = option[0]
    value = option[1]
    config_writer.write(key, value)
