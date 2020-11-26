# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:53
# @Author : 赵宇飞
# @File : distribution_object_dem_noframe.py
from imetadata.base.c_json import CJson
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_dem_noframe(distribution_guotu_object):
    """
    李宪 数据检索分发模块对DEM非分幅类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'DEM_非分幅'
        info['table_name'] = 'ap3_product_rsp_ndem_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        return self.get_sync_xml_dict_list(insert_or_updata)

    def get_sync_xml_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
                """
        object_id = self._obj_id
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        dso_time = self._dataset.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()  # 时间数据json
        dso_time_json.load_obj(dso_time)
        metadataxml_bus_xml = CXml()  # 业务元数据xml
        metadataxml_bus_xml.load_xml(dsometadataxml_bus)

        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprndid', object_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprnwid', self._dataset.value_by_name(0, 'dsoparentobjid', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', self._dataset.value_by_name(0, 'dsodatatype', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'projinfo', self._dataset.value_by_name(0, 'dso_prj_project', ''))
        # sync_dict_list, 'createrorganize'  # 为空
        # sync_dict_list, 'submitorganize'  # 为空
        # sync_dict_list, 'copyrightorgnize'  # 为空
        # sync_dict_list, 'supplyorganize'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'metafilename',
            '{0}_21at.xml'.format(object_name))
        # sync_dict_list, 'networksize'  # 为空
        # sync_dict_list, 'zonetype'  # 为空
        # sync_dict_list, 'centerline'  # 为空
        # sync_dict_list, 'zoneno'  # 为空
        # sync_dict_list, 'coordinateunit'  # 为空
        # sync_dict_list, 'demname'  # 为空
        # sync_dict_list, 'demstandard'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''))
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''))
        # sync_dict_list, 'secrecylevel'  # 为空
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        # sync_dict_list, 'resolution'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')))
        return sync_dict_list
