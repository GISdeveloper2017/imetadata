# -*- coding: utf-8 -*- 
# @Time : 2020/11/12 08:32 
# @Author : 王西亚 
# @File : c_mdObjectSearch.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.database.base.c_dataset import CDataSet


class CMDObjectSearch(CResource):
    def __init__(self, db_server_id):
        self.__db_server_id = db_server_id

    def search_object(self, search_json_obj: CJson, other_option: dict = None) -> CDataSet:
        """
        根据搜索条件json, 检索符合要求的对象, 并以数据集的方式返回
        :param search_json_obj:
        :param other_option:
        :return:
        """
        if search_json_obj is None:
            return CDataSet()



