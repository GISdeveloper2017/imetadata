#!/usr/bin/python3
# -*- coding:utf-8 -*-


"""
@author 王西亚
@desc 本模块是一个数据库的操作对象，其中负责数据库的连接池的维护，并设计了基础的数据库处理模式
@date 2020-06-02
说明：
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
from imetadata.base.core.Exceptions import *
from sqlalchemy.engine import Engine
from imetadata.database.base.c_dataset import CDataSet


class CDataBase:
    """
    数据库对象
    """
    DATABASE_POSTGRESQL = 'postgresql'
    DATABASE_MYSQL = 'mysql'

    __db_conn_id__ = ''
    __db_conn_type__ = ''

    __db_conn_host__ = ''
    __db_conn_port__ = ''
    __db_conn_name__ = ''
    __db_conn_username__ = ''
    __db_conn_password_native__ = ''
    __db_conn_password__ = ''

    def __init__(self, database_option):
        self.__db_conn_id__ = database_option['id']
        self.__db_conn_type__ = database_option['type']
        self.__db_conn_host__ = database_option['host']
        self.__db_conn_port__ = database_option['port']
        self.__db_conn_name__ = database_option['database']
        self.__db_conn_username__ = database_option['username']
        self.__db_conn_password_native__ = database_option['password']
        self.__db_conn_password__ = urllib.parse.quote_plus(self.__db_conn_password_native__)
        self.__init_db__(database_option)

    def __init_db__(self, database_option):
        pass

    def db_connection(self):
        return ''

    def one_row(self, sql, params=None) -> CDataSet:
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, params)
                data = cursor.fetchone()
                if data is None:
                    return CDataSet()
                else:
                    row_data = [data]
                    return CDataSet(row_data)
            finally:
                session.close()
        finally:
            eng.dispose()

    def all_row(self, sql, params=None) -> CDataSet:
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, params)
                data = cursor.fetchall()
                return CDataSet(data)
            except:
                raise DBSQLExecuteException(self.__db_conn_id__, sql)
            finally:
                session.close()
        finally:
            eng.dispose()

    def execute(self, sql, params=None) -> bool:
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, params)
                session.commit()
                return True
            except Exception as ee:
                session.rollback()
                raise DBSQLExecuteException(self.__db_conn_id__, sql)
                # print(cursor.lastrowid)
            finally:
                session.close()
        finally:
            eng.dispose()

    def if_exists(self, sql, params=None) -> bool:
        data = self.one_row(sql, params)
        return not data.is_empty()

    def engine(self) -> Engine:
        try:
            return create_engine(self.db_connection(), echo=True, max_overflow=5)
        except:
            raise DBLinkException(self.__db_conn_id__)
