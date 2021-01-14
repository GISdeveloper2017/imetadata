# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 14:48 
# @Author : 王西亚 
# @File : c_quality.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CQuality(CResource):
    __xml_obj: CXml
    # 根节点
    __xml_root_node = None

    # 整体质量节点
    __node_total = None
    # 数据质量节点
    __node_data = None
    # 数据的总体质量节点
    __node_data_items = None
    # 数据的每一个记录的质量节点, 用于矢量数据检验
    __node_data_records = None

    # 元数据质量节点
    __node_metadata = None
    # 业务元数据质量节点
    __node_metadata_bus = None
    # 数据本身的元数据质量节点
    __node_metadata_data = None

    __XPath_Root = '/root'
    __XPath_Total = '{0}/total'.format(__XPath_Root)
    __XPath_MetaData = '{0}/metadata'.format(__XPath_Root)
    __XPath_MetaData_Data = '{0}/data'.format(__XPath_MetaData)
    __XPath_MetaData_Bus = '{0}/business'.format(__XPath_MetaData)
    __XPath_Data = '{0}/data'.format(__XPath_Root)
    __XPath_Data_Items = '{0}/items'.format(__XPath_Data)

    def __init__(self):
        self.__xml_obj = CXml()
        self.__xml_root_node = self.__xml_obj.new_xml(self.Name_Root)

        self.__node_total = CXml.create_element(self.__xml_root_node, self.Name_Total)

        self.__node_data = CXml.create_element(self.__xml_root_node, self.Name_Data)
        self.__node_data_items = CXml.create_element(self.__node_data, self.Name_Items)
        self.__node_data_records = CXml.create_element(self.__node_data, self.Name_Records)

        self.__node_metadata = CXml.create_element(self.__xml_root_node, self.Name_MetaData)
        self.__node_metadata_bus = CXml.create_element(self.__node_metadata, self.Name_Business)
        self.__node_metadata_data = CXml.create_element(self.__node_metadata, self.Name_Data)

    def __append_quality_info(self, xml_node, audit_result: dict):
        quality_id = CUtils.dict_value_by_name(audit_result, self.Name_ID, '')
        quality_title = CUtils.dict_value_by_name(audit_result, self.Name_Title, '')
        quality_group = CUtils.dict_value_by_name(audit_result, self.Name_Group, self.QA_Group_Data_Integrity)
        quality_result = CUtils.dict_value_by_name(audit_result, self.Name_Result, self.QA_Result_Pass)
        quality_memo = CUtils.dict_value_by_name(audit_result, self.Name_Message, '')

        temp_node = CXml.node_xpath_one(xml_node, './{0}[@id="{1}"]'.format(self.Name_Item, quality_id))
        if temp_node is not None:
            CXml.remove(temp_node)

        temp_node = CXml.create_element(xml_node, self.Name_Item)
        CXml.set_attr(temp_node, self.Name_ID, quality_id)
        CXml.set_attr(temp_node, self.Name_Group, quality_group)
        CXml.set_attr(temp_node, self.Name_Title, quality_title)
        CXml.set_attr(temp_node, self.Name_Result, quality_result)
        CXml.set_element_text(temp_node, quality_memo)
        # 暂时不知道是否会有影响 by 王学谦
        # if temp_node is not None:
        #     old_quality_result = CXml.get_attr(temp_node, self.Name_Result, self.QA_Result_Pass, False)
        #     if CUtils.equal_ignore_case(old_quality_result, self.QA_Result_Pass) or \
        #             (CUtils.equal_ignore_case(old_quality_result, self.QA_Result_Warn) and
        #              CUtils.equal_ignore_case(quality_result, self.QA_Result_Error)):
        #         CXml.remove(temp_node)
        #         temp_node = CXml.create_element(xml_node, self.Name_Item)
        #         CXml.set_attr(temp_node, self.Name_ID, quality_id)
        #         CXml.set_attr(temp_node, self.Name_Group, quality_group)
        #         CXml.set_attr(temp_node, self.Name_Title, quality_title)
        #         CXml.set_attr(temp_node, self.Name_Result, quality_result)
        #         CXml.set_element_text(temp_node, quality_memo)
        #     # 原本错误等级更高的情况则不置换节点
        # else:
        #     temp_node = CXml.create_element(xml_node, self.Name_Item)
        #     CXml.set_attr(temp_node, self.Name_ID, quality_id)
        #     CXml.set_attr(temp_node, self.Name_Group, quality_group)
        #     CXml.set_attr(temp_node, self.Name_Title, quality_title)
        #     CXml.set_attr(temp_node, self.Name_Result, quality_result)
        #     CXml.set_element_text(temp_node, quality_memo)

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
        self.__append_quality_info(self.__node_total, audit_result)

    def append_data_quality(self, audit_result: dict):
        """
        设置数据的总体质量
        :param audit_result:
        :return:
        """
        self.__append_quality_info(self.__node_data_items, audit_result)

    def append_data_records_quality(self, record_index, audit_result: dict):
        """
        设置数据的每一个记录的质量信息
        :param record_index:
        :param audit_result:
        :return:
        """
        temp_node = CXml.node_xpath_one(
            self.__node_data_records,
            './{0}[@index="{1}"]'.format(self.Name_Record, record_index)
        )
        if temp_node is None:
            temp_node = CXml.create_element(self.__node_data_records, self.Name_Record)
        self.__append_quality_info(temp_node, audit_result)

    def append_metadata_data_quality(self, audit_result: dict):
        """
        设置实体的元数据质量检验结果
        :param audit_result:
        :return:
        """
        self.__append_quality_info(self.__node_metadata_data, audit_result)

    def append_metadata_bus_quality(self, audit_result: dict):
        """
        设置业务的元数据质量检验结果
        :param audit_result:
        :return:
        """
        self.__append_quality_info(self.__node_metadata_bus, audit_result)

    def save_as(self, file_name_with_path):
        """
        将质检结果保存为文件
        :param file_name_with_path:
        :return:
        """
        self.__xml_obj.save_file(file_name_with_path)

    def to_xml(self) -> str:
        """
        将质检结果导出为xml文本
        :return:
        """
        return self.__xml_obj.to_xml()

    def summary(self) -> str:
        json_obj = CJson()
        json_obj.set_value_of_name(
            self.Name_Total,
            self.__quality_result_of_level(self.__XPath_Total)
        )
        metadata_qa_s = {
            self.Name_Data: self.__quality_result_of_level(self.__XPath_MetaData_Data),
            self.Name_Business: self.__quality_result_of_level(self.__XPath_MetaData_Bus)
        }
        json_obj.set_value_of_name(
            self.Name_MetaData,
            metadata_qa_s
        )
        json_obj.set_value_of_name(
            self.Name_Data,
            {self.Name_Items: self.__quality_result_of_level(self.__XPath_Data_Items)}
        )
        return json_obj.to_json()

    def __quality_result_of_level(self, xpath: str):
        if self.__xml_obj.xpath_one(
                '{0}/*[@{1}="{2}"]'.format(xpath, self.Name_Result, self.QA_Result_Error)) is not None:
            return self.QA_Result_Error
        elif self.__xml_obj.xpath_one(
                '{0}/*[@{1}="{2}"]'.format(xpath, self.Name_Result, self.QA_Result_Warn)) is not None:
            return self.QA_Result_Warn
        else:
            return self.QA_Result_Pass
