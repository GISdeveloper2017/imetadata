# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:07
# @Author : 赵宇飞
# @File : distribution_object_ortho.py
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_ortho(distribution_guotu_object):
    """
    邢凯凯 数据检索分发模块对单景正射类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '单景正射'
        info['table_name'] = 'ap3_product_rsp_os_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_id = self._obj_id
        object_table_data = self._dataset

        # 业务元数据
        dsometadataxml_bus = object_table_data.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)

        # 后处理流程介绍文档中的字段
        if insert_or_updata:
            self.add_value_to_sync_dict_list(sync_dict, 'aprodid', object_table_id, self.DB_True)
        self.add_value_to_sync_dict_list(sync_dict, 'aprowid', object_table_data.value_by_name(0, 'dsoparentobjid', ''),
                                         self.DB_True)
        self.add_value_to_sync_dict_list(sync_dict, 'sataname', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/SatelliteID'), self.DB_True)
        dsoobjectname = object_table_data.value_by_name(0, 'dsoobjectname', '')
        resolution = xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/Resolution')
        if 'pan' in CUtils.text_to_lower(dsoobjectname):

            self.add_value_to_sync_dict_list(sync_dict, 'panfilename', dsoobjectname, self.DB_True)

            self.add_value_to_sync_dict_list(sync_dict, 'panresolution', resolution, self.DB_True)

            self.add_value_to_sync_dict_list(sync_dict, 'panimagedate', xml.get_element_text_by_xpath_one(
                '/Metadatafile/BasicDataContent/ReceiveTime'), self.DB_True)

            self.add_value_to_sync_dict_list(sync_dict, 'fusefilename', dsoobjectname, self.DB_True)
        else:

            self.add_value_to_sync_dict_list(sync_dict, 'msfilename', dsoobjectname, self.DB_True)
            # sync_dict['mssensorname'] = "''"

            self.add_value_to_sync_dict_list(sync_dict, 'msresolution', resolution, self.DB_True)
            # sync_dict['mstraceno'] = "''"

            self.add_value_to_sync_dict_list(sync_dict, 'msimagedate', xml.get_element_text_by_xpath_one(
                '/Metadatafile/BasicDataContent/ReceiveTime'), self.DB_True)
            # sync_dict['fusefilename'] = "''"

        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml_bus', ''), self.DB_True)
        # sync_dict['bandcount'] = "''"
        # sync_dict['bandname'] = "''"
        # sync_dict['cloudpercent'] = "''"

        # 数据量
        # sync_dict['datacount'] = "''"
        # 密级
        # sync_dict['secrecylevel'] = "''"
        # 行政区码
        # sync_dict['regioncode'] = "''"
        # 行政区
        # sync_dict['regionname'] = "''"
        # 产品时间
        # sync_dict['producetime'] = "'{0}'".format(
        #    xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/ProduceDate'))
        # resolution
        self.add_value_to_sync_dict_list(sync_dict, 'resolution', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/Resolution'), self.DB_True)
        # 色彩模式
        # sync_dict['colormodel'] = "''"
        # 像素位数
        # sync_dict['piexldepth'] = "''"
        # 比例尺分母
        # sync_dict['scale'] = "''"
        # 主要星源
        self.add_value_to_sync_dict_list(sync_dict, 'mainrssource', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/SatelliteID'), self.DB_True)
        self.add_value_to_sync_dict_list(sync_dict, 'remark', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/Description'), self.DB_True)

        return sync_dict
