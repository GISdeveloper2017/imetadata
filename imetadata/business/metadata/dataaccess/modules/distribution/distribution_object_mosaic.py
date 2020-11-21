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
        info['table_name'] = 'ap3_product_rsp_nmosaic_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，字典key为字段名，字典value为对应的值或者sql语句，在写时需要加语句号，子查询语句加(),值加‘’
        子查询：sync_dict['字段名']=“(select 字段 from 表 where id=‘1’)”
        值：sync_dict['字段名']=“‘值’”
        同时，配置插件方法时请在information()方法中添加info['table_name'] = '表名'的字段
        """
        sync_dict = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_id = self._obj_id
        object_table_data = self._dataset

        # 业务元数据
        dsometadataxml_bus = object_table_data.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)

        # 后处理流程介文档中的字段
        self.add_value_to_sync_dict_list(sync_dict, 'aprndid', object_table_id, self.DB_True)

        self.add_value_to_sync_dict_list(sync_dict, 'aprnwid', object_table_data.value_by_name(0, 'dsoparentobjid', ''),
                                         self.DB_True)

        # sync_dict['dataformat'] = "'{0}'".format()
        # sync_dict['project'] = "'{0}'".format()
        # sync_dict['zonationtype'] = "'{0}'".format()
        # sync_dict['centralmeridian'] = "'{0}'".format()
        # sync_dict['projectbandno'] = "'{0}'".format()
        # sync_dict['coordinateunit'] = "'{0}'".format()
        # sync_dict['demname'] = "'{0}'".format()
        # sync_dict['elevationdatum'] = "'{0}'".format()

        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml', ''), self.DB_True)
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
        # sync_dict['colormodel'] = "''"
        # 像素位数
        # sync_dict['piexldepth'] = "''"
        # 比例尺分母
        # sync_dict['scale'] = "''"
        # 主要星源
        # sync_dict['mainrssource'] = "''"

        return sync_dict
