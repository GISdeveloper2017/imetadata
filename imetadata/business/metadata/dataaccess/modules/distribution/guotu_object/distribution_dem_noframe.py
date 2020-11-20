# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:53
# @Author : 赵宇飞
# @File : distribution_dem_noframe.py
from imetadata.base.c_json import CJson
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_dem_noframe(distribution_guotu_object):
    """
    李宪 数据检索分发模块对DEM非分幅类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'DEM_非分幅'
        info['table_name'] = 'ap3_product_rsp_nmosaic_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，字典key为字段名，字典value为对应的值或者sql语句，在写时需要加语句号，子查询语句加(),值加‘’
        子查询：sync_dict['字段名']=“(select 字段 from 表 where id=‘1’)”
        值：sync_dict['字段名']=“‘值’”
        同时，配置插件方法时请在information()方法中添加info['table_name'] = '表名'的字段
        """

        # object_id = self._obj_id
        # object_name = self._obj_name
        return self.get_sync_xml_dict_list(insert_or_updata)

    def get_sync_xml_dict_list(self, insert_or_updata) -> list:

        object_id = self._obj_id
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        dso_time = self._dataset.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()  # 时间数据json
        dso_time_json.load_obj(dso_time)
        metadataxml_bus_xml = CXml()  # 业务元数据xml
        metadataxml_bus_xml.load_xml(dsometadataxml_bus)

        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprndid', object_id, self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprnwid', self._dataset.value_by_name(0, 'dsoparentobjid', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', self._dataset.value_by_name(0, 'dsodatatype', ''),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'project', self._dataset.value_by_name(0, 'dso_prj_project', ''),
            self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'zonationtype', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='zonationtype']"),
        #     self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'centralmeridian',
        #     metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='centralmeridian']"), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'projectbandno', self._dataset.value_by_name(0, 'projectbandno', ''), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'coordinateunit',
        #     metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='coordinateunit']"), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'demname',
        #     metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='demname']"), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'elevationdatum',
        #     metadataxml_bus_xml.get_element_text_by_xpath_one('/root/elevationdatum'), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadataxml', self._dataset.value_by_name(0, 'dsometadataxml', ''),
            self.DB_True)
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''), self.DB_True)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='secrecylevel']"),
        #     self.DB_True)    # 为空
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one('/root/resolution'),
        #     self.DB_True)    # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate', dso_time_json.xpath_one('time', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate', dso_time_json.xpath_one('start_time', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate', dso_time_json.xpath_one('end_time', ''), self.DB_True)
        return sync_dict_list