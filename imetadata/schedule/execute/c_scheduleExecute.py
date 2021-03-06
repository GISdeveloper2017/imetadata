# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_scheduleExecute.py
from abc import abstractmethod

from imetadata.base.c_json import CJson
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys


class CScheduleExecute(CResource):
    __schedule_id__: str = None
    __schedule_trigger__: str = None
    __schedule_algorithm__: str = None
    __schedule_params__ = None

    def __init__(self, schedule_id, schedule_trigger, schedule_algorithm, schedule_params=None):
        self.__schedule_id__ = schedule_id
        self.__schedule_trigger__ = schedule_trigger
        self.__schedule_algorithm__ = schedule_algorithm
        self.__schedule_params__ = schedule_params

    def default_create_sch_job(self, schedule_trigger, schedule_algorithm, *args, **kwargs):
        """
        默认创建调度的方法
        :param schedule_trigger:
        :param schedule_algorithm:
        :param args:
        :param kwargs:
        :return:
        """
        return CObject.create_job_instance(CSys.get_job_root_dir(), CSys.get_job_package_root_name(), schedule_trigger,
                                           schedule_algorithm, args, kwargs)

    def should_stop(self) -> bool:
        """
         检验是否需要终止处理过程
         :return:
         """
        return False

    @abstractmethod
    def start(self):
        pass

    def params_value_by_name(self, attr_name: str, default_value):
        """
        通过解析传入参数, 直接获取任务执行方面的参数, 该参数都存储在trigger对象下
        :param attr_name:
        :param default_value:
        :return:
        """
        return CJson().json_attr_value(self.__schedule_params__, '{0}.{1}'.format(self.TRIGGER_Params, attr_name),
                                       default_value)
