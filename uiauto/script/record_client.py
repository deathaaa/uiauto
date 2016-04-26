#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import rpyc

__author__ = 'litang.wang'

if __name__ == '__main__':
    args = sys.argv
    print args
    conn = rpyc.connect('10.86.50.200', 9999)
    cResult = conn.root.record(testType=args[1], business=args[2], url_str=args[3], build_num=args[4],
                               branchName=args[5])
    # conn =rpyc.connect('127.0.0.1',9999)
    # cResult =conn.root.test(111)
    conn.close()

    print cResult
