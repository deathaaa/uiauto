#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

__author__ = 'litang.wang'

if len(sys.argv) > 1:
    file_list = sys.argv[1].split(',')
    ret = 0
    all_fail_str = ""
    url = ''
    for resfile in file_list:
        if os.path.exists(resfile):
            last_pay_frp = open(resfile, "rU")
            last_pay_ids = last_pay_frp.readlines()
            last_pay_frp.close()
            cur_fail_str = ""
            for line in last_pay_ids:
                line = line.strip('\n')
                if not line.find('fail') == -1:
                    cur_fail_str = cur_fail_str + " " + line
                    ret = 1
                elif 'result_url' in line:
                    url = ' more info:' + line.split('result_url=')[1]
        else:
            cur_fail_str = resfile + " have no exist"
            ret = 2
        if cur_fail_str != "":
            all_fail_str = all_fail_str + cur_fail_str
            break

    if all_fail_str != "":
        print all_fail_str + url + "\n"
        exit(ret)
    else:
        print 'all run success'
        exit(0)
else:
    print 'please input file_path'
    exit(2)
