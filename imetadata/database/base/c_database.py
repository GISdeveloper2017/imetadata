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

    __db_conn_id__ = ''
    __db_conn_type__ = ''

    __db_conn_host__ = ''
    __db_conn_port__ = ''
    __db_conn_name__ = ''
    __db_conn_username__ = ''
    __db_conn_password_native__ = ''
    __db_conn_password__ = ''

    def __init__(self, database_option):
        """
        todo(王西亚) 这里需要考虑数据库访问密码的明文存储和解密事宜
        :param database_option:
        """
        self.__sql__ = self.create_default_sql()

        self.__db_conn_id__ = CUtils.dict_value_by_name(database_option, self.Name_ID, self.DB_Server_ID_Default)
        self.__db_conn_type__ = CUtils.dict_value_by_name(database_option, self.Name_Type, self.DB_Type_Postgresql)
        self.__db_conn_host__ = CUtils.dict_value_by_name(database_option, CResource.Name_Host, self.Host_LocalHost)
        self.__db_conn_port__ = CUtils.dict_value_by_name(database_option, CResource.Name_Port,
                                                          CResource.Port_Postgresql_Default)
        self.__db_conn_name__ = CUtils.dict_value_by_name(database_option, CResource.Name_DataBase, '')
        self.__db_conn_username__ = CUtils.dict_value_by_name(database_option, CResource.Name_UserName, '')
        self.__db_conn_password_native__ = CUtils.dict_value_by_name(database_option, CResource.Name_Password, '')
        self.__db_conn_password__ = urllib.parse.quote_plus(self.__db_conn_password_native__)
        self.__init_db__(database_option)

    def __init_db__(self, database_option):
        pass

    def db_connection(self):
        return ''

    def sql(self):
        return self.__sql__

    def __prepare_params_of_execute_sql__(self, engine, sql, params):
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
                cursor = session.execute(sql, self.__prepare_params_of_execute_sql__(eng, sql, params))
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
                cursor = session.execute(sql, self.__prepare_params_of_execute_sql__(eng, sql, params))
                data = cursor.fetchall()
                return CDataSet(data)
            except:
                raise DBSQLExecuteException(self.__db_conn_id__, sql)
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
                cursor = session.execute(sql, self.__prepare_params_of_execute_sql__(eng, sql, params))
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
            return create_engine(self.db_connection(), echo=True, max_overflow=5)
        except:
            raise DBLinkException(self.__db_conn_id__)

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
        session.execute(sql, self.__prepare_params_of_execute_sql__(session.get_bind(), sql, params))

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
            return False
        finally:
            self.session_close(session)

    @abstractmethod
    def create_default_sql(self) -> CSql:
        pass

    @abstractmethod
    def seq_next_value(self, seq_type: int) -> str:
        pass
