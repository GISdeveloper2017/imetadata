#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

from imetadata import settings
from imetadata.base.Exceptions import *
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.singleton import singleton
from imetadata.database.base.c_database import CDataBase
from imetadata.database.types.c_postgresql import CPostgreSQL


@singleton
class CFactory(CResource):
    def __init__(self):
        pass

    def create_db(self, database) -> CDataBase:
        if database[self.Name_Type].strip().lower() == CDataBase.DATABASE_POSTGRESQL:
            return CPostgreSQL(database)
        else:
            raise DBException(CUtils.dict_value_by_name(database, self.Name_ID, self.DB_Server_ID_Default))

    def give_me_db(self, db_id=None) -> CDataBase:
        if db_id is None:
            rt_db_id = self.DB_Server_ID_Default
        else:
            rt_db_id = CUtils.any_2_str(db_id)

        if CUtils.equal_ignore_case(rt_db_id, ''):
            rt_db_id = self.DB_Server_ID_Default

        for database in CUtils.dict_value_by_name(settings.application, self.Name_DataBases, None):
            if rt_db_id == CUtils.dict_value_by_name(database, self.Name_ID, self.DB_Server_ID_Default):
                return self.create_db(database)

        raise Exception('未找到标示为[{0}]]的数据库定义！'.format(rt_db_id))
