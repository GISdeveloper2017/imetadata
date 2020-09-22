# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 15:28 
# @Author : 王西亚 
# @File : c_timeScheduleExecute.py

import time
from abc import abstractmethod

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger

from imetadata.base.c_logger import CLogger
from imetadata.schedule.execute.c_scheduleExecute import CScheduleExecute
from imetadata.schedule.job.c_timeJob import CTimeJob


class CTimeScheduleExecute(CScheduleExecute):
    __schedule__ = None

    __cron_scheduler__: BackgroundScheduler
    __cron_job__: Job

    @abstractmethod
    def get_or_create_trigger(self) -> BaseTrigger:
        return None

    def get_or_create_sch_job(self) -> CTimeJob:
        if self.__schedule__ is None:
            self.__schedule__ = super().default_create_sch_job(self.__schedule_trigger__,
                                                               self.__schedule_algorithm__,
                                                               self.__schedule_id__,
                                                               self.__schedule_params__)

        return self.__schedule__

    def process_job(self):
        schedule = self.get_or_create_sch_job()
        if schedule is None:
            return
        if self.__cron_job__ is not None:
            self.__cron_job__.pause()
        try:
            CLogger().debug('{0} 定时任务开始启动...'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

            schedule.execute()

            CLogger().debug('{0} 定时任务处理完成...'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        finally:
            if self.should_stop():
                self.stop()
            else:
                if self.__cron_job__ is not None:
                    self.__cron_job__.resume()

    def start(self):
        schedule = self.get_or_create_sch_job()
        if schedule is None:
            return

        schedule.before_execute()

        job_stores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=5)
        }
        job_defaults = {
            'coalesce': True,
            'max_instances': 1,
            'misfire_grace_time': 60
        }

        self.__cron_scheduler__ = BackgroundScheduler(jobstores=job_stores, executors=executors,
                                                      job_defaults=job_defaults, daemonic=False)
        self.__cron_job__ = self.__cron_scheduler__.add_job(self.process_job, trigger=self.get_or_create_trigger(),
                                                            replace_existing=True)
        self.__cron_scheduler__.start()

        while True:
            time.sleep(5)
            if self.should_stop():
                try:
                    self.stop()
                finally:
                    return

    def stop(self):
        if self.__schedule__ is not None:
            self.__schedule__.before_stop()
            CLogger().info('调度即将结束')

        if self.__cron_job__ is not None:
            new_job = self.__cron_job__
            self.__cron_job__ = None
            new_job.remove()
            CLogger().info('调度Job已经移除...')

        if self.__cron_scheduler__ is not None:
            self.__cron_scheduler__.shutdown()
            self.__cron_scheduler__ = None
            CLogger().info('调度器已经停止...')
