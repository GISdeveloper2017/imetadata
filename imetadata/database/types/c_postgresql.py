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
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_database import CDataBase
from imetadata.database.base.sql.c_sql import CSql
from imetadata.database.types.sql.c_sqlPostgresql import CSqlPostgresql


class CPostgreSQL(CDataBase):
    def create_default_sql(self) -> CSql:
        return CSqlPostgresql(self.DATABASE_POSTGRESQL, 0)

    def db_connection(self):
        return "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            self.__db_conn_username__,
            self.__db_conn_password__,
            self.__db_conn_host__,
            self.__db_conn_port__,
            self.__db_conn_name__
        )

    def seq_next_value(self, seq_type: int) -> str:
        if seq_type == self.Seq_Type_Date_AutoInc:
            sql_last_seq_date = '''
            select coalesce(gcfgvalue, current_date::text) as last_date, current_date::text as curr_date from ro_global_config where
            gcfgcode = 'sys_seq_date_autoinc'
            '''
            ds_last_seq_date = self.one_row(sql_last_seq_date)
            if ds_last_seq_date.is_empty():
                self.execute('''
                insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo)
                values (10001, 'sys_seq_date_autoinc', '日期自增序列最后记录', current_date::text, null)
                ''')
                ds_last_seq_date = self.one_row(sql_last_seq_date)

            last_seq_date = ds_last_seq_date.value_by_name(0, 'last_date', None)
            curr_seq_date = ds_last_seq_date.value_by_name(0, 'curr_date', None)
            if last_seq_date is None:
                self.execute(
                    '''
                    update ro_global_config set gcfgvalue = current_date::text
                    where gcfgcode = 'sys_seq_date_autoinc'
                    ''')
            elif not CUtils.equal_ignore_case(last_seq_date, curr_seq_date):
                self.execute('''
                update ro_global_config set gcfgvalue = current_date::text
                where gcfgcode = 'sys_seq_date_autoinc'
                ''')
                next_value = self.one_row("select setval('sys_seq_date_autoinc', 1)").value_by_index(0, 0, 1)
                return '{0}-{1}'.format(curr_seq_date, CUtils.int_2_format_str(next_value, 3))

            next_value = self.one_row("select nextval('sys_seq_date_autoinc')").value_by_index(0, 0, 1)
            return '{0}-{1}'.format(curr_seq_date, CUtils.int_2_format_str(next_value, 3))
        else:
            return CUtils.any_2_str(self.one_row("select nextval('sys_seq_autoinc')").value_by_index(0, 0, 1))
