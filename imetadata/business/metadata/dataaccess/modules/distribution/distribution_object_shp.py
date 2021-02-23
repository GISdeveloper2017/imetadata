# -*- coding: utf-8 -*- 
# @Time : 2020/11/20 18:27
# @Author : 赵宇飞
# @File : distribution_object_vector.py
import datetime

from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import distribution_guotu


class distribution_object_shp(distribution_guotu):
    """
    完成 王学谦 数据检索分发模块对shp类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'shp矢量'
        info['table_name'] = 'ap3_product_rsp_vp_detail'
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
            sync_dict_list, 'apvid', object_table_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'productname', object_table_data.value_by_name(0, 'dsoobjectname', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producttype', self._obj_type_code)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsodatatype', object_table_data.value_by_name(0, 'dsodatatype', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'queryable', '0')
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'isdel', '0')
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'addtime', now_time)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsno', object_table_data.value_by_name(0, 'dsoparentobjid', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dtype', object_table_data.value_by_name(0, 'dsoobjecttype', ''))

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'projectcoordinate',
            '''
            (SELECT 
            split_part( ( dsometadatajson -> 'layers' ->> 0 ) :: json -> 'wkt' ->> 'data', '"', 2 ) 
            AS process_md_coordinate FROM  dm2_storage_object  
            WHERE  dsometadatajson IS NOT NULL AND dsoid = '{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'geometrytype',
            '''
            (SELECT 
            ( dsometadatajson -> 'layers' ->> 0 ) :: json -> 'geometry' ->> 'name' 
            AS process_md_geomtype FROM  dm2_storage_object  
            WHERE  dsometadatajson IS NOT NULL AND dsoid = '{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'tbcount',
            '''
            (SELECT 
            cast((( dsometadatajson -> 'layers' ->> 0 ) :: json -> 'features' ->> 'count' ) as integer )
            AS process_md_tbcount FROM  dm2_storage_object  
            WHERE  dsometadatajson IS NOT NULL AND dsoid = '{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomwkt',
            "st_astext("
            "(select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')"
            ")".format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsdid', object_table_data.value_by_name(0, 'query_directory_id', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsfid', object_table_data.value_by_name(0, 'query_file_id', ''))

        # 时间信息
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producetime', object_table_data.value_by_name(0, 'query_directory_lastmodifytime', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedatetag',
            self.transform_time_to_imagedatetag(
                object_table_data.value_by_name(0, 'query_directory_lastmodifytime', '')
            )
        )

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerx',
            "st_x(st_centroid("
            "(select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')"
            "))".format(object_table_id), self.DataValueType_SQL)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centery',
            "st_y(st_centroid("
            "(select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')"
            "))".format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution',
            '''
            (SELECT dsometadatajson->'pixelsize'->>'width' FROM dm2_storage_object 
            where dsometadatajson->'pixelsize'->>'width'> '0.1' is not null and dsoid = '{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        return sync_dict_list
