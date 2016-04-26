# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import traceback

from uiauto.util.config_reader import ConfigReader
from uiauto.util.config_writer import ConfigWriter
from uiauto.util.upload_file import UploadFile

__author__ = 'litang.wang'


class BaseMonitor():
    def __init__(self, config):

        self.driver = None
        self.config = config

        self.conf_file = config.conf_file
        self.config_writer = ConfigWriter(self.conf_file)
        self.config_reader = ConfigReader(self.conf_file)

        self.all_ret = 0
        self.screen_shots = []
        self.msgs = []
        self.result = []
        self.status_dict = {0: 'success', -1: 'fail', 255: 'except'}
        self.error_msg = ''

    def get_pic(self, case_name=""):
        pic_path = self.config.pic_path
        time_str = time.strftime('_%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = case_name + time_str + ".jpg"
        file_path = pic_path + os.sep + file_name
        self.screen_shots.append(file_name)
        try:
            self.driver.get_screenshot_as_file(file_path)
            UploadFile.upload_backgroud(file_path, file_name, 'img')
            logging.info(file_path)
        except Exception, e:
            logging.error('get pic except')
            logging.error(e)

    def print_error_lines(self):
        try:
            tb = sys.exc_info()[2]
            extract_tbs = traceback.extract_tb(tb)
            msg = ''
            for i in range(1, len(extract_tbs)):
                extract_tb = extract_tbs[i]
                file_path = extract_tb[0]
                line_no = extract_tb[1]
                lines = open(file_path, 'r').readlines()
                lines_len = len(lines)
                msg += "\n%s \n %s %s %s %s>%s %s %s %s %s %s\n" % (
                    file_path,
                    (line_no - 2) if line_no - 3 >= 0 else '', lines[line_no - 3] if line_no - 3 >= 0 else '',
                    (line_no - 1) if line_no - 3 >= 0 else '', lines[line_no - 2] if line_no - 2 >= 0 else '',
                    line_no, lines[line_no - 1],
                    (line_no + 1) if line_no < lines_len else '', lines[line_no] if line_no < lines_len else '',
                    (line_no + 2) if line_no + 1 < lines_len else '',
                    lines[line_no + 1] if line_no + 1 < lines_len else ''
                )

            self.msgs.append(msg)
            logging.error(msg)
        except Exception, e:
            logging.error('get error line except')
            logging.error(e)
            # self.tear_down_module()
            # self.all_ret = 0
            # self.return_ret()

    def set_up_module(self):
        pass

    def tear_down_module(self):
        pass

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def run_case(self, case, param=None):
        ret = 0
        for i in range(0, int(self.config.retry), 1):
            self.set_up()
            try:
                if param:
                    ret = case(param)
                else:
                    ret = case()

                if ret == -1:
                    self.get_pic(case.__name__)
                self.tear_down()
                if ret == 0:
                    break
            except Exception, e:
                logging.error(e)
                self.print_error_lines()
                self.get_pic(case.__name__)
                self.tear_down()
                ret = -1
        return ret

    def run(self, case_queue):
        while True:
            case_list = case_queue.get_case_list(self)
            if not case_list:
                return
            for case in case_list:
                notes = case.__dict__
                owner = notes.get('owner', '')
                desc = notes.get('desc', '')
                case_name = case.__name__
                ignore = notes.get('ignore', False)
                datas = notes.get('datas', [None])
                begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if ignore:
                    logging.info('%s %s ignore' % (self.config.name, case_name))
                    self.result.append(
                            {'case_name': case_name, 'status': 'ignore', 'begin_time': begin_time,
                             'end_time': begin_time,
                             'owner': owner, 'desc': desc, 'screen_shots': [], 'msgs': []})
                    continue
                for data in datas:
                    if data:
                        case_name = data

                    logging.info('%s begin' % case_name)

                    ret = self.run_case(case, data)
                    status = self.status_dict[ret]
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    self.result.append(
                            {'case_name': case_name, 'status': status, 'begin_time': begin_time, 'end_time': end_time,
                             'owner': owner, 'desc': desc, 'screen_shots': self.screen_shots, 'msgs': self.msgs})
                    self.msgs = []
                    self.screen_shots = []
                    logging.info('%s %s' % (case_name, status))
                    if ret:
                        self.error_msg += '%s %s fail\n' % (self.config.name, case_name)
                        self.all_ret = -1
                        if self.config.fail_continue.lower() == 'false':
                            self.tear_down_module()
                            return
