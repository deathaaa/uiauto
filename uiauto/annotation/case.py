# coding=utf-8
__author__ = 'litang.wang'


def case(owner='', desc='', ignore=False, priority=-1, tag=None, prefix=False, repeatable=True):
    def _case(func):
        func.owner = owner
        func.desc = desc
        func.priority = priority
        func.ignore = ignore
        func.tag = tag
        func.prefix = prefix
        func.repeatable = repeatable
        func.type = 'case'
        return func

    return _case


def data_case(datas, owner='', desc='', ignore=False, priority=-1, tag=None, prefix=False, repeatable=True):
    def _data_case(func):
        func.datas = datas
        func.owner = owner
        func.desc = desc
        func.priority = priority
        func.ignore = ignore
        func.tag = tag
        func.prefix = prefix
        func.repeatable = repeatable
        func.type = 'data_case'
        return func

    return _data_case
