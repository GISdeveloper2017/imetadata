# -*- coding: utf-8 -*- 
# @Time : 2020/11/12 08:32 
# @Author : 王西亚 
# @File : c_mdObjectCatalog.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.c_factory import CFactory


class CMDObjectCatalog(CResource):
    def __init__(self, db_server_id):
        self.__db_server_id = db_server_id

    @property
    def db_server_id(self):
        return self.__db_server_id

    def search(self, module_name: str, search_json_obj: CJson, other_option: dict = None) -> CDataSet:
        """
        根据搜索条件json, 检索符合要求的对象, 并以数据集的方式返回如下字段:
        1. object_id
        1. object_name
        1. object_type
        1. object_data_type
        1. object_parent_id
        1. object_size
        1. object_lastmodifytime
        :param module_name: 模块名称
        :param search_json_obj:
        :param other_option:
        :return:
        """
        if search_json_obj is None:
            return CDataSet()

        params_search = dict()
        sql_from = ''
        sql_where = ''

        if (not CUtils.equal_ignore_case(module_name, self.ModuleName_MetaData)) and \
                (not CUtils.equal_ignore_case(module_name, '')):
            # sql_where = "dm2_storage_object.dso_da_result#>>'{{{0},result}}'='pass'".format(module_name)
            sql_from = ', dm2_storage_obj_na '
            sql_where = " dm2_storage_obj_na.dson_app_id = 'module_name' "

        condition_obj_access = search_json_obj.xpath_one(self.Name_Access, self.DataAccess_Pass)
        if not CUtils.equal_ignore_case(condition_obj_access, ''):
            condition = "dm2_storage_obj_na.dson_object_access = '{0}'".format(CUtils.any_2_str(condition_obj_access))
            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_inbound_id = search_json_obj.xpath_one(self.Name_InBound, None)
        if not CUtils.equal_ignore_case(condition_inbound_id, ''):
            condition = "dm2_storage_obj.dso_ib_id = '{0}'".format(CUtils.any_2_str(condition_inbound_id))
            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_tag = search_json_obj.xpath_one(self.Name_Tag, None)
        if condition_tag is not None:
            if isinstance(condition_tag, list):
                condition = CUtils.list_2_str(condition_tag, "'", ", ", "'", True)
            else:
                condition = CUtils.list_2_str([condition_tag], "'", ", ", "'", True)
            if not CUtils.equal_ignore_case(condition, ''):
                condition = 'dm2_storage_object.dsotags @ > array[{0}]:: CHARACTER VARYING[]'.format(condition)

            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_id = search_json_obj.xpath_one(self.Name_ID, None)
        if condition_id is not None:
            if isinstance(condition_id, list):
                condition = self.__condition_list_2_sql('dm2_storage_object_def.dsodid', condition_id, True)
            else:
                condition = self.__condition_value_like_2_sql('dm2_storage_object_def.dsodid', condition_id, True)

            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_name = search_json_obj.xpath_one(self.Name_Name, None)
        if condition_name is not None:
            if isinstance(condition_name, list):
                condition = self.__condition_list_2_sql('dm2_storage_object_def.dsodname', condition_name, True)
            else:
                condition = self.__condition_value_like_2_sql('dm2_storage_object_def.dsodname', condition_name, True)

            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_type = search_json_obj.xpath_one(self.Name_Type, None)
        if condition_type is not None:
            if isinstance(condition_type, list):
                condition = self.__condition_list_2_sql('dm2_storage_object_def.dsodtype', condition_type, True)
            else:
                condition = self.__condition_value_like_2_sql('dm2_storage_object_def.dsodtype', condition_type, True)

            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        condition_group = search_json_obj.xpath_one(self.Name_Group, None)
        if condition_group is not None:
            if isinstance(condition_group, list):
                condition = self.__condition_list_2_sql('dm2_storage_object_def.dsodgroup', condition_group, True)
            else:
                condition = self.__condition_value_like_2_sql('dm2_storage_object_def.dsodgroup', condition_group, True)

            sql_where = CUtils.str_append(sql_where, condition, ' and ')

        if not CUtils.equal_ignore_case(sql_where, ''):
            sql_where = ' and {0}'.format(sql_where)

        sql_search = '''
        select dm2_storage_object.dsoid as object_id
            , dm2_storage_object.dsoobjectname as object_name
            , dm2_storage_object.dsoobjecttype as object_type
            , dm2_storage_object.dsodatatype as object_data_type
            , dm2_storage_object.dsoparentobjid as object_parent_id
            , dm2_storage_object.dso_volumn_now as object_size
            , dm2_storage_object.dso_obj_lastmodifytime as object_lastmodifytime
        from dm2_storage_object, dm2_storage_object_def {0} 
        where dm2_storage_object.dsoobjecttype = dm2_storage_object_def.dsodid
            and dm2_storage_object.dsoid = dm2_storage_obj_na.dson_object_id
        {1}
        '''.format(sql_from, sql_where)

        return CFactory().give_me_db(self.db_server_id).all_row(sql_search)

    def __condition_list_2_sql(self, field, value_list, quoted_value):
        if quoted_value:
            in_sql = CUtils.list_2_str(value_list, "'", ", ", "'", True)
        else:
            in_sql = CUtils.list_2_str(value_list, "", ", ", "", True)

        if CUtils.equal_ignore_case(in_sql, ''):
            return ""
        else:
            return "{0} in ({1})".format(field, in_sql)

    def __condition_value_like_2_sql(self, field, value):
        if CUtils.equal_ignore_case(value, ''):
            return ""

        return "{0} like '{0}'".format(field, value)

    def object_full_name_by_id(self, object_id: str):
        result = CFactory().give_me_db(self.db_server_id).one_value(
            '''
            select coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_file.dsffilerelationname as full_name
            from dm2_storage_object, dm2_storage_file, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id
                and dm2_storage_file.dsfstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{0}'
                and dm2_storage_object.dsoid = :object_id
            union 
            select coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_directory.dsddirectory as full_name
            from dm2_storage_object, dm2_storage_directory, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id
                and dm2_storage_directory.dsdstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{1}'
                and dm2_storage_object.dsoid = :object_id
            '''.format(self.FileType_File, self.FileType_Dir)
            , {'object_id': object_id}
        )

        if result is not None:
            return result

        ds_object_info = CFactory().give_me_db(self.db_server_id).one_row(
            '''
            select dsoobjectname, dsoparentobjid
            from dm2_storage_object
            where dsoid = :object_id and dsodatatype not in ('file', 'dir')
            '''
        )
        if ds_object_info.is_empty():
            return None

        object_name = ds_object_info.value_by_index(0, 0, '')
        object_parent_id = ds_object_info.value_by_index(0, 1, '')
        if CUtils.equal_ignore_case(object_parent_id, ''):
            return None

        result = CFactory().give_me_db(self.db_server_id).one_value(
            '''
            select coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_file.dsffilerelationname as full_name
            from dm2_storage_object, dm2_storage_file, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id
                and dm2_storage_file.dsfstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{0}'
                and dm2_storage_object.dsoid = :object_id
            union 
            select coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_directory.dsddirectory as full_name
            from dm2_storage_object, dm2_storage_directory, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id
                and dm2_storage_directory.dsdstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{1}'
                and dm2_storage_object.dsoid = :object_id
            '''.format(self.FileType_File, self.FileType_Dir)
            , {'object_id': object_parent_id}
        )
        if result is not None:
            return CFile.join_file(CUtils.any_2_str(result), object_name)
        else:
            return None

    def object_uni_full_name_by_id(self, object_id: str):
        result = CFactory().give_me_db(self.db_server_id).one_value(
            '''
            select dm2_storage.dstunipath || dm2_storage_file.dsffilerelationname as full_name
            from dm2_storage_object, dm2_storage_file, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id
                and dm2_storage_file.dsfstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{0}'
                and dm2_storage_object.dsoid = :object_id
            union 
            select dm2_storage.dstunipath || dm2_storage_directory.dsddirectory as full_name
            from dm2_storage_object, dm2_storage_directory, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id
                and dm2_storage_directory.dsdstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{1}'
                and dm2_storage_object.dsoid = :object_id
            '''.format(self.FileType_File, self.FileType_Dir)
            , {'object_id': object_id}
        )

        if result is not None:
            return result

        ds_object_info = CFactory().give_me_db(self.db_server_id).one_row(
            '''
            select dsoobjectname, dsoparentobjid
            from dm2_storage_object
            where dsoid = :object_id and dsodatatype not in ('file', 'dir')
            '''
        )
        if ds_object_info.is_empty():
            return None

        object_name = ds_object_info.value_by_index(0, 0, '')
        object_parent_id = ds_object_info.value_by_index(0, 1, '')
        if CUtils.equal_ignore_case(object_parent_id, ''):
            return None

        result = CFactory().give_me_db(self.db_server_id).one_value(
            '''
            select dm2_storage.dstunipath || dm2_storage_file.dsffilerelationname as full_name
            from dm2_storage_object, dm2_storage_file, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id
                and dm2_storage_file.dsfstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{0}'
                and dm2_storage_object.dsoid = :object_id
            union 
            select dm2_storage.dstunipath || dm2_storage_directory.dsddirectory as full_name
            from dm2_storage_object, dm2_storage_directory, dm2_storage
            where dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id
                and dm2_storage_directory.dsdstorageid = dm2_storage.dstid
                and dm2_storage_object.dsodatatype = '{1}'
                and dm2_storage_object.dsoid = :object_id
            '''.format(self.FileType_File, self.FileType_Dir)
            , {'object_id': object_parent_id}
        )
        if result is not None:
            return CFile.join_file(CUtils.any_2_str(result), object_name)
        else:
            return None
