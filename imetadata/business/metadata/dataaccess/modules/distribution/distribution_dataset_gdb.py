# -*- coding: utf-8 -*- 
# @Time : 2020/11/23 15:51
# @Author : 赵宇飞
# @File : distribution_dataset_gdb.py
import datetime

from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import distribution_guotu


class distribution_dataset_gdb(distribution_guotu):
    """
    完成 王学谦 数据检索分发模块对gdb数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'GDB数据集'
        info['table_name'] = 'ap3_product_rsp_vp_ds'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = list()
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprid', object_table_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprvdid1', object_table_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'productname', object_table_data.value_by_name(0, 'dsoobjectname', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producttype', object_table_data.value_by_name(0, 'dsodcode', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsodatatype', object_table_data.value_by_name(0, 'dsodatatype', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'queryable', '1')
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dstype', '1')
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'isdel', '0')
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'addtime', now_time)

        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'dsnamed', object_table_data.value_by_name(0, 'dsoobjectname', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsnamed',
            '''
            (select array_to_string(array_agg(dsoobjectname), '/') 
            from dm2_storage_object where dsoparentobjid='{0}')
            '''.format(object_table_id),
            self.DataValueType_SQL)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'busitype', object_table_data.value_by_name(0, 'dsoobjecttype', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsdid', object_table_data.value_by_name(0, 'query_directory_id', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsfid', object_table_data.value_by_name(0, 'query_file_id', ''))

        # 时间信息
        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'begdate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'enddate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'imagedate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'producetime', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'imagedatetag',
            object_table_data.value_by_name(0, 'query_directory_lastmodifytime', '').replace(r'[-/\.年月日]', '')[:8])

        # 空间信息
        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'geomobj',
            '''
            (SELECT st_union (
            (select dso_geo_bb_native from dm2_storage_object where dsoparentobjid='{0}' limit 1)
            ))
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'extent',
            '''
            (SELECT st_union( 
            (select dso_geo_bb_native from dm2_storage_object where dsoparentobjid='{0}' limit 1)
            ))
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerx',
            '''
            (SELECT st_x ( st_centroid ( st_union ( 
            (select dso_geo_bb_native from dm2_storage_object where dsoparentobjid='{0}' limit 1)
            ) ) ) )
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centery',
            '''
            (SELECT st_y ( st_centroid ( st_union ( 
            (select dso_geo_bb_native from dm2_storage_object where dsoparentobjid='{0}' limit 1)
            ) ) ) )
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomwkt',
            '''
            (SELECT st_astext ( st_union ( 
            (select dso_geo_bb_native from dm2_storage_object where dsoparentobjid='{0}' limit 1)
            ) ) )
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imgsize',
            '''
            (select round((sum(dodfilesize)/1048576),2) from dm2_storage_obj_detail 
            where dodobjectid in 
            (select dsoid FROM dm2_storage_object WHERE dsoparentobjid='{0}'))
            '''.format(object_table_id), self.DataValueType_SQL)

        return sync_dict_list
