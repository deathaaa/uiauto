#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib
from HTMLParser import HTMLParser

__author__ = 'litang.wang'


class MyHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)


def is_apk(link):
    if link.startswith('Qunar_Spider') and link.endswith('.apk'):
        return True


def get_links(url):
    content = urllib.urlopen(url).read()
    html_parser = MyHTMLParser()
    html_parser.feed(content)
    html_parser.close()
    links = html_parser.links
    return links


def get_beta_apk(url, file_path, auto):
    if auto:
        result = json.loads(urllib.urlopen(url).read())
        url = result[0]['download_link']
        content = urllib.urlopen(url).read()
    else:
        content = urllib.urlopen(url).read()
    f = open(file_path, 'wb')
    f.write(content)
    f.close()


if __name__ == '__main__':
    try:
        argv = sys.argv
        url = argv[1]
        file_path = argv[2]
        tag_type = 'r'
        if len(argv) >= 4:
            tag_type = argv[3]
        if tag_type == 'b':
            get_beta_apk(url, file_path)
            exit(0)
        if tag_type == 'c':
            get_beta_apk(url, file_path, False)
            exit(0)


        def is_rtag(link):
            return link.startswith('%s-' % tag_type)


        # url='http://l-yum1.cm.cn1.qunar.com/mobile_app/android/m_adr_spider_finn/tags/'
        # file_path='/Users/LT_Wong/Downloads/test.apk'
        if os.path.exists(file_path):
            mtime = time.strftime('%y%m%d%H%M%S', time.localtime(os.path.getmtime(file_path)))
        else:
            mtime = 0
        # 获得所有rtag并找到最后一个rtag的链接

        if tag_type == 'p':
            last_tag = url
            url = 'http://l-yum1.cm.cn1.qunar.com/mobile_app/android/m_adr_spider_finn/tags/'
        else:
            links = get_links(url)
            tags = filter(is_rtag, links)
            last_tag = max(tags)
        tag_times = last_tag.split('-')
        last_time = tag_times[1] + tag_times[2]
        print '%stag_time:%s,apk_last_modify_time:%s' % (tag_type, last_time, mtime)

        if last_time > mtime:  # rtag创建时间大于apk的修改时间
            # 获得最后一个rtag对应的apk链接
            url += last_tag
            links = get_links(url)
            apk = filter(is_apk, links)[0]
            # 下载最新apk
            url += apk
            content = urllib.urlopen(url).read()
            f = open(file_path, 'wb')
            f.write(content)
            f.close()
            print 'download the newest apk success'
        else:
            print'the apk is the newest'
    except Exception, e:
        print 'download the newest apk fail'
        print e
