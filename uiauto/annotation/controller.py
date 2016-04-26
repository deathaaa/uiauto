# -*- coding: utf-8 -*-
import copy
import inspect
import logging
import os
import sys
import threading

from uiauto.lib.case_queue import CaseQueue
from uiauto.lib.platform import PLATFORM
from uiauto.module.case_type import CaseType
from uiauto.module.cases import Cases
from uiauto.module.monitor_relation import monitor_relation, Relation
from uiauto.util.android_util import AndroidUtil
from uiauto.util.config_util import ConfigUtil
from uiauto.util.return_result import return_ret

__author__ = 'litang.wang'

over = threading.Event()


def controller(case_classes, conf='', platform='', tag=None, monitor_class=None, config_class=None):
    def __is_case(case):
        if inspect.ismethod(case):
            params = case.__dict__
            case_type = params.get('type', '')
            if case_type == 'case' or case_type == 'data_case':
                return True
            else:
                return False
        else:
            return False

    def __is_prefix_case(case):
        return __is_case(case) and case.__dict__.get('prefix', False)

    def __is_not_prefix_case(case):
        return __is_case(case) and not case.__dict__.get('prefix', False)

    def __is_same_tag(case):
        case_tag = case.__dict__.get('tag', None)
        if tag is None:
            return True
        elif ((isinstance(tag, int) or isinstance(tag, str)) and tag == case_tag) or (
                    isinstance(tag, list) and case_tag in tag):
            return True
        else:
            return False

    def __check_param():
        os.system('upgrade.py %s' % conf)  # upgrade
        if not os.path.exists(conf):
            raise Exception('path [%s] is not exist' % conf)
        if platform not in PLATFORM.__dict__.values():
            raise Exception('platform [%s] is undefined' % platform)

    def __init(config):
        if platform == PLATFORM.ANDROID:
            if sys.platform == 'darwin' or sys.platform == 'linux2':
                os.system('android_prepare.sh')
            else:
                os.system('android_prepare.bat')

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=config.log,
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def __get_case_list():
        case_list = []

        for item in case_classes:
            orderly_case_list = []
            # 如果传入的case_class是一个字典
            if isinstance(item, dict):
                for (case_class, cases) in item.items():  # 遍历字典
                    case_list.append(Cases(case_class, cases, [], CaseType.CUSTOM))
            else:
                case_class = item
                prefix_cases = inspect.getmembers(case_class, __is_prefix_case)
                prefix_list = []
                for prefix_case in prefix_cases:
                    prefix_list.append(prefix_case[1])
                prefix_list = filter(__is_same_tag, prefix_list)
                case_dict = {}
                for case in inspect.getmembers(case_class,
                                               __is_not_prefix_case):  # 遍历case类中的case，并按优先级排序成字典，key为优先级，value为case列表
                    case = case[1]
                    attrs = case.__dict__
                    priority = int(attrs.get('priority', -1))
                    if priority in case_dict:
                        case_dict.get(priority).append(case)
                    else:
                        case_dict[priority] = [case]
                for i in case_dict.keys():  # 把按优先级构造好的字典构造成case的list
                    if i != -1:
                        orderly_case_list += case_dict[i]

                orderly_case_list = filter(__is_same_tag, orderly_case_list)
                if len(orderly_case_list) > 0:
                    case_list.append(Cases(case_class, orderly_case_list, prefix_list, CaseType.ORDERLY))
                normal_case_list = filter(__is_same_tag, case_dict.get(-1, []))
                if len(normal_case_list) > 0:
                    for case in normal_case_list:
                        case_list.append(Cases(case_class, [case], prefix_list, CaseType.NORMAL))

        return case_list

    def __get_monitor_list(monitor_class, config, thread_count):
        monitor_list = []
        if platform == PLATFORM.ANDROID:
            server_port = 4749
            bootstrap_port = 4750
            device_nums = AndroidUtil.get_device_nums()
            for device_num in device_nums:
                copy_config = copy.deepcopy(config)

                copy_config.device_num = device_num
                copy_config.server_port = str(server_port)
                copy_config.bootstrap_port = str(bootstrap_port)
                monitor = monitor_class(copy_config)
                monitor_list.append(monitor)

                server_port -= 1
                bootstrap_port += 1
        elif platform == PLATFORM.IOS:
            monitor_list = [monitor_class(config)]
        else:
            for i in range(0, thread_count):
                monitor_list.append(monitor_class(config))

        return monitor_list

    def __run(monitor, case_queue):
        try:
            monitor.set_up_module()
        except:
            over.set()
            return
        monitor.run(case_queue)
        monitor.tear_down_module()
        over.set()

    def __get_relation():
        if platform == PLATFORM.CUSTOM:
            return Relation(monitor_class, config_class)
        else:
            return monitor_relation[platform]

    def _control(func):
        __check_param()
        relation = __get_relation()
        monitor_class = relation.monitor_class
        config = ConfigUtil.get_config(conf, relation.config_class)
        __init(config)
        thread_count = int(getattr(config, 'thread_count', 1))

        case_queue = CaseQueue(__get_case_list())
        monitor_list = __get_monitor_list(monitor_class, config, thread_count)

        thread_list = []
        for i in range(0, thread_count):
            thread_list.append(threading.Thread(target=__run, args=(monitor_list[i], case_queue)))
        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()

        def __is_over():

            for monitor in monitor_list:
                if monitor.all_ret != 0:
                    return True
            for thread in thread_list:
                if thread.isAlive():
                    return False
            return True

        for i in range(0, len(thread_list)):
            over.wait()
            if __is_over():
                break
            else:
                over.clear()

        result_list = []
        error_msg = ''
        all_ret = 0
        for monitor in monitor_list:
            result_list += monitor.result
            if monitor.all_ret != 0:
                error_msg += monitor.error_msg
                all_ret = -1

        result_list = sorted(result_list, key=lambda result: result['begin_time'])
        return_ret(config, result_list, error_msg, all_ret)
        return func

    return _control
