# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 08:10 
# @Author : 王西亚 
# @File : c_cronScheduleExecute.py

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from imetadata.schedule.execute.c_timeScheduleExecute import CTimeScheduleExecute


class CCronScheduleExecute(CTimeScheduleExecute):

    def get_or_create_trigger(self) -> BaseTrigger:
        return CronTrigger()
