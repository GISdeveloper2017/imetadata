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
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_database import CDataBase
from imetadata.database.base.sql.c_sql import CSql
from imetadata.database.types.sql.c_sqlPostgresql import CSqlPostgresql


class CPostgreSQL(CDataBase):
    def _create_default_sql(self) -> CSql:
        return CSqlPostgresql(self.DATABASE_POSTGRESQL, 0)

    def _init_db(self, database_option):
        """
        在这里对数据库常见的字段进行初始化
        :param database_option:
        :return:
        """
        self.db_column_list_define.append(
            {
                CResource.Name_Name: 'varchar'
                , CResource.Name_DataType: CResource.DataType_String
                , CResource.Name_Get: "'%(value)'"
                , CResource.Name_Set: "'%(value)'"
            }
        )

    def table_info(self, table_name: str) -> dict:
        result = dict()

        sql_get_table_info = '''
select pg_tables.tablename as table_name, table_Comments.description as table_description
from pg_tables 
  left join 
(
select pg_class.relname, pg_description.description
from pg_class 
  inner join pg_namespace ON pg_class.relnamespace = pg_namespace.oid AND upper(pg_namespace.nspname) = upper('{0}')
  left join pg_description ON pg_description.objoid = pg_class.oid and pg_description.objsubid = 0

) table_Comments
   on table_Comments.relname = pg_tables.tablename
where upper(pg_tables.schemaname) = upper('{0}') and upper(pg_tables.tablename) = upper('{1}')	        
        '''.format(table_name.upper(), self._db_conn_schema.upper())
        ds_table = self.one_row(sql_get_table_info)
        result[CResource.Name_Name] = table_name.lower()
        result[CResource.Name_Title] = ds_table.value_by_index(0, 1, '')

        sql_get_column_info = '''
select columns.column_name as columnname, columns.ordinal_position as primarykeyposition, columns.column_Default as DefaultValue, 
coalesce(columns.character_Maximum_length, columns.numeric_precision) as columnsize, columns.numeric_scale as scale, primarykey.primarykey, 
columns.udt_name as datatype, table_comments.comments, table_comments.extAttr
from information_schema.columns left join 
(
select b.column_name, 1 as primarykey
from information_schema.table_constraints a, information_schema.key_column_usage b
where upper(a.table_name) = '{1}'
  and upper(a.table_schema) = '{0}'
  and a.table_name = b.table_name
  and a.table_schema = b.table_schema
  and a.constraint_name = b.constraint_name
  and upper(a.constraint_type) = 'PRIMARY KEY' 
) primarykey on columns.column_name = primarykey.column_name  
left join
(
SELECT a.attname AS column_name,
       pg_description.description AS comments,
       format_type(ty.oid,a.atttypmod) as extAttr
 FROM
       pg_catalog.pg_attribute a
       INNER JOIN pg_class  ON a.attrelid = pg_class.oid AND upper(pg_class.relname)='{1}'
       INNER JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid AND upper(pg_namespace.nspname) = '{0}'
       INNER JOIN pg_type ty ON ty.oid=atttypid
       LEFT OUTER JOIN pg_description ON pg_description.objoid = pg_class.oid AND pg_description.objsubid = a.attnum
       LEFT OUTER JOIN (SELECT a.attnum, pg_constraint.contype
                        FROM pg_catalog.pg_attribute a
                 INNER JOIN pg_class  ON a.attrelid = pg_class.oid AND upper(pg_class.relname)='{1}'
                             INNER JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid AND upper(pg_namespace.nspname) = '{0}'
                             INNER JOIN pg_constraint ON pg_constraint.conrelid = pg_class.oid 
                                             AND pg_constraint.connamespace = pg_namespace.oid 
                                             AND a.attnum = ANY(pg_constraint.conkey)
                        GROUP BY a.attnum, pg_constraint.contype) b
                        ON a.attnum = b.attnum
 WHERE
       a.attnum > 0
       AND attisdropped <> 't'
       AND a.attname <> 'oid'
 ORDER BY a.attnum
) table_comments on columns.column_name = table_comments.column_name
where upper(columns.table_schema)=upper('{0}') and upper(columns.table_name) =upper('{1}')
order by columns.ordinal_position        
        '''.format(table_name.upper(), self._db_conn_schema.upper())
        ds_columns = self.all_row(sql_get_table_info)
        if not ds_columns.is_empty():
            columns_list = list()
            for column_index in range(ds_columns.size()):
                columns_list.append(
                    {
                        CResource.Name_Name: ds_columns.value_by_name(column_index, 'columnname', '')
                        , CResource.Name_DataType: ds_columns.value_by_name(column_index, 'datatype', '')
                        , CResource.Name_PrimaryKey: ds_columns.value_by_name(column_index, 'primarykey', '')
                    }
                )
            result[CResource.Name_Columns] = columns_list

        return result

    def _db_connection(self):
        return "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            self._db_conn_username,
            self._db_conn_password,
            self._db_conn_host,
            self._db_conn_port,
            self._db_conn_database
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
