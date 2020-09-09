# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 15:17 
# @Author : 王西亚 
# @File : c_processUtils.py

from multiprocessing import Process

from imetadata.base.c_json import CJson


class CProcess(Process):
    NAME_CMD_COMMAND = 'cmd_command'
    NAME_CMD_ID = 'cmd_id'
    NAME_CMD_TITLE = 'cmd_title'
    NAME_CMD_TRIGGER = 'cmd_trigger'
    NAME_CMD_ALGORITHM = 'cmd_algorithm'
    NAME_CMD_PARAMS = 'cmd_params'

    CMD_START = 'start'
    CMD_STOP = 'stop'
    CMD_FORCE_STOP = 'force_stop'

    NAME_PARAMS = 'params'
    NAME_STOP_EVENT = 'stop_event'
    NAME_SUBPROCESS_LIST = 'subprocess_list'
    Name_Parallel_Count = 'parallel_count'

    Name_Process = 'process'

    def params_value_by_name(self, params: str, attr_name: str, default_value):
        """
        通过解析传入参数, 直接获取任务执行方面的参数, 该参数都存储在job对象下
        :param attr_name:
        :param default_value:
        :return:
        """
        return CJson().json_attr_value(params, '{0}.{1}'.format(self.Name_Process, attr_name), default_value)
