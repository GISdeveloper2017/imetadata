#!/usr/bin/python3
# -*- coding:utf-8 -*-


# 定义一个常量类实现常量的功能
#
# 该类定义了一个方法__setattr()__,和一个异常ConstError, ConstError类继承
# 自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典
# 中。如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
# 最后两行代码的作用是把const类注册到sys.modules这个全局字典中。


class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


const = _const()
const.NAME_CMD_COMMAND = 'cmd_command'
const.NAME_CMD_ID = 'cmd_id'
const.NAME_CMD_TITLE = 'cmd_title'
const.NAME_CMD_TRIGGER = 'cmd_trigger'
const.NAME_CMD_ALGORITHM = 'cmd_algorithm'
const.NAME_CMD_PARALLEL_COUNT = 'cmd_parallel_count'

const.CMD_START = 'start'
const.CMD_STOP = 'stop'

const.NAME_PARAMS = 'params'
const.NAME_STOP_EVENT = 'stop_event'
const.NAME_SUBPROCESS_LIST = 'subprocess_list'
