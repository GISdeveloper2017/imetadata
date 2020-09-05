# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 15:17 
# @Author : 王西亚 
# @File : c_processUtils.py

from multiprocessing import Process


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


