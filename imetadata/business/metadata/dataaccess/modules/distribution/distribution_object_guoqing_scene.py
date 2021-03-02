# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:11
# @Author : 赵宇飞
# @File : distribution_object_guoqing_scene.py
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_guoqing_scene(distribution_guotu_object):
    """
    邢凯凯 数据检索分发模块对国情影像-整景纠正类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '国情影像-整景纠正'
        info['table_name'] = 'ap3_product_rsp_gqos_detail'
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
        self.add_value_to_sync_dict_list(sync_dict, 'aprgdid', object_table_id)
        self.add_value_to_sync_dict_list(sync_dict, 'aprgwid', object_table_data.value_by_name(0, 'dsoparentobjid', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'datatype', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/DataFormat'))
        self.add_value_to_sync_dict_list(sync_dict, 'panfilename',
                                         object_table_data.value_by_name(0, 'dsoobjectname', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'pansensorname', xml.get_element_text_by_xpath_one(
            '//PBandSensorType'))
        # numeric
        self.add_value_to_sync_dict_list(sync_dict, 'panresolution', xml.get_element_text_by_xpath_one(
            '//SateResolution'))
        self.add_value_to_sync_dict_list(sync_dict, 'pantraceno', xml.get_element_text_by_xpath_one(
            '//PBandOribitCode'))
        # self.add_value_to_sync_dict_list(sync_dict, 'panimagedate', xml.get_element_text_by_xpath_one(''))
        self.add_value_to_sync_dict_list(sync_dict, 'msfilename',
                                         object_table_data.value_by_name(0, 'dsoobjectname', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'satename',
                                         xml.get_element_text_by_xpath_one('//SateName'))
        # int4
        self.add_value_to_sync_dict_list(sync_dict, 'mssensorname', xml.get_element_text_by_xpath_one(
            '//MultiBandSensorType'))
        self.add_value_to_sync_dict_list(sync_dict, 'msresolution', xml.get_element_text_by_xpath_one(
            '//MultiBandResolution'))
        self.add_value_to_sync_dict_list(sync_dict, 'mstraceno', xml.get_element_text_by_xpath_one(
            '//MultiBandOrbitCode'))
        # self.add_value_to_sync_dict_list(sync_dict, 'msimagedate', xml.get_element_text_by_xpath_one(''))
        self.add_value_to_sync_dict_list(sync_dict, 'bandcount', xml.get_element_text_by_xpath_one(
            '//MultiBandNum'))
        self.add_value_to_sync_dict_list(sync_dict, 'bandname', xml.get_element_text_by_xpath_one(
            '//MultiBandName'))
        # self.add_value_to_sync_dict_list(sync_dict, 'bandide', xml.get_element_text_by_xpath_one(''))
        # int4
        self.add_value_to_sync_dict_list(sync_dict, 'zoneno', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/MathFoundation/GaussKrugerZoneNo'))
        # self.add_value_to_sync_dict_list(sync_dict, 'sensor', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'sensorscode', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'cloudpercent', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'istile', xml.get_element_text_by_xpath_one(''))
        # self.add_value_to_sync_dict_list(sync_dict, 'tileindex', xml.get_element_text_by_xpath_one(''))
        self.add_value_to_sync_dict_list(sync_dict, 'metafilename', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/MetaDataFileName'))
        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml_bus', ''))
        # 数据量
        self.add_value_to_sync_dict_list(sync_dict, 'datacount', 1)
        # 密级
        self.add_value_to_sync_dict_list(sync_dict, 'secrecylevel',
                                         xml.get_element_text_by_xpath_one(
                                             '/Metadatafile/BasicDataContent/ConfidentialLevel'))
        # 行政区码
        # self.add_value_to_sync_dict_list(sync_dict, 'regioncode',xml.get_element_text_by_xpath_one()
        # 行政区
        # self.add_value_to_sync_dict_list(sync_dict, 'regionname',xml.get_element_text_by_xpath_one()
        # 产品时间
        # self.add_value_to_sync_dict_list(sync_dict, 'producetime', xml.get_element_text_by_xpath_one(''))
        # 分辨率
        self.add_value_to_sync_dict_list(sync_dict, 'resolution', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/GroundResolution'))
        # 色彩模式
        self.add_value_to_sync_dict_list(sync_dict, 'colormodel', xml.get_element_text_by_xpath_one(
            '/Metadatafile/BasicDataContent/ImgColorModel'))
        # 像素位数
        self.add_value_to_sync_dict_list(sync_dict, 'piexldepth',
                                         xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/PixelBits'))
        # 比例尺分母
        # self.add_value_to_sync_dict_list(sync_dict, 'scale', xml.get_element_text_by_xpath_one(''))
        # 主要星源
        self.add_value_to_sync_dict_list(sync_dict, 'mainrssource',
                                         xml.get_element_text_by_xpath_one('//SateName'))
        # 备注
        # self.add_value_to_sync_dict_list(sync_dict, 'remark', xml.get_element_text_by_xpath_one(''))

        return sync_dict

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        check_dict['MetaDataFileName'] = 'MetaDataFileName'
        check_dict['ProductName'] = 'ProductName'
        check_dict['Owner'] = 'Owner'
        check_dict['Producer'] = 'Producer'
        check_dict['Publisher'] = 'Publisher'
        check_dict['ProduceDate'] = 'ProduceDate'
        check_dict['ConfidentialLevel'] = 'ConfidentialLevel'
        check_dict['GroundResolution'] = 'GroundResolution'
        check_dict['ImgColorModel'] = 'ImgColorModel'
        check_dict['PixelBits'] = 'PixelBits'
        check_dict['DataFormat'] = 'DataFormat'
        check_dict['MapProjection'] = 'MapProjection'
        check_dict['SateName'] = 'SateName'
        check_dict['PBandSensorType'] = 'PBandSensorType'
        check_dict['SateResolution'] = 'SateResolution'
        check_dict['PBandOribitCode'] = 'PBandOribitCode'
        check_dict['PBandDate'] = 'PBandDate'
        check_dict['MultiBandSensorType'] = 'MultiBandSensorType'
        check_dict['MultiBandResolution'] = 'MultiBandResolution'
        check_dict['MultiBandOrbitCode'] = 'MultiBandOrbitCode'
        check_dict['MultiBandDate'] = 'MultiBandDate'
        check_dict['MultiBandNum'] = 'MultiBandNum'
        check_dict['MultiBandName'] = 'MultiBandName'

        return check_dict
