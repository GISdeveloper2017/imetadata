# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 14:48 
# @Author : 王西亚 
# @File : c_quality.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CQuality(CResource):
    __xml_obj__: CXml
    # 根节点
    __xml_root_node__ = None

    # 整体质量节点
    __node_total__ = None
    # 数据质量节点
    __node_data__ = None
    # 数据的总体质量节点
    __node_data_items__ = None
    # 数据的每一个记录的质量节点, 用于矢量数据检验
    __node_data_records__ = None

    # 元数据质量节点
    __node_metadata__ = None
    # 业务元数据质量节点
    __node_metadata_bus__ = None
    # 数据本身的元数据质量节点
    __node_metadata_data__ = None

    def __init__(self):
        self.__xml_obj__ = CXml()
        self.__xml_obj__.new_xml(self.Name_Root)
        self.__xml_root_node__ = self.__xml_obj__.__xml_root_node__

        self.__node_total__ = CXml.create_element(self.__xml_root_node__, self.Name_Total)

        self.__node_data__ = CXml.create_element(self.__xml_root_node__, self.Name_Data)
        self.__node_data_items__ = CXml.create_element(self.__node_data__, self.Name_Items)
        self.__node_data_records__ = CXml.create_element(self.__node_data__, self.Name_Records)

        self.__node_metadata__ = CXml.create_element(self.__xml_root_node__, self.Name_MetaData)
        self.__node_metadata_bus__ = CXml.create_element(self.__node_metadata__, self.Name_Business)
        self.__node_metadata_data__ = CXml.create_element(self.__node_metadata__, self.Name_Data)

    def __append_quality_info__(self, xml_node, quality_id, quality_level, quality_title, quality_result, quality_memo):
        temp_node = CXml.node_xpath_one(xml_node, './{0}[@id="{1}"]'.format(self.Name_Item, quality_id))
        if temp_node is not None:
            CXml.remove(temp_node)

        temp_node = CXml.create_element(xml_node, self.Name_Item)
        CXml.set_attr(temp_node, self.Name_ID, quality_id)
        CXml.set_attr(temp_node, self.Name_Level, quality_level)
        CXml.set_attr(temp_node, self.Name_Title, quality_title)
        CXml.set_attr(temp_node, self.Name_Result, quality_result)
        CXml.set_element_text(temp_node, quality_memo)

    def append_total_quality(self, audit_result: dict):
        """
        设置总体的质量信息
        . 质量标识: 重复的质量标识, 仅仅保留一个
        . 质量标题: 中文简述
        . 质量类型: 信息:提示;警告:警示;错误:错误, 不能继续
        . 质量描述: 质量的详细描述
        :param audit_result:
        :return:
        """
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_level = CUtils.dict_value_by_name(audit_result, self.Name_Level, 0)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')
        self.__append_quality_info__(self.__node_total__, quality_id, quality_level, quality_title, quality_result,
                                     quality_memo)

    def append_data_quality(self, audit_result: dict):
        """
        设置数据的总体质量
        :param audit_result:
        :return:
        """
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_level = CUtils.dict_value_by_name(audit_result, self.Name_Level, 0)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')
        self.__append_quality_info__(self.__node_data_items__, quality_id, quality_level, quality_title, quality_result,
                                     quality_memo)

    def append_data_records_quality(self, record_index, audit_result: dict):
        """
        设置数据的每一个记录的质量信息
        :param record_index:
        :param audit_result:
        :return:
        """
        temp_node = CXml.node_xpath_one(self.__node_data_records__,
                                        './{0}[@index="{1}"]'.format(self.Name_Record, record_index))
        if temp_node is None:
            temp_node = CXml.create_element(self.__node_data_records__, self.Name_Record)
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_level = CUtils.dict_value_by_name(audit_result, self.Name_Level, 0)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')
        self.__append_quality_info__(temp_node, quality_id, quality_level, quality_title, quality_result, quality_memo)

    def append_metadata_data_quality(self, audit_result: dict):
        """
        设置实体的元数据质量检验结果
        :param audit_result:
        :return:
        """
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_level = CUtils.dict_value_by_name(audit_result, self.Name_Level, 0)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')
        self.__append_quality_info__(self.__node_metadata_data__, quality_id, quality_level, quality_title,
                                     quality_result, quality_memo)

    def append_metadata_bus_quality(self, audit_result: dict):
        """
        设置业务的元数据质量检验结果
        :param audit_result:
        :return:
        """
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_level = CUtils.dict_value_by_name(audit_result, self.Name_Level, 0)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')
        self.__append_quality_info__(self.__node_metadata_bus__, quality_id, quality_level, quality_title,
                                     quality_result, quality_memo)

    def save_as(self, file_name_with_path):
        """
        将质检结果保存为文件
        :param file_name_with_path:
        :return:
        """
        self.__xml_obj__.save_file(file_name_with_path)

    def to_xml(self) -> str:
        """
        将质检结果导出为xml文本
        :return:
        """
        return self.__xml_obj__.to_xml()

    def quality_result(self) -> str:
        json_obj = CJson()
        for qa_level in range(self.QA_Level_Min, self.QA_Level_Max + 1):
            json_obj.set_value_of_name('level_{0}'.format(qa_level), self.quality_result_of_level(qa_level))
        return json_obj.to_json()

    def quality_result_of_level(self, qa_level):
        if self.__xml_obj__.xpath_one(
                '//*[@{0}="{1}" and {2}="{3}"]'.format(self.Name_Result, self.QA_Result_Error, self.Name_Level,
                                                       qa_level)) is not None:
            return self.QA_Result_Error
        elif self.__xml_obj__.xpath_one(
                '//*[@{0}="{1}" and {2}="{3}"]'.format(self.Name_Result, self.QA_Result_Warn, self.Name_Level,
                                                       qa_level)) is not None:
            return self.QA_Result_Warn
        else:
            return self.QA_Result_Pass
