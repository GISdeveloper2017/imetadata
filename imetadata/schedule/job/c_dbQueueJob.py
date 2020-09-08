#!/usr/bin/python3
# -*- coding:utf-8 -*-

from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.c_factory import CFactory
from imetadata.base.core.Exceptions import *
from abc import abstractmethod
from imetadata.schedule.job.c_job import CJob


class CDBQueueJob(CJob):
    __mission_db_id__: str

    def custom_init(self):
        super().custom_init()
        self.__mission_db_id__ = super().params_value_by_name(self.Job_Params_DB_Server_ID, '0')

    def get_mission_db_id(self) -> str:
        return self.__mission_db_id__

    @abstractmethod
    def get_mission_seize_sql(self) -> str:
        return None

    @abstractmethod
    def get_mission_info_sql(self) -> str:
        return None

    @abstractmethod
    def get_abnormal_mission_restart_sql(self) -> str:
        return None

    @abstractmethod
    def process_mission(self, dataset) -> str:
        return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '测试成功')

    def execute(self) -> str:
        mission_data = self.get_mission_info()
        if not mission_data.is_empty():
            return self.process_mission(mission_data)
        else:
            return CMetaDataUtils.merge_result(CMetaDataUtils.Failure, '没有可执行的任务！')

    def get_mission_info(self) -> CDataSet:
        mission_flag = CMetaDataUtils.one_id()
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
        except DBException as err:
            return CDataSet()

    def abnormal_mission_restart(self):
        sql = self.get_abnormal_mission_restart_sql()
        if sql is not None:
            try:
                factory = CFactory()
                db = factory.give_me_db(self.get_mission_db_id())
                db.execute(sql)
            except Exception as err:
                pass
