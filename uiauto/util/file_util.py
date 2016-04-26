# coding=utf-8
import os
import shutil

from uiauto.util.pyh import *

__author__ = 'litang.wang'


class FileUtil:
    @staticmethod
    def change_encoding(src_path, dest_path, src_encode="UTF-8", dest_encode="GBK"):
        src_file = open(src_path, 'r+')
        dest_file = open(dest_path, 'w')
        try:
            for line in src_file:
                new_line = line.decode(src_encode).encode(dest_encode)
                dest_file.write(new_line)
        finally:
            src_file.close()
            dest_file.close()

    @staticmethod
    def append_file(src_path, dest_path):
        src_file = open(src_path, 'r+')
        dest_file = open(dest_path, 'a')
        try:
            for line in src_file:
                dest_file.write(line)
        finally:
            src_file.close()
            dest_file.close()

    @staticmethod
    def copy_file(src_path, dest_path):
        shutil.copy(src_path, dest_path)

    @staticmethod
    def clear_file(file_path):
        file(file_path, 'r+').truncate()

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def json_to_report(result, dest_path, log_name):
        print dest_path

        page = PyH("autotest report")

        table1 = page << table(border='1', id='mytable', cellpadding="8")

        tr1 = table1 << tr(id="header")

        for field in ['名称', '开始时间', '结束时间', '状态', '负责人', '说明', '截图', '日志']:
            tr1 << th(field)

        for row in result:
            tr2 = table1 << tr()
            screen_shot = row['screen_shots']
            msgs = row['msgs']
            screen_shot_len = len(screen_shot)
            msgs_len = len(msgs)
            tr2 << td(row['case_name'], rowspan=max(screen_shot_len, msgs_len))
            tr2 << td(row['begin_time'], rowspan=max(screen_shot_len, msgs_len))
            tr2 << td(row['end_time'], rowspan=max(screen_shot_len, msgs_len))
            tr2 << td(row['status'], rowspan=max(screen_shot_len, msgs_len))
            tr2 << td(row['owner'], rowspan=max(screen_shot_len, msgs_len))
            tr2 << td(row['desc'], rowspan=max(screen_shot_len, msgs_len))

            tr2 << td() << img(src='http://uiauto.beta.qunar.com/request/pic?src=' + screen_shot[0], height='100',
                               width='100') if screen_shot_len > 0 else tr2 << td()
            tr2 << td() << pre(msgs[0]) if msgs_len > 0 else tr2 << td()
            for i in range(1, max(len(msgs), len(screen_shot)), 1):
                tr3 = table1 << tr()
                tr3 << td() << img(src='http://uiauto.beta.qunar.com/request/pic?src=' + screen_shot[i], height='100',
                                   width='100') if screen_shot_len > i else tr3 << td()
                tr3 << td() << pre(msgs[i]) if msgs_len > i else tr3 << td()

        page << a('点击在浏览器中查看', href='http://uiauto.beta.qunar.com/request/html?src=' + dest_path.split(os.sep)[-1])
        page << a('查看日志', href='http://uiauto.beta.qunar.com/request/file?src=' + log_name)
        page.printOut(dest_path)

    @staticmethod
    def list_to_report(dest_path, title_list, key_list, data_list):
        print dest_path

        page = PyH("autotest report")

        table1 = page << table(border='1', id='mytable', cellpadding="8")

        tr1 = table1 << tr(id="header")

        for field in title_list:
            tr1 << th(field)

        for row in data_list:
            tr2 = table1 << tr()
            for key in key_list:
                tr2 << td(row[key])
        page.printOut()

    @staticmethod
    def json_to_file(result, dest_path, result_url):
        def _filter_fail_result(data):
            if data.get('status') == 'fail':
                return True
            else:
                return False

        f = file(dest_path, 'w')
        fail_results = filter(_filter_fail_result, result)
        if len(fail_results) > 0:
            fail_result = fail_results[0]
            f.write('%s %s fail\nresult_url= %s' % (fail_result['begin_time'], fail_result['case_name'], result_url))
        else:
            f.write('')
        f.flush()

        f.close()


if __name__ == '__main__':
    FileUtil.list_to_report('', ['a', 'b'], ['a', 'b'], [{'a': 1, 'b': '2'}, {'a': 3, 'b': 4}])
