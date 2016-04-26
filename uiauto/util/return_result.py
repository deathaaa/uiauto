# -*- coding: utf-8 -*-
import logging
import os
import time

from uiauto.util.file_util import FileUtil
from uiauto.util.push_msg import PushMsg
from uiauto.util.send_mail import SendMail
from uiauto.util.upload_file import UploadFile

__author__ = 'litang.wang'


def return_ret(config, result, error_msg, all_ret):
    print result
    status_dict = {0: 'success', -1: 'fail', 255: 'except'}
    status = status_dict[all_ret]
    logging.info('%s autotest %s' % (config.name, status))
    sendmail = SendMail(config.mail_sender)

    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    html_name = config.name + now + '.html'
    html_path = config.report_path + html_name

    result_url = 'http://uiauto.beta.qunar.com/request/html?src=' + html_name
    logging.info('result_url= %s' % result_url)
    if all_ret:
        mail_receiver = config.mailtolist_fail
        push_msg = PushMsg()
        push_msg.send_msg_to_app('%s autotest fail' % config.name, '%smore_info:%s' % (error_msg, result_url),
                                 result_url, config.msg_receiver)
    else:
        mail_receiver = config.mailtolist_succ

    log_name = config.log.split(os.sep)[-1].replace('.',
                                                    time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.')

    UploadFile.upload(config.log, log_name, 'file')
    FileUtil.json_to_report(result, html_path, log_name)
    UploadFile.upload(html_path, html_name, 'file')
    sendmail.send_mail(config.name + ' UI autotest ' + status, result_url, mail_receiver, status, config.jira)
    FileUtil.json_to_file(result, config.log_bak, result_url)
    FileUtil.copy_file(html_path, config.log + '.html')

    exit(all_ret)
