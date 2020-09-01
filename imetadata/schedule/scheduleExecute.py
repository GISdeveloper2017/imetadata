# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 14:06 
# @Author : 王西亚 
# @File : scheduleExecute.py

from imetadata.schedule.scheduleBase import scheduleBase
from imetadata.schedule.scheduleExecuteBase import scheduleExecuteBase
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from imetadata.database.factory import Factory
from multiprocessing import Process, Semaphore, Queue, Lock, Event


class scheduleExecute(scheduleExecuteBase):
    __stop_event__: Event = None

    def __init__(self, schedule_id, schedule_algorithm, stop_event: Event):
        super().__init__(schedule_id, schedule_algorithm)
        self.__stop_event__ = stop_event
        self.__schedule_algorithm__ = schedule_algorithm

    def default_create_schedule(self, schedule_algorithm, *args, **kwargs) -> scheduleBase:
        return CObject.create_business_instance(CSys.get_business_dir(), 'imetadata.business', schedule_algorithm, args, kwargs)

    def stop(self) -> bool:
        """
        如果事件被设置，则终止
        """
        return self.__stop_event__.ev.is_set()
