#!/usr/bin/python3
# -*- coding:utf-8 -*-


"""
@author 王西亚
@desc 本模块是一个数据库的操作对象，其中负责数据库的连接池的维护，并设计了基础的数据库处理模式
@date 2020-06-02
说明：
2020-09-15 王西亚
.增加session的获取, 关闭, 执行sql, 提交和撤销动作, 以支持自定义的数据库事务
"""

import urllib.parse
from abc import abstractmethod

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from imetadata.base.c_logger import CLogger
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.exceptions import *
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.base.sql.c_sql import CSql


class CDataBase(CResource):
    """
    数据库对象
    """
    DATABASE_POSTGRESQL = 'postgresql'
    DATABASE_MYSQL = 'mysql'

    _db_conn_id = ''
    _db_conn_type = ''

    _db_conn_host = ''
    _db_conn_port = ''
    _db_conn_database = ''
    _db_conn_schema: str = ''
    _db_conn_username = ''
    _db_conn_password_native = ''
    _db_conn_password = ''

    _db_column_list_define = None

    def __init__(self, database_option):
        """
        todo(王西亚) 这里需要考虑数据库访问密码的明文存储和解密事宜
        :param database_option:
        """
        self.__sql = self._create_default_sql()
        self._db_column_list_define = list()

        self._db_conn_id = CUtils.dict_value_by_name(database_option, self.Name_ID, self.DB_Server_ID_Default)
        self._db_conn_type = CUtils.dict_value_by_name(database_option, self.Name_Type, self.DB_Type_Postgresql)
        self._db_conn_host = CUtils.dict_value_by_name(database_option, CResource.Name_Host, self.Host_LocalHost)
        self._db_conn_port = CUtils.dict_value_by_name(database_option, CResource.Name_Port,
                                                       CResource.Port_Postgresql_Default)
        self._db_conn_database = CUtils.dict_value_by_name(database_option, CResource.Name_DataBase, '')
        self._db_conn_schema = CUtils.dict_value_by_name(database_option, CResource.Name_Schema, CResource.Name_Public)
        self._db_conn_username = CUtils.dict_value_by_name(database_option, CResource.Name_UserName, '')
        self._db_conn_password_native = CUtils.dict_value_by_name(database_option, CResource.Name_Password, '')
        self._db_conn_password = urllib.parse.quote_plus(self._db_conn_password_native)
        self._init_db(database_option)

    def _init_db(self, database_option):
        """
        在这里对数据库常见的字段进行初始化
        :param database_option:
        :return:
        """
        pass

    def _db_connection(self):
        return ''

    @property
    def db_column_list_define(self) -> list:
        return self._db_column_list_define

    @property
    def sql(self) -> CSql:
        return self.__sql

    def _prepare_params_of_execute_sql(self, engine, sql, params):
        """
        处理和优化传入的参数
        todo 还不支持blob字段的入库, 在需要时去实现
        :param engine:
        :param sql:
        :param params:
        :return:
        """
        if params is None:
            return None
        else:
            statement = text(sql)
            exe_params = statement.compile(engine).params

            new_params = {}
            exe_params_names = exe_params.keys()
            new_params = dict()
            for exe_param_name in exe_params_names:
                exe_param_value = CUtils.dict_value_by_name(params, exe_param_name, None)
                if exe_param_value is not None:
                    new_params[exe_param_name] = exe_param_value
                else:
                    new_params[exe_param_name] = None
            return new_params

    def table_info(self, table_name: str) -> dict:
        return None

    def one_value(self, sql, params=None, default_value=None):
        object_copy_stat_dataset = self.one_row(sql, params)

        if object_copy_stat_dataset is None:
            return default_value
        elif object_copy_stat_dataset.is_empty():
            return default_value
        else:
            return object_copy_stat_dataset.value_by_index(0, 0, default_value)

    def one_row(self, sql, params=None) -> CDataSet:
        """
        执行sql, 返回第一行符合要求的记录
        :param sql:
        :param params:
        :return:
        """
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, self._prepare_params_of_execute_sql(eng, sql, params))
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
        """
        执行sql, 返回所有符合要求的记录
        :param sql:
        :param params:
        :return:
        """
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, self._prepare_params_of_execute_sql(eng, sql, params))
                data = cursor.fetchall()
                return CDataSet(data)
            except:
                raise DBSQLExecuteException(self._db_conn_id, sql)
            finally:
                session.close()
        finally:
            eng.dispose()

    def execute(self, sql, params=None) -> bool:
        """
        执行sql, 无返回记录
        :param sql:
        :param params:
        :return:
        """
        eng = self.engine()
        try:
            session_maker = sessionmaker(bind=eng)
            session = session_maker()
            try:
                cursor = session.execute(sql, self._prepare_params_of_execute_sql(eng, sql, params))
                session.commit()
                return True
            except Exception as ee:
                session.rollback()
                raise
                # raise DBSQLExecuteException(self.__db_conn_id__, sql)
                # print(cursor.lastrowid)
            finally:
                session.close()
        finally:
            eng.dispose()

    def if_exists(self, sql, params=None) -> bool:
        """
        检测一个sql查询是否有结果
        :param sql:
        :param params:
        :return:
        """
        data = self.one_row(sql, params)
        return not data.is_empty()

    def engine(self) -> Engine:
        """
        返回一个引擎
        :return:
        """
        try:
            return create_engine(self._db_connection(), echo=True, max_overflow=5)
        except:
            raise DBLinkException(self._db_conn_id)

    def give_me_session(self, engine_obj: Engine = None):
        """
        为了自行控制数据库事务, 这里可以直接创建session
        :return:
        """
        if engine_obj is None:
            eng = self.engine()
        else:
            eng = engine_obj
        session_maker = sessionmaker(bind=eng)
        session = session_maker()
        session.autocommit = False
        return session

    def session_close(self, session: Session):
        """
        session必须手工在finally里关闭
        :param session:
        :return:
        """
        eng = session.get_bind()
        session.close()
        if eng is not None:
            eng.dispose()

    def session_execute(self, session: Session, sql: str, params=None):
        """
        session执行sql
        :param session:
        :param sql:
        :param params:
        :return:
        """
        session.execute(sql, self._prepare_params_of_execute_sql(session.get_bind(), sql, params))

    def session_commit(self, session: Session):
        """
        session的Commit操作
        :param session:
        :return:
        """
        session.commit()

    def session_rollback(self, session: Session):
        """
        session的rollback操作
        :param session:
        :return:
        """
        session.rollback()

    def execute_batch(self, sql_params_tuple: []) -> bool:
        """
        批处理事务执行
        @param db_server_id: 数据库服务器识别id
        @param sql_params_tuple: sql与dict参数组合的元组集合 [(sql1,dict_params1),(sql2,dict_params2)]
        @return:
        """
        session = self.give_me_session()
        try:
            for sql, params in sql_params_tuple:
                self.session_execute(session, sql, params)
            self.session_commit(session)
            return True
        except Exception as error:
            CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__()))
            self.session_rollback(session)
            raise
        finally:
            self.session_close(session)

    @abstractmethod
    def _create_default_sql(self) -> CSql:
        pass

    @abstractmethod
    def seq_next_value(self, seq_type: int) -> str:
        pass
