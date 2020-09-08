# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 15:25 
# @Author : 王西亚 
# @File : c_intervalScheduleExecute.py

from imetadata.base.c_logger import CLogger
from imetadata.schedule.execute.c_timeScheduleExecute import CTimeScheduleExecute
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.base import BaseTrigger


class CTrigger(IntervalTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        next_fire_time = now + self.interval

        if self.jitter is not None:
            next_fire_time = self._apply_jitter(next_fire_time, self.jitter, now)

        if not self.end_date or next_fire_time <= self.end_date:
            return self.timezone.normalize(next_fire_time)


class CIntervalScheduleExecute(CTimeScheduleExecute):

    def get_or_create_trigger(self) -> BaseTrigger:
        seconds = super().params_value_by_name(self.TRIGGER_Interval_Params_Seconds, 5)
        CLogger().info(
            '调度{0}.{1}设置的定时间隔为{2}秒...'.format(self.__schedule_id__, self.__schedule_trigger__, seconds))
        return CTrigger(seconds=seconds)
