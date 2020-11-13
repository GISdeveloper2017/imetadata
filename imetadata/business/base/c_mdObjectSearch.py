# -*- coding: utf-8 -*- 
# @Time : 2020/11/12 08:32 
# @Author : 王西亚 
# @File : c_mdObjectSearch.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
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

        sql_search = '''
        select dm2_storage_object.dsoid as object_id
            , dm2_storage_object.dsoobjectname as object_name
            , dm2_storage_object.dsoobjecttype as object_type
            , dm2_storage_object.dsodatatype as object_data_type
            , dm2_storage_object.dsoparentobjid as object_parent_id
            , dm2_storage_object.dso_volumn_now as object_size
            , dm2_storage_object.dso_obj_lastmodifytime as object_lastmodifytime
        from dm2_storage_object 
            left join dm2_storage_object_def on dm2_storage_object.dsoobjecttype = dm2_storage_object_def.dsodid
        where
            dm2_storage_object_def.dsodid = :dsodid
        '''

        sql_where = ''
        condition_id = search_json_obj.xpath_one(self.Name_ID, None)
        if condition_id is not None:
            if isinstance(condition_id, list):
                condition_id = self.__condition_list_2_sql(condition_id)
            sql_where = CUtils.str_append(sql_where, '')

        return CDataSet()
