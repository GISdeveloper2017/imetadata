# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_job.py
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
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

    NAME_JOB = 'job'

    CMD_START = 'start'
    CMD_STOP = 'stop'

    Job_Params_DB_Server_ID = 'db_server_id'

    __id__: str = None
    __params__ = None

    def __init__(self, job_id: str, job_params):
        self.__id__ = job_id
        self.__params__ = job_params
        self.custom_init()

    def params_value_by_name(self, attr_name: str, default_value):
        """
        通过解析传入参数, 直接获取任务执行方面的参数, 该参数都存储在job对象下
        :param attr_name:
        :param default_value:
        :return:
        """
        if self.__params__ is None:
            return default_value
        else:
            return CJson().json_attr_value(self.__params__, '{0}.{1}'.format(self.NAME_JOB, attr_name), default_value)

    @abstractmethod
    def execute(self) -> str:
        return CMetaDataUtils.merge_result(CMetaDataUtils.Failure, '没有可执行的任务！')

    def before_execute(self):
        pass

    def before_stop(self):
        pass

    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        pass
