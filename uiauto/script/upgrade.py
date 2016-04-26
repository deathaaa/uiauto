#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from uiauto.util.upgrade_framework import UpgradeFramework

__author__ = 'litang.wang'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        UpgradeFramework.auto_upgrade(sys.argv[1])
    else:
        UpgradeFramework.upgrade(True)
