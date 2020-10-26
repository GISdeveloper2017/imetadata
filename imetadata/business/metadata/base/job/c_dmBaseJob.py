# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDMBaseJob(CDBQueueJob):
    Path_MD_Bus_Root = '/root'
    Path_MD_Bus_ProductType = '{0}/ProductType'.format(Path_MD_Bus_Root)
