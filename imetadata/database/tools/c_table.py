# -*- coding: utf-8 -*- 
# @Time : 2020/11/21 12:25 
# @Author : 王西亚 
# @File : c_table.py
from abc import abstractmethod

from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.base.c_columnList import CColumnList


class CTable(CResource):
    __db_id: str = None
    __table_name: str = None
    __column_list = CColumnList()

    def __init__(self):
        self.__column_list = list()

    def load_info(self, db_id, table_name):
        self.__db_id = db_id
        self.__table_name = table_name
        self.__load_table_info()

    @property
    def db_id(self):
        return self.__db_id

    @property
    def table_name(self):
        return self.__table_name

    @abstractmethod
    def __load_table_info(self):
        """
        在这里加载数据表的信息, 并初始化__column_list对象
        todo(赵宇飞) 这里需要将dict格式的字典信息, 更新到column_list中
        :return:
        """
        dict_table_info = CFactory().give_me_db(self.db_id).table_info(self.__table_name)

    def save_data(self) -> str:
        if self.if_exists():
            return self.update_data()
        else:
            return self.insert_data()

    def if_exists(self) -> bool:
        return False

    def insert_data(self) -> str:
        return CResult.merge_result(CResult.Success)

    def update_data(self) -> str:
        return CResult.merge_result(CResult.Success)

    def delete_data(self) -> str:
        return CResult.merge_result(CResult.Success)
