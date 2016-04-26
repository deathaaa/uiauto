# -*- coding: utf-8 -*-
import logging
import smtplib
import urllib
from email.mime.text import MIMEText

__author__ = 'litang.wang'


class SendMail:
    def __init__(self, sender):
        self.sender = sender
        self.server = 'mta3.corp.qunar.com'

    def send_html(self, title, filename, mail_receiver, priority='3'):
        if mail_receiver == '' or mail_receiver is None:
            return
        try:
            msg = MIMEText(file(filename, 'r').read(), _subtype='html', _charset='utf-8')

            msg['X-Priority'] = priority
            mailto = mail_receiver.split(",")
            msg['Subject'] = title
            msg['to'] = ",".join(mailto)
            msg['From'] = self.sender

            # smtp = smtplib.SMTP('mail.qunar.com')
            smtp = smtplib.SMTP(self.server)
            smtp.sendmail(self.sender, mailto, msg.as_string())
            smtp.quit()
            print 'send mail success title:%s mail_receiver:%s' % (title, mail_receiver)
        except smtplib.SMTPException, e:
            logging.error("send mail error...%d: %s" % (e.args[0], e.args[1]))

    @staticmethod
    def send_mail(title, url, mail_receiver, status='success', jira=''):
        env = 'prod'
        if 'online' in title:
            env = 'prod'
        elif 'beta' in title:
            env = 'beta'

        if 'android' in title:
            client = 'android'
        elif 'ios' in title:
            client = 'ios'
        elif 'touch' in title:
            client = 'touch'
        elif 'pc' in 'title':
            client = 'pc'
        else:
            client = 'other'

        if 'movie' in title:
            business = 'movie'
        elif 'tuan' in title:
            business = 'tuan'
        else:
            business = 'other'

        param = {
            'title': title,
            'type': 'ui',
            'user': 'timer',
            'status': status,
            'env': env,
            'receiver': mail_receiver,
            'url': url,
            'clientType': client,
            'business': business,
            'jira': jira
        }
        print 'send mail param:%s' % param
        result = urllib.urlopen('http://desqa.beta.qunar.com/mail/send.do', urllib.urlencode(param))
        print result.read()


if __name__ == '__main__':
    send = SendMail('des-autotest@qunar.com')
    # send.send_html('test','/Users/LT_Wong/project/uiauto/online_tuan_pc/report/online_tuan_pc20150608121405.html','krystal.guo@qunar.com,litang.wang@qunar.com')
    send.send_mail('beta_test', 'http://uiauto.beta.qunar.com/request/html?src=online_tuan_android20150806180032.html',
                   'litang.wang@qunar.com,zmin.zhang@qunar.com,baiwei.ji@qunar.com')
