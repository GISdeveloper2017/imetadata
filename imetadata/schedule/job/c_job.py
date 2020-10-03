# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_job.py

from abc import abstractmethod

from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult


class CJob(CResource):
    __id__: str = None
    __params__: str = None

    def __init__(self, job_id: str, job_params: str):
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
