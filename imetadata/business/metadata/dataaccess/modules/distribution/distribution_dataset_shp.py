# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 17:02
# @Author : 赵宇飞
# @File : distribution_dataset_ortho.py
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_dataset import \
    distribution_guotu_dataset
import datetime


class distribution_dataset_shp(distribution_guotu_dataset):
    """
    完成 数据检索分发模块对单景正射数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'shp数据集'
        info['table_name'] = 'ap3_product_rsp_vp_ds'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_id = self._obj_id
        object_table_data = self._dataset
        dsometadataxml = object_table_data.value_by_name(0, 'dsometadataxml_bus', '')
        dsometadataxml_xml = CXml()
        dsometadataxml_xml.load_xml(dsometadataxml)  # 加载查询出来的xml
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprvdid1', object_table_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsnamed',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/DSName'))  # 配置字段值
        if insert_or_updata:
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'adddate', now_time)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsdate',
            CUtils.to_day_format(dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date'), ''))
        regioncode = dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionCode')
        self.add_value_to_sync_dict_list(  # regioncode:行政区码
            sync_dict_list, 'dsregionno', regioncode)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'busitype', 'shp')
        self.add_value_to_sync_dict_list(  # regionname:行政区
            sync_dict_list, 'dsregionname',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionName'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dstype', '1')
        return sync_dict_list
