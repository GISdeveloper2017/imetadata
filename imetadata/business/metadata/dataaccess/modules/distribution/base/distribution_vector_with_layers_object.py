# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:24
# @Author : 赵宇飞
# @File : distribution_guotu_object.py

import datetime
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import \
    distribution_guotu


class distribution_vector_with_layers_object(distribution_guotu):
    """
    对象的处理基类（即时服务）
    """
    def information(self) -> dict:
        info = super().information()
        return info

    def db_access_check(self, access_Wait_flag, access_Forbid_flag, message):
        temporary_dict = dict()
        temporary_dict['dso_time'] = self._dataset.value_by_name(0, 'dso_time', '')
        temporary_dict['dso_geo_wgs84'] = self._dataset.value_by_name(0, 'dso_geo_wgs84', '')
        temporary_dict['dso_prj_proj4'] = self._dataset.value_by_name(0, 'dso_prj_proj4', '')
        for key, value in temporary_dict.items():
            if CUtils.equal_ignore_case(value, ''):
                message = message + '[数据{0}入库异常!请进行检查与修正！]'.format(key.replace('dso_', ''))
                access_Forbid_flag = self.DB_True
        return access_Wait_flag, access_Forbid_flag, message

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        return check_dict

    def get_sync_predefined_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 指明配置的是更新还是插入，-1时为插入，0为更新
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        本方法处理公共部分
        datacount:数据量 secrecylevel:密级 regioncode:行政区码 regionname:行政区 resolution:分辨率
        colormodel:色彩模式 piexldepth:像素位数 scale:比例尺分母 mainrssource:主要星源  交插件去处理
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
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dstype', '1')
        if insert_or_updata:
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

        # 空间信息
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomwkt',
            '''
            (select array_to_string(array_agg(dso_geo_wgs84), '')
            from dm2_storage_object where dsoparentobjid='{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(  # !!!无法用分割符
            sync_dict_list, 'geomobj',
            '''
            (select array_to_string(array_agg(dso_geo_wgs84), '/')
            from dm2_storage_object where dsoparentobjid='{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(  # 配置子查询，调用函数
            sync_dict_list, 'extent',
            '''
            (select array_to_string(array_agg(dso_geo_bb_native), '/')
            from dm2_storage_object where dsoparentobjid='{0}')
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerx',
            '''
            (select st_x(st_centroid(dgw.dso_geo_wgs84))::decimal(8, 2) as centerx FROM
            (select dso_geo_wgs84 from dm2_storage_object where 
            dsoparentobjid='{0}') as dgw)
            '''.format(object_table_id), self.DataValueType_SQL)

        # select array_to_string(array_agg(sty.centery), '/')
        # FROM( select st_y(st_centroid(dgw.dso_geo_wgs84))::decimal(8, 2) as centery
        # FROM (select dso_geo_wgs84 from dm2_storage_object where
        # dsoparentobjid = '7a58c05c8072334fbd613de2c82ec6cc') as dgw ) as sty
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centery',
            '''
            (select st_y(st_centroid(dgw.dso_geo_wgs84))::decimal(8, 2) as centery FROM
            (select dso_geo_wgs84 from dm2_storage_object where 
            dsoparentobjid='{0}') as dgw)
            '''.format(object_table_id), self.DataValueType_SQL)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imgsize',
            '''
            (select round((sum(dodfilesize)/1048576),2) from dm2_storage_obj_detail 
            where dodobjectid in 
            (select dsoid FROM dm2_storage_object WHERE dsoparentobjid='{0}'))
            '''.format(object_table_id), self.DataValueType_SQL)

        return sync_dict_list

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 指明配置的是更新还是插入，-1时为插入，0为更新
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        return self.get_sync_predefined_dict_list(insert_or_updata)