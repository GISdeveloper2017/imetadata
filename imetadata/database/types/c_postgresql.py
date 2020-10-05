#!/usr/bin/python3
# -*- coding:utf-8 -*-


"""
@author 王西亚
@desc 本模块是Postgresql数据库的实例化
@date 2020-06-02
说明：
# default
engine = create_engine('postgresql://scott:tiger@localhost:port/mydatabase')

# psycopg2
engine = create_engine('postgresql+psycopg2://scott:tiger@localhost:port/mydatabase')

# pg8000
engine = create_engine('postgresql+pg8000://scott:tiger@localhost:port/mydatabase')
"""

from imetadata.database.base.c_database import CDataBase


class CPostgreSQL(CDataBase):
    def __init__(self, database_option):
        super().__init__(self, database_option)

    def db_connection(self):
        return "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            self.__db_conn_username__,
            self.__db_conn_password__,
            self.__db_conn_host__,
            self.__db_conn_port__,
            self.__db_conn_name__
        )
