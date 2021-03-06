#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52 
# @Author : 王西亚 
# @File : c_dbQueueScheduleExecute.py

import time

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.schedule.execute.c_scheduleExecute import CScheduleExecute
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDBQueueScheduleExecute(CScheduleExecute):
    __schedule__: CDBQueueJob = None

    def get_or_create_sch_job(self) -> CDBQueueJob:
        if self.__schedule__ is None:
            self.__schedule__ = super().default_create_sch_job(
                self.__schedule_trigger__,
                self.__schedule_algorithm__,
                self.__schedule_id__,
                self.__schedule_params__
            )

        return self.__schedule__

    def start(self):
        schedule = self.get_or_create_sch_job()
        if schedule is None:
            CLogger().warning(
                '无法创建Job对象: {0}.{1}.{2}'.format(
                    self.__schedule_id__,
                    self.__schedule_trigger__,
                    self.__schedule_algorithm__
                )
            )
            return

        schedule.before_execute()
        schedule.abnormal_mission_restart()
        while True:
            mission_process_result = schedule.execute()
            if not CResult.result_success(mission_process_result):
                time.sleep(5)

            if self.should_stop():
                break

        schedule.before_stop()
