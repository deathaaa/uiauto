# -*- coding: utf-8 -*-
import inspect
import thread

__author__ = 'litang.wang'

lock = thread.allocate_lock()


class CaseQueue:
    def __init__(self, case_list):
        self.queue = case_list
        self.run_log = {}

    def get_case_list(self, monitor):
        case_list = []
        lock.acquire()
        if len(self.queue) > 0:
            cases = self.queue.pop(0)
            case_object = cases.case_class(monitor)
            unbound_case_list = cases.prefix_case_list + cases.case_list
            if monitor in self.run_log.keys():
                run_log = self.run_log[monitor]
                unbound_case_list = filter(
                        lambda unbound_case: not (unbound_case in run_log and not unbound_case.repeatable),
                        unbound_case_list)
                self.run_log[monitor] += unbound_case_list
            else:
                self.run_log[monitor] = unbound_case_list
            case_names = map(lambda unbound_case: unbound_case.__name__, unbound_case_list)
            for case_name in case_names:
                case = inspect.getmembers(case_object,
                                          lambda o: inspect.ismethod(o) and o.__name__ == case_name)
                if len(case) > 0:
                    case = case[0][1]
                    case_list.append(case)

        else:
            case_list = None
        lock.release()
        return case_list
