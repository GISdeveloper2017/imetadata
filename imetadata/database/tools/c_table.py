# -*- coding: utf-8 -*- 
# @Time : 2020/11/21 12:25 
# @Author : 王西亚 
# @File : c_table.py
from abc import abstractmethod

from sqlalchemy.orm.session import Session

import settings
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_database import CDataBase
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.base.c_column import CColumn
from imetadata.database.tools.base.c_columnList import CColumnList


class CTable(CResource):
    """
    数据表记录更新类
    . 可以自动提取数据表中的字段信息
    . 通过简单的方式, 设置每一个字段的内容
    . 数据表将根据结构中的主键等信息, 自动进行更新\插入\删除等操作
    """
    __database: CDataBase = None
    __db_id: str = None
    __table_name: str = None
    __column_list: CColumnList = None

    def __init__(self):
        self.__column_list = CColumnList()

    def load_info(self, db_id, table_name):
        self.__db_id = db_id
        self.__database = CFactory().give_me_db(self.__db_id)
        self.__table_name = table_name
        self.__load_table_info()

    @property
    def column_list(self):
        return self.__column_list

    @property
    def db_id(self) -> str:
        return self.__db_id

    @property
    def table_name(self):
        return self.__table_name

    @abstractmethod
    def __load_table_info(self):
        """
        在这里加载数据表的信息, 并初始化__column_list对象
        :return:
        """
        dict_table_info = self.__database.table_info(self.__table_name)
        table_column_list = CUtils.dict_value_by_name(dict_table_info, self.Name_Columns, None)
        self.__column_list.clear()
        if table_column_list is None:
            return

        for table_column in table_column_list:
            column_name = CUtils.dict_value_by_name(table_column, self.Name_Name, '')
            if CUtils.equal_ignore_case(column_name, ''):
                continue

            column_data_type = CUtils.dict_value_by_name(table_column, self.Name_DataType, '')
            column_is_primary_key = CUtils.dict_value_by_name(table_column, self.Name_PrimaryKey, 0)
            self.__column_list.add(CColumn(column_name, column_data_type, column_is_primary_key == self.DB_True))

    def __param_name(self, column_name: str) -> str:
        return '{0}'.format(column_name.strip().lower())

    def __prepare_where_condition(self, column: CColumn, sql_text: str, sql_params: dict):
        column_type = self.__database.db_column_type_by_name(column.db_column_type)
        if CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Param):
            sql_text = CUtils.str_append(
                sql_text,
                '{0}=:{1}'.format(column.name, self.__param_name(column.name)),
                ' and '
            )
            sql_params[self.__param_name(column.name)] = CUtils.any_2_str(
                CUtils.dict_value_by_name(column.value, self.Name_Text, ''))
        elif CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Function):
            sql_text = CUtils.str_append(
                sql_text,
                '{0}=:{1}'.format(column.name, self.__param_name(column.name)),
                ' and '
            )
            sql_params[self.__param_name(column.name)] = CUtils.replace_placeholder(
                column_type.set_value_template,
                dict(
                    {
                        self.Name_Value, CUtils.any_2_str(CUtils.dict_value_by_name(column.value, self.Name_Text, ''))
                    }
                )
            )
        return sql_text, sql_params

    def __prepare_where(self):
        sql_text = ''
        sql_params = {}
        for column_index in range(self.__column_list.size()):
            column = self.__column_list.column_by_index(column_index)
            if column.is_primary_key:
                sql_text, sql_params = self.__prepare_where_condition(column, sql_text, sql_params)

        return sql_text, sql_params

    def __prepare_if_exists(self):
        sql_from = self.__column_list.column_by_index(0).name
        for column_index in range(self.__column_list.size()):
            column = self.__column_list.column_by_index(column_index)
            if column.is_primary_key:
                sql_from = column.name
                break

        sql_text, sql_params = self.__prepare_where()
        sql_text = CUtils.str_append('select {0} from {1}'.format(sql_from, self.__table_name), sql_text, ' where ')
        return sql_text, sql_params

    def __prepare_insert_data(self) -> list:
        sql_list = []

        temp_helper_code_list = []
        sql_insert_field = ''
        sql_insert_data = ''
        sql_insert_params = dict()
        for column_index in range(self.__column_list.size()):
            column = self.__column_list.column_by_index(column_index)

            if column.value is None:
                continue
            try:
                column_type = self.__database.db_column_type_by_name(column.db_column_type)
                column_insert_field, column_insert_data = '', ''
                column_value_type = CUtils.dict_value_by_name(column.value, self.Name_Type, self.DataValueType_SQL)
                column_value_as_text = CUtils.any_2_str(CUtils.dict_value_by_name(column.value, self.Name_Text, ''))
                # 如果值为原生sql, 则不管字段类型为何值, 都直接把sql存入insert_data语句中
                if CUtils.equal_ignore_case(column_value_type, self.DataValueType_SQL):
                    column_insert_field = column.name
                    column_insert_data = column_value_as_text
                elif CUtils.equal_ignore_case(column_value_type, self.DataValueType_File):
                    column_insert_field = column.name
                    column_insert_data = ':{0}'.format(self.__param_name(column.name))
                    self.__database.file2param(
                        sql_insert_params,
                        self.__param_name(column.name),
                        column_value_as_text
                    )
                else:
                    if CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Function):
                        column_insert_field = column.name
                        if len(column_value_as_text) > column_type.function_param_max_size >= 0:
                            column_data_id = CUtils.one_id()
                            temp_helper_code_list.append(column_data_id)
                            sql_exchange = '''
                            insert into ro_global_spatialhandle(code, data) values(:code, :data)
                            '''
                            param_exchange = {'code': column_data_id, 'data': column_value_as_text}
                            sql_list.append((sql_exchange, param_exchange))

                            column_insert_data = CUtils.replace_placeholder(
                                column_type.set_value_template,
                                dict(
                                    {
                                        self.Name_Value: "(select data from ro_global_spatialhandle where code = '{0}')".format(
                                            column_data_id)
                                    }
                                )
                            )
                        else:
                            if column_type.function_param_quoted:
                                column_value_as_text = CUtils.quote(column_value_as_text)
                            column_insert_data = CUtils.replace_placeholder(
                                column_type.set_value_template,
                                dict(
                                    {
                                        self.Name_Value: column_value_as_text
                                    }
                                )
                            )
                    elif CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Geometry):
                        column_insert_field = column.name
                        if len(column_value_as_text) > column_type.function_param_max_size >= 0:
                            column_data_id = CUtils.one_id()
                            temp_helper_code_list.append(column_data_id)
                            sql_exchange = '''
                            insert into ro_global_spatialhandle(code, data) values(:code, :data)
                            '''
                            param_exchange = {'code': column_data_id, 'data': column_value_as_text}
                            sql_list.append((sql_exchange, param_exchange))

                            column_insert_data = CUtils.replace_placeholder(
                                column_type.set_value_template,
                                dict(
                                    {
                                        self.Name_Value: "(select data from ro_global_spatialhandle where code = '{0}')".format(
                                            column_data_id),
                                        self.Name_Srid: CUtils.dict_value_by_name(
                                            column.value,
                                            self.Name_Srid,
                                            settings.application.xpath_one(
                                                self.Path_Setting_Spatial_Srid,
                                                self.SRID_WGS84
                                            )
                                        )
                                    }
                                )
                            )
                        else:
                            if column_type.function_param_quoted:
                                column_value_as_text = CUtils.quote(column_value_as_text)
                            column_insert_data = CUtils.replace_placeholder(
                                column_type.set_value_template,
                                dict(
                                    {
                                        self.Name_Value: column_value_as_text,
                                        self.Name_Srid: CUtils.dict_value_by_name(
                                            column.value,
                                            self.Name_Srid,
                                            settings.application.xpath_one(
                                                self.Path_Setting_Spatial_Srid,
                                                self.SRID_WGS84
                                            )
                                        )
                                    }
                                )
                            )
                    else:  # if CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Param):
                        column_insert_field = column.name
                        column_insert_data = ':{0}'.format(self.__param_name(column.name))
                        sql_insert_params[self.__param_name(column.name)] = column_value_as_text

                sql_insert_field = CUtils.str_append(sql_insert_field, column_insert_field, ', ')
                sql_insert_data = CUtils.str_append(sql_insert_data, column_insert_data, ', ')
            except Exception as error:
                print(error.__str__())
                raise

        sql_insert = 'insert into {0}({1}) values({2})'.format(self.__table_name, sql_insert_field, sql_insert_data)
        sql_list.append((sql_insert, sql_insert_params))

        for temp_helper_code in temp_helper_code_list:
            sql_list.append(("delete from ro_global_spatialhandle where code = '{0}'".format(temp_helper_code), None))

        return sql_list

    def __prepare_update_data(self) -> list:
        sql_list = []

        temp_helper_code_list = []

        sql_update_set = ''
        sql_update_params = dict()
        for column_index in range(self.__column_list.size()):
            column = self.__column_list.column_by_index(column_index)

            if column.is_primary_key or (column.value is None):
                continue

            try:
                column_type = self.__database.db_column_type_by_name(column.db_column_type)
                column_value_type = CUtils.dict_value_by_name(column.value, self.Name_Type, self.DataValueType_SQL)
                column_value_as_text = CUtils.any_2_str(CUtils.dict_value_by_name(column.value, self.Name_Text, ''))
                # 如果值为原生sql, 则不管字段类型为何值, 都直接把sql存入insert_data语句中
                if CUtils.equal_ignore_case(column_value_type, self.DataValueType_SQL):
                    column_update_set = '{0}={1}'.format(column.name, column_value_as_text)
                elif CUtils.equal_ignore_case(column_value_type, self.DataValueType_File):
                    column_update_set = '{0}={1}'.format(column.name, ':{0}'.format(self.__param_name(column.name)))
                    self.__database.file2param(
                        sql_update_params,
                        self.__param_name(column.name),
                        column_value_as_text
                    )
                else:
                    if CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Function):
                        if len(column_value_as_text) > column_type.function_param_max_size >= 0:
                            column_data_id = CUtils.one_id()
                            temp_helper_code_list.append(column_data_id)
                            sql_exchange = '''
                            insert into ro_global_spatialhandle(code, data) values(:code, :data)
                            '''
                            param_exchange = {'code': column_data_id, 'data': column_value_as_text}
                            sql_list.append((sql_exchange, param_exchange))

                            column_update_set = '{0}={1}'.format(
                                column.name,
                                CUtils.replace_placeholder(
                                    column_type.set_value_template,
                                    dict(
                                        {
                                            self.Name_Value: "(select data from ro_global_spatialhandle where code = '{0}')".format(
                                                column_data_id)
                                        }
                                    )
                                )
                            )
                        else:
                            if column_type.function_param_quoted:
                                column_value_as_text = CUtils.quote(column_value_as_text)
                            column_update_set = '{0}={1}'.format(
                                column.name,
                                CUtils.replace_placeholder(
                                    column_type.set_value_template,
                                    dict(
                                        {
                                            self.Name_Value: column_value_as_text
                                        }
                                    )
                                )
                            )
                    elif CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Geometry):
                        if len(column_value_as_text) > column_type.function_param_max_size >= 0:
                            column_data_id = CUtils.one_id()
                            temp_helper_code_list.append(column_data_id)
                            sql_exchange = '''
                            insert into ro_global_spatialhandle(code, data) values(:code, :data)
                            '''
                            param_exchange = {'code': column_data_id, 'data': column_value_as_text}
                            sql_list.append((sql_exchange, param_exchange))

                            column_update_set = '{0}={1}'.format(
                                column.name,
                                CUtils.replace_placeholder(
                                    column_type.set_value_template,
                                    dict(
                                        {
                                            self.Name_Value: "(select data from ro_global_spatialhandle where code = '{0}')".format(
                                                column_data_id),
                                            self.Name_Srid: CUtils.dict_value_by_name(
                                                column.value,
                                                self.Name_Srid,
                                                settings.application.xpath_one(self.Path_Setting_Spatial_Srid,
                                                                               self.SRID_WGS84)
                                            )
                                        }
                                    )
                                )
                            )
                        else:
                            if column_type.function_param_quoted:
                                column_value_as_text = CUtils.quote(column_value_as_text)
                            column_update_set = '{0}={1}'.format(
                                column.name,
                                CUtils.replace_placeholder(
                                    column_type.set_value_template,
                                    dict(
                                        {
                                            self.Name_Value: column_value_as_text,
                                            self.Name_Srid: CUtils.dict_value_by_name(
                                                column.value,
                                                self.Name_Srid,
                                                settings.application.xpath_one(
                                                    self.Path_Setting_Spatial_Srid,
                                                    self.SRID_WGS84
                                                )
                                            )
                                        }
                                    )
                                )
                            )
                    else:  # if CUtils.equal_ignore_case(column_type.set_value_method, self.DB_Column_Set_Method_Param):
                        column_update_set = '{0}={1}'.format(column.name, ':{0}'.format(self.__param_name(column.name)))
                        sql_update_params[self.__param_name(column.name)] = column_value_as_text

                sql_update_set = CUtils.str_append(sql_update_set, column_update_set, ', ')
            except Exception as error:
                print(error.__str__())
                raise

        sql_where = ''
        for column_index in range(self.__column_list.size()):
            column = self.__column_list.column_by_index(column_index)
            if column.is_primary_key:
                sql_where, sql_update_params = self.__prepare_where_condition(column, sql_where, sql_update_params)

        if not CUtils.equal_ignore_case(sql_where, ''):
            sql_where = CUtils.str_append(' where ', sql_where, ' ')

        sql_update = 'update {0} set {1} {2}'.format(self.__table_name, sql_update_set, sql_where)
        sql_list.append((sql_update, sql_update_params))

        for temp_helper_code in temp_helper_code_list:
            sql_list.append(("delete from ro_global_spatialhandle where code = '{0}'".format(temp_helper_code), None))

        return sql_list

    def __prepare_delete(self):
        sql_text, sql_params = self.__prepare_where()
        sql_text = CUtils.str_append('delete from {0}'.format(self.__table_name), sql_text, ' where ')
        return sql_text, sql_params

    def sql_of_insert(self) -> list:
        return self.__prepare_insert_data()

    def sql_of_update(self) -> list:
        return self.__prepare_update_data()

    def sql_of_delete(self) -> list:
        sql_text, sql_params = self.__prepare_delete()
        return [(sql_text, sql_params)]

    def save_data(self, session: Session = None) -> str:
        if self.if_exists(session):
            return self.update_data(session)
        else:
            return self.insert_data(session)

    def if_exists(self, session: Session = None) -> bool:
        sql_text, sql_params = self.__prepare_if_exists()

        if session is None:
            return self.__database.if_exists(sql_text, sql_params)
        else:
            return self.__database.session_if_exists(session, sql_text, sql_params)

    def insert_data(self, session: Session = None) -> str:
        try:
            sql_list = self.__prepare_insert_data()

            if session is None:
                self.__database.execute_batch(sql_list)
            else:
                self.__database.session_execute_batch(session, sql_list)

            return CResult.merge_result(CResult.Success)
        except Exception as error:
            return CResult.merge_result(CResult.Failure, error.__str__())

    def update_data(self, session: Session = None) -> str:
        try:
            sql_list = self.__prepare_update_data()

            if session is None:
                self.__database.execute_batch(sql_list)
            else:
                self.__database.session_execute_batch(session, sql_list)

            return CResult.merge_result(CResult.Success)
        except Exception as error:
            return CResult.merge_result(CResult.Failure, error.__str__())

    def delete_data(self, session: Session = None) -> str:
        try:
            sql_text, sql_params = self.__prepare_delete()

            if session is None:
                self.__database.execute(sql_text, sql_params)
            else:
                self.__database.session_execute(session, sql_text, sql_params)
            return CResult.merge_result(CResult.Success)
        except Exception as error:
            return CResult.merge_result(CResult.Failure, error.__str__())
