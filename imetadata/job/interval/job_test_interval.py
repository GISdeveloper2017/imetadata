# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 18:35 
# @Author : 王西亚 
# @File : job_test_interval.py.py 

from __future__ import absolute_import

import time

from imetadata.base.c_result import CResult
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_test_interval(CTimeJob):
    def execute(self) -> str:
        time.sleep(10)
        return CResult.merge_result(CResult.Success, '任务执行成功结束！')
