#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import
from imetadata.base.core.singleton import singleton
from imetadata.database.types.postgresql import PostgreSQL
from imetadata.database.base.database import DataBase
from imetadata import settings
from imetadata.base.core.Exceptions import *


@singleton
class Factory:
    def __init__(self):
        pass

    @staticmethod
    def create_db(database) -> DataBase:
        if database['type'].strip().lower() == DataBase.DATABASE_POSTGRESQL:
            return PostgreSQL(database)
        else:
            raise DBException(database['id'])

    @staticmethod
    def give_me_db(db_id: str = '0') -> DataBase:
        for database in settings.databases:
            if db_id == database['id']:
                return __class__.create_db(database)

        raise Exception('未找到标示为%s的数据库定义！' % db_id)
