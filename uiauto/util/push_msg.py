# -*- coding:utf-8 -*-

import json
import logging
from urllib2 import (
    Request,
    urlopen,
    URLError
)


class PushMsg:
    def __init__(self):
        pass

    @staticmethod
    def send_msg_by_url(title, content, content_url, request_url, msg_receiver):
        params = {
            "providerUserName": "des_auto_test",
            "passWord": "123456",
            "msgCatName": "des_auto_test",
            "title": title,
            "content": content,
            "receiverName": msg_receiver,
            "receiverType": "user",
            "tag": "tag",
            "level": 1,
            "url": content_url}
        params = json.dumps(params)

        request = Request(request_url, params)
        request.add_header('Content-Type', 'application/json')

        try:
            response = urlopen(request)
            res = response.read()
            result = json.loads(res)
            if result.get("ret"):
                logging.info('send msg success')
            else:
                logging.error('send msg fail')
        except URLError as _ex:
            if hasattr(_ex, "reason"):
                logging.error("push message to app failed, reasion: %s" % str(_ex))
                return 'send msg success'
            elif hasattr(_ex, "code"):
                logging.error("the server cann't not fulfil the request, err code : %s" % str(_ex))
                return 'send msg fail'

    def send_msg_to_app(self, title, content, content_url, msg_receiver):
        if msg_receiver == '' or msg_receiver is None:
            return
        android_url = "http://ps.corp.qunar.com/pushservice/api/ps/pushMsg.qunar"
        ios_url = "http://pn.qunar.com/pushservice/api/ps/pushMsg.qunar"
        urls = [android_url, ios_url]
        for url in urls:
            self.send_msg_by_url(title, content, content_url, url, msg_receiver)
