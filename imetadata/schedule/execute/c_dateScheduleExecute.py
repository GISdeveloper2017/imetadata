# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 15:31 
# @Author : 王西亚 
# @File : c_dateScheduleExecute.py

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.date import DateTrigger

from imetadata.schedule.execute.c_timeScheduleExecute import CTimeScheduleExecute


class CDateScheduleExecute(CTimeScheduleExecute):

    def get_or_create_trigger(self) -> BaseTrigger:
        return DateTrigger()
