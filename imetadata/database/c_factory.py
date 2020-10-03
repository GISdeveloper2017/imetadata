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
        if database['job'].strip().lower() == CDataBase.DATABASE_POSTGRESQL:
            return CPostgreSQL(database)
        else:
            raise DBException(database['id'])

    def give_me_db(self, db_id: str = '0') -> CDataBase:
        for database in CUtils.dict_value_by_name(settings.application, self.Name_DataBases, None):
            if db_id == database['id']:
                return self.create_db(database)

        raise Exception('未找到标示为%s的数据库定义！' % db_id)
