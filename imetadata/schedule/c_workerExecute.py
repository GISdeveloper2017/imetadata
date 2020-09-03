# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 14:06 
# @Author : 王西亚 
# @File : c_workerExecute.py

from imetadata.schedule.type.c_DBQueueSchedule import CDBQueueSchedule
from imetadata.schedule.execute.c_DBQueueScheduleExecute import CDBQueueScheduleExecute
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from multiprocessing import Event


class CWorkerExecute(CDBQueueScheduleExecute):
    __stop_event__: Event = None

    def __init__(self, schedule_id, schedule_algorithm, stop_event: Event):
        super().__init__(schedule_id, schedule_algorithm)
        self.__stop_event__ = stop_event
        self.__schedule_algorithm__ = schedule_algorithm

    def default_create_sch_mission(self, schedule_algorithm, *args, **kwargs) -> CDBQueueSchedule:
        return CObject.create_business_instance(CSys.get_business_dir(), 'imetadata.business', schedule_algorithm, args, kwargs)

    def stop(self) -> bool:
        """
        如果事件被设置，则终止
        """
        return self.__stop_event__.is_set()
