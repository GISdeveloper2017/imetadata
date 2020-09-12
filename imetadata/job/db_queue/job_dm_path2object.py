# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:31 
# @Author : 王西亚 
# @File : job_dm_path2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob
from imetadata.base.c_logger import CLogger


class job_dm_path2object(CDBQueueJob):
    def get_mission_seize_sql(self) -> str:
        pass

    def get_mission_info_sql(self) -> str:
        pass

    def get_abnormal_mission_restart_sql(self) -> str:
        pass

    def process_mission(self, dataset) -> str:
        pass


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path2object('', '').execute()
