#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52 
# @Author : 王西亚 
# @File : scheduleExecuteBase.py

from imetadata.schedule.scheduleBase import scheduleBase
from abc import abstractmethod
from imetadata.base.utils import MetaDataUtils
import time


class scheduleExecuteBase:
    __schedule_id__: str = None
    __schedule_algorithm__: str = None
    __schedule__: scheduleBase = None

    def __init__(self, schedule_id, schedule_algorithm):
        self.__schedule_id__ = schedule_id
        self.__schedule_algorithm__ = schedule_algorithm

    def get_or_create_schedule(self) -> scheduleBase:
        if self.__schedule__ is None:
            self.__schedule__ = self.default_create_schedule(self.__schedule_algorithm__, self.__schedule_id__)

        return self.__schedule__

    @abstractmethod
    def default_create_schedule(self, schedule_algorithm, *args, **kwargs) -> scheduleBase:
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
        schedule = self.get_or_create_schedule()
        if schedule is None:
            return

        schedule.before_execute()
        schedule.abnormal_mission_restart()
        while True:
            mission_process_result = schedule.execute()
            if not MetaDataUtils.result_success(mission_process_result):
                time.sleep(5)

            if self.stop():
                break

        schedule.before_stop()
