# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:14 
# @Author : 王西亚 
# @File : c_scheduleExecute.py

from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from abc import abstractmethod


class CScheduleExecute:
    TRIGGER_TYPE_DB_QUEUE = 'db_queue'
    TRIGGER_TYPE_DATE = 'date'
    TRIGGER_TYPE_INTERVAL = 'interval'
    TRIGGER_TYPE_CRON = 'cron'
    TRIGGER_TYPE_QUEUE = 'queue'
    TRIGGER_TYPE_NONE = 'none'

    TRIGGER_Interval_Params_Interval = 'interval'

    __schedule_id__: str = None
    __schedule_trigger__: str = None
    __schedule_algorithm__: str = None
    __schedule_params__: str = None

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
        return CObject.create_business_instance(CSys.get_job_root_dir(), CSys.get_job_package_root_name(), schedule_trigger,
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
