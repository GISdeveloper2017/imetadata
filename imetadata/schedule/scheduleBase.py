#!/usr/bin/python3
# -*- coding:utf-8 -*-

from imetadata.base.utils import MetaDataUtils
from imetadata.database.base.dataset import DataSet
from imetadata.database.factory import Factory
from imetadata.base.core.Exceptions import *
from abc import abstractmethod


class scheduleBase:
    SYSTEM_NAME_MISSION_ID = '{system.mission.id}'

    __id__: str = None

    def __init__(self, a_id: str):
        self.__id__ = a_id

    def get_mission_db_id(self) -> str:
        return '0'

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
        return MetaDataUtils.merge_result(MetaDataUtils.Success, '测试成功')

    def execute(self) -> str:
        mission_data = self.get_mission_info()
        if not mission_data.is_empty():
            return self.process_mission(mission_data)
        else:
            return MetaDataUtils.merge_result(MetaDataUtils.Failure, '没有可执行的任务！')

    def get_mission_info(self) -> DataSet:
        mission_flag = MetaDataUtils.one_id()
        mission_seize_sql = self.get_mission_seize_sql()
        mission_info_sql = self.get_mission_info_sql()

        if mission_seize_sql is None:
            return None
        if mission_info_sql is None:
            return None

        mission_seize_sql = mission_seize_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)
        mission_info_sql = mission_info_sql.replace(self.SYSTEM_NAME_MISSION_ID, mission_flag)

        try:
            factory = Factory()
            db = factory.give_me_db(self.get_mission_db_id())
            db.execute(mission_seize_sql)

            return db.one_row(mission_info_sql)
        except DBException as err:
            return DataSet()

    def abnormal_mission_restart(self):
        sql = self.get_abnormal_mission_restart_sql()
        if sql is not None:
            try:
                factory = Factory()
                db = factory.give_me_db(self.get_mission_db_id())
                db.execute(sql)
            except Exception as err:
                pass

    def before_execute(self):
        pass

    def before_stop(self):
        pass
