# -*- coding: utf-8 -*-
import os
import re

__author__ = 'litang.wang'


class AndroidUtil:
    def __init__(self):
        pass

    @staticmethod
    def get_device_nums():
        device_nums = []
        lines = os.popen('adb devices').readlines()
        for line in lines:
            m = re.match('(.*)\tdevice\n', line)
            if m is not None:
                device_num = m.groups()[0]
                print device_num
                device_nums.append(device_num)
        if len(device_nums) == 0:
            print 'Not connected to the device'
        return device_nums
