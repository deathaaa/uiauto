# -*- coding: utf-8 -*-
import os

__author__ = 'litang.wang'


class BaseConfig:
    def __init__(self):
        self.type = None
        self.root_path = ''

        self.fail_continue = 'False'
        self.retry = 3
        self.log = self.root_path + 'log' + os.sep + 'last.log'
        self.log_bak = self.root_path + 'log' + os.sep + 'last_bak.log'
        self.pic_path = self.root_path + 'pic' + os.sep
        self.report_path = self.root_path + 'report' + os.sep
        self.mail_sender = 'des-autotest@qunar.com'

        self.name = None
        self.msg_receiver = ''
        self.mailtolist_fail = ''
        self.mailtolist_succ = ''
        self.jira = ''
