# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:59
# @Author : 赵宇飞
# @File : distribution_object_mosaic.py
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_tjch_ffyx_qt(distribution_guotu_object):
    """
    邢凯凯 数据检索分发模块对天津测绘分幅影像-其他国家坐标系类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '天津测绘分幅影像-其他国家坐标系'
        # 表名待修改
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

        # 下列字段名均待修改
        self.add_value_to_sync_dict_list(sync_dict, 'aprmwid', object_table_id)
        self.add_value_to_sync_dict_list(sync_dict, 'mosaiclinefilename', xml.get_element_text_by_xpath_one(
            "//item[@name='ProductName']"))
        self.add_value_to_sync_dict_list(sync_dict, 'sensors', xml.get_element_text_by_xpath_one(
            "//item[@name='SatelliteID']"))
        self.add_value_to_sync_dict_list(sync_dict, 'dsometadatajson',
                                         object_table_data.value_by_name(0, 'dsometadataxml_bus', ''))
        self.add_value_to_sync_dict_list(sync_dict, 'resolution', xml.get_element_text_by_xpath_one(
            "//item[@name='Resolution']"))
        # self.add_value_to_sync_dict_list(sync_dict, 'regionname', xml.get_element_text_by_xpath_one(
        #     "//item[@name='GeographicName']"))
        dso_prj_project = object_table_data.value_by_name(0, 'dso_prj_project', '')
        if CUtils.equal_ignore_case(dso_prj_project, 'tj2000'):
            dso_prj_project = '2000天津城市坐标系'
        if CUtils.equal_ignore_case(dso_prj_project, 'tj1990'):
            dso_prj_project = '1990天津任意直角坐标系'
        if CUtils.equal_ignore_case(dso_prj_project, 'cgcs2000'):
            dso_prj_project = '2000国家标准坐标系'
        else:
            dataoptions = '其他国家标准坐标系'
        self.add_value_to_sync_dict_list(sync_dict, 'dataoptions', dso_prj_project)
        # 备注
        self.add_value_to_sync_dict_list(sync_dict, 'remark', xml.get_element_text_by_xpath_one(
            "//item[@name='Description']"))
        return sync_dict

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        check_dict['ProductName'] = 'ProductName'
        check_dict['DataDate'] = 'DataDate'
        check_dict['Resolution'] = 'Resolution'

        return check_dict
