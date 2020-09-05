# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 09:50 
# @Author : 王西亚 
# @File : test_schedule.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.base import BaseTrigger
from apscheduler.job import Job
import time
import os
import datetime


class CTrigger(IntervalTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        next_fire_time = now + self.interval

        if self.jitter is not None:
            next_fire_time = self._apply_jitter(next_fire_time, self.jitter, now)

        if not self.end_date or next_fire_time <= self.end_date:
            return self.timezone.normalize(next_fire_time)


class CAbc:
    scheduler: BackgroundScheduler
    job: Job

    def __init__(self, str):
        self.__str__ = str

    def tick(self):
        if self.job is not None:
            self.job.pause()
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            print("{0} working ...".format(self.__str__))
            time.sleep(10)
            print("{0} work finished".format(self.__str__))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        finally:
            if self.job is not None:
                self.job.resume()

    def start(self):
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

        self.scheduler = BackgroundScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults,
                                        daemonic=False)
        self.job = self.scheduler.add_job(self.tick, trigger=CTrigger(seconds=7), replace_existing=True)
        self.scheduler.start()  # 这里的调度任务是独立的一个线程
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    def stop(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S stop', time.localtime(time.time())))
        if self.job is not None:
            new_job = self.job
            self.job = None
            new_job.remove()

        self.scheduler.shutdown(5)


if __name__ == '__main__':
    abc = CAbc('wangxiya')
    abc.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        abc.stop()
    print('Exit The Job!')
