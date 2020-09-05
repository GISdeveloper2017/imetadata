# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_job.py

from imetadata.base.c_utils import CMetaDataUtils
from abc import abstractmethod


class CJob:
    SYSTEM_NAME_MISSION_ID = '{system.mission.id}'
    NAME_CMD_COMMAND = 'cmd_command'
    NAME_CMD_ID = 'cmd_id'
    NAME_CMD_TITLE = 'cmd_title'
    NAME_CMD_TRIGGER = 'cmd_trigger'
    NAME_CMD_ALGORITHM = 'cmd_algorithm'
    NAME_CMD_PARAMS = 'cmd_params'

    CMD_START = 'start'
    CMD_STOP = 'stop'

    __id__: str = None
    __params__: str = None

    def __init__(self, job_id: str, job_params: str):
        self.__id__ = job_id
        self.__params__ = job_params

    @abstractmethod
    def execute(self) -> str:
        return CMetaDataUtils.merge_result(CMetaDataUtils.Failure, '没有可执行的任务！')

    def before_execute(self):
        pass

    def before_stop(self):
        pass
