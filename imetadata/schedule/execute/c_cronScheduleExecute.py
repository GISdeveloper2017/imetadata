# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:10 
# @Author : 王西亚 
# @File : c_cronScheduleExecute.py

from imetadata.base.c_logger import CLogger
from imetadata.schedule.execute.c_timeScheduleExecute import CTimeScheduleExecute
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.base import BaseTrigger


class CCronScheduleExecute(CTimeScheduleExecute):

    def get_or_create_trigger(self) -> BaseTrigger:
        return CronTrigger()
