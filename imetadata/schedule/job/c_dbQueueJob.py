#!/usr/bin/python3
# -*- coding:utf-8 -*-

from abc import abstractmethod

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_job import CJob


class CDBQueueJob(CJob):
    @abstractmethod
    def get_mission_seize_sql(self) -> str:
        """
        任务捕捉使用的sql
        :return:
        """
        return ''

    @abstractmethod
    def get_mission_info_sql(self) -> str:
        """
        任务领取的sql
        :return:
        """
        return ''

    @abstractmethod
    def get_abnormal_mission_restart_sql(self) -> str:
        """
        异常任务重启的sql
        :return:
        """
        return ''

    @abstractmethod
    def process_mission(self, dataset, is_retry_mission: bool) -> str:
        return CResult.merge_result(CResult.Success, '测试成功')

    def execute(self) -> str:
        mission_data_retry = False
        mission_data = self.get_mission_info()
        if mission_data.is_empty():
            mission_data_retry = True
            mission_data = self.get_retry_mission_info()
            if mission_data is None:
                return CResult.merge_result(CResult.Failure, '没有可执行的任务！')

        if not mission_data.is_empty():
            return self.process_mission(mission_data, mission_data_retry)
        else:
            return CResult.merge_result(CResult.Failure, '没有可执行的任务！')

    def get_mission_info(self):
        mission_flag = CUtils.one_id()
        mission_seize_sql = self.get_mission_seize_sql()
        mission_info_sql = self.get_mission_info_sql()

        if mission_seize_sql is None:
            return None
        if mission_info_sql is None:
            return None

        mission_seize_sql = mission_seize_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)
        mission_info_sql = mission_info_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)

        try:
            factory = CFactory()
            db = factory.give_me_db(self.get_mission_db_id())
            db.execute(mission_seize_sql)

            return db.one_row(mission_info_sql)
        except:
            CLogger().debug('任务抢占查询语句有误, 请修正! 详细错误信息为: {0}'.format(mission_seize_sql))
            return CDataSet()

    def abnormal_mission_restart(self):
        sql = self.get_abnormal_mission_restart_sql()
        if sql is not None:
            try:
                factory = CFactory()
                db = factory.give_me_db(self.get_mission_db_id())
                db.execute(sql)
            except:
                pass

    def get_retry_mission_info(self):
        """
        获取重试的任务
        :return:
        """
        mission_flag = CUtils.one_id()
        mission_seize_sql = self.get_mission_retry_sql()
        mission_info_sql = self.get_mission_info_sql()

        if CUtils.equal_ignore_case(mission_seize_sql, ''):
            return None
        if CUtils.equal_ignore_case(mission_info_sql, ''):
            return None

        mission_seize_sql = mission_seize_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)
        mission_info_sql = mission_info_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)

        try:
            factory = CFactory()
            db = factory.give_me_db(self.get_mission_db_id())
            db.execute(mission_seize_sql)

            return db.one_row(mission_info_sql)
        except:
            return CDataSet()

    def get_mission_retry_sql(self) -> str:
        return ''
