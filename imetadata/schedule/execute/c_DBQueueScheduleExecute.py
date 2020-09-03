#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52 
# @Author : 王西亚 
# @File : c_DBQueueScheduleExecute.py

from imetadata.schedule.type.c_DBQueueSchedule import CDBQueueSchedule
from abc import abstractmethod
from imetadata.base.c_utils import CMetaDataUtils
import time


class CDBQueueScheduleExecute:
    TRIGGER_TYPE_DB_QUEUE = 'db_queue'
    TRIGGER_TYPE_CRON = 'cron'
    TRIGGER_TYPE_QUEUE = 'queue'
    TRIGGER_TYPE_NONE = 'none'

    __schedule_id__: str = None
    __schedule_trigger__: str = None
    __schedule_algorithm__: str = None
    __schedule__: CDBQueueSchedule = None

    def __init__(self, schedule_id, schedule_trigger, schedule_algorithm):
        self.__schedule_id__ = schedule_id
        self.__schedule_algorithm__ = schedule_algorithm
        self.__schedule_trigger__ = schedule_trigger

    def get_or_create_sch_mission(self) -> CDBQueueSchedule:
        if self.__schedule__ is None:
            self.__schedule__ = self.default_create_sch_mission(self.__schedule_algorithm__, self.__schedule_id__)

        return self.__schedule__

    @abstractmethod
    def default_create_sch_mission(self, schedule_algorithm, *args, **kwargs) -> CDBQueueSchedule:
        """
        默认创建调度的方法
        :param schedule_algorithm:
        :param args:
        :param kwargs:
        :return:
        """
        return None

    @abstractmethod
    def stop(self) -> bool:
        """
         检验是否需要终止处理过程
         :return:
         """
        return False

    def start(self):
        schedule = self.get_or_create_sch_mission()
        if schedule is None:
            return

        schedule.before_execute()
        schedule.abnormal_mission_restart()
        while True:
            mission_process_result = schedule.execute()
            if not CMetaDataUtils.result_success(mission_process_result):
                time.sleep(5)

            if self.stop():
                break

        schedule.before_stop()
