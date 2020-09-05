# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 18:35 
# @Author : 王西亚 
# @File : job_test_interval.py.py 

from __future__ import absolute_import
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.schedule.job.c_timeJob import CTimeJob
import time


class job_test_interval(CTimeJob):
    def execute(self) -> str:
        time.sleep(10)
        return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '任务执行成功结束！')
