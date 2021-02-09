# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_job.py

from abc import abstractmethod

import settings
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils


class CJob(CResource):
    __id = None
    __mission_db_id = None
    __params = None
    __abnormal_job_retry_times = 0

    def __init__(self, job_id: str, job_params: str):
        self.__id = job_id
        self.__params = job_params
        self.__mission_db_id = CUtils.any_2_str(
            self.params_value_by_name(
                self.Job_Params_DB_Server_ID,
                self.DB_Server_ID_Default
            )
        )
        self.__abnormal_job_retry_times = self.params_value_by_name(
            self.Job_Params_Abnormal_Job_Retry_Times,
            -1
        )
        if CUtils.equal_ignore_case(self.__abnormal_job_retry_times, -1):
            self.__abnormal_job_retry_times = settings.application.xpath_one(
                self.Path_Setting_MetaData_InBound_Parser_MetaData_Retry_Times,
                self.Default_Abnormal_Job_Retry_Times
            )

        self.custom_init()

    def abnormal_job_retry_times(self) -> int:
        return self.__abnormal_job_retry_times

    def get_mission_db_id(self) -> str:
        return self.__mission_db_id

    def params_value_by_name(self, attr_name: str, default_value):
        """
        通过解析传入参数, 直接获取任务执行方面的参数, 该参数都存储在job对象下
        :param attr_name:
        :param default_value:
        :return:
        """
        if self.__params is None:
            return default_value
        else:
            return CJson.json_attr_value(self.__params, '{0}.{1}'.format(self.NAME_JOB, attr_name), default_value)

    @abstractmethod
    def execute(self) -> str:
        return CResult.merge_result(CResult.Failure, '没有可执行的任务！')

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
