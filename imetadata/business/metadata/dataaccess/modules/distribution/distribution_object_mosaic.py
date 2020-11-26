# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:59
# @Author : 赵宇飞
# @File : distribution_object_mosaic.py
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_mosaic(distribution_guotu_object):
    """
    邢凯凯 数据检索分发模块对镶嵌类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '镶嵌影像'
        info['table_name'] = 'ap3_product_rsp_mosaic_whole'
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

        # 后处理流程介文档中的字段
        self.add_value_to_sync_dict_list(sync_dict, 'aprmwid', object_table_id, self.DB_True)
        # sync_dict['datatype'] = "'{0}'".format()
        # sync_dict['projinfo'] = "'{0}'".format()
        # sync_dict['zonetype'] = "'{0}'".format()
        # sync_dict['centerline'] = "'{0}'".format()
        # int4
        # sync_dict['zoneno'] = "'{0}'".format()
        # sync_dict['coordinateunit'] = "'{0}'".format()
        # sync_dict['demname'] = "'{0}'".format()
        # sync_dict['demstandard'] = "'{0}'".format()
        self.add_value_to_sync_dict_list(sync_dict, 'mosaiclinefilename', object_table_data.value_by_name(0,'dsoobjectname',''))
        # sync_dict['sensors'] = "'{0}'".format()
        # sync_dict['iscuted'] = "'{0}'".format()
        # numeric
        # sync_dict['productsize'] = "'{0}'".format()
        self.add_value_to_sync_dict_list(sync_dict, 'imagesource',xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/ImageSource'))
        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml_bus', ''), self.DB_True)
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
        # 分辨率
        self.add_value_to_sync_dict_list(sync_dict, 'resolution',
                                         xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/Resolution'),
                                         self.DB_True)
        # 色彩模式
        # self.add_value_to_sync_dict_list(sync_dict, 'colormodel',xml.get_element_text_by_xpath_one(''))
        # 像素位数
        # self.add_value_to_sync_dict_list(sync_dict, 'piexldepth',xml.get_element_text_by_xpath_one(''))
        # 比例尺分母
        # self.add_value_to_sync_dict_list(sync_dict, 'scale',xml.get_element_text_by_xpath_one(''))
        # 主要星源
        # self.add_value_to_sync_dict_list(sync_dict, 'mainrssource', xml.get_element_text_by_xpath_one(''))
        # 备注
        self.add_value_to_sync_dict_list(sync_dict, 'remark', xml.get_element_text_by_xpath_one('/Metadatafile/BasicDataContent/Description'))
        return sync_dict
