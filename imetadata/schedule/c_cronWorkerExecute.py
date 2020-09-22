# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 14:01 
# @Author : 王西亚 
# @File : c_cronWorkerExecute.py


from multiprocessing import Event

from imetadata.schedule.execute.c_cronScheduleExecute import CCronScheduleExecute


class CCronWorkerExecute(CCronScheduleExecute):
    __stop_event__: Event = None

    def __init__(self, schedule_id, schedule_trigger, schedule_algorithm, schedule_params, stop_event: Event):
        super().__init__(schedule_id, schedule_trigger, schedule_algorithm, schedule_params)
        self.__stop_event__ = stop_event

    def should_stop(self) -> bool:
        """
        如果事件被设置，则终止
        """
        return self.__stop_event__.is_set()
