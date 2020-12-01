# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:10
# @Author : 赵宇飞
# @File : distribution_object_custom.py
from imetadata.base.c_json import CJson
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_custom(distribution_guotu_object):
    """
    完成 李宪 数据检索分发模块对自定义影像类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '自定义影像'
        info['table_name'] = 'ap3_product_rsp_nmosaic_detail'
        return info

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        pass

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
            sync_dict_list, 'project', self._dataset.value_by_name(0, 'dso_prj_project', ''))
        # sync_dict_list, 'zonationtype'  # 为空
        # sync_dict_list, 'centralmeridian'  # 为空
        # sync_dict_list, 'projectbandno'  # 为空
        # sync_dict_list, 'coordinateunit'  # 为空
        # sync_dict_list, 'demname'  # 为空
        # sync_dict_list, 'elevationdatum'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson',
            self._dataset.value_by_name(0, 'dsometadataxml_bus', ''))
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
