#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import

from imetadata import settings
from imetadata.base.Exceptions import *
from imetadata.base.singleton import singleton
from imetadata.database.base.c_database import CDataBase
from imetadata.database.types.c_postgresql import CPostgreSQL


@singleton
class CFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_db(database) -> CDataBase:
        if database['job'].strip().lower() == CDataBase.DATABASE_POSTGRESQL:
            return CPostgreSQL(database)
        else:
            raise DBException(database['id'])

    @staticmethod
    def give_me_db(db_id: str = '0') -> CDataBase:
        for database in settings.databases:
            if db_id == database['id']:
                return __class__.create_db(database)

        raise Exception('未找到标示为%s的数据库定义！' % db_id)
