# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 14:48 
# @Author : 王西亚 
# @File : c_quality.py
from imetadata.base.c_resource import CResource
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

    def __append_quality_info__(self, xml_node, quality_id, quality_title, quality_type, quality_memo):
        temp_node = CXml.node_xpath_one(xml_node, './{0}[@id="{1}"]'.format(self.Name_Item, quality_id))
        if temp_node is not None:
            CXml.remove(temp_node)

        temp_node = CXml.create_element(xml_node, self.Name_Item)
        CXml.set_attr(temp_node, self.Name_ID, quality_id)
        CXml.set_attr(temp_node, self.Name_Title, quality_title)
        CXml.set_attr(temp_node, self.Name_Type, quality_type)
        CXml.set_element_text(temp_node, quality_memo)

    def append_total_quality(self, quality_id, quality_title, quality_type, quality_memo):
        """
        设置总体的质量信息
        . 质量标识: 重复的质量标识, 仅仅保留一个
        . 质量标题: 中文简述
        . 质量类型: 信息:提示;警告:警示;错误:错误, 不能继续
        . 质量描述: 质量的详细描述
        :param quality_id:
        :param quality_title:
        :param quality_type:
        :param quality_memo:
        :return:
        """
        self.__append_quality_info__(self.__node_total__, quality_id, quality_title, quality_type, quality_memo)

    def append_data_quality(self, quality_id, quality_title, quality_type, quality_memo):
        """
        设置数据的总体质量
        :param quality_id:
        :param quality_title:
        :param quality_type:
        :param quality_memo:
        :return:
        """
        self.__append_quality_info__(self.__node_data_items__, quality_id, quality_title, quality_type, quality_memo)

    def append_data_records_quality(self, record_index, quality_title, quality_type, quality_memo):
        """
        设置数据的每一个记录的质量信息
        :param record_index: 记录索引
        :param quality_title:
        :param quality_type:
        :param quality_memo:
        :return:
        """
        self.__append_quality_info__(self.__node_data_records__, record_index, quality_title, quality_type, quality_memo)

    def append_metadata_data_quality(self, quality_id, quality_title, quality_type, quality_memo):
        """
        设置实体的元数据质量检验结果
        :param quality_id:
        :param quality_title:
        :param quality_type:
        :param quality_memo:
        :return:
        """
        self.__append_quality_info__(self.__node_metadata_data__, quality_id, quality_title, quality_type, quality_memo)

    def append_metadata_bus_quality(self, quality_id, quality_title, quality_type, quality_memo):
        """
        设置业务的元数据质量检验结果
        :param quality_id:
        :param quality_title:
        :param quality_type:
        :param quality_memo:
        :return:
        """
        self.__append_quality_info__(self.__node_metadata_bus__, quality_id, quality_title, quality_type, quality_memo)


if __name__ == '__main__':
    quality_obj = CQuality()
    quality_obj.append_total_quality('total_id', 'total_title', 'warn', 'total_memo')
    quality_obj.append_total_quality('total_id', 'total_title', 'error', 'total_memo')
    quality_obj.append_data_quality('data_id', 'data_title', 'error', 'data_memo')
    quality_obj.append_metadata_data_quality('metadata_data_id', 'metadata_data_title', 'error', 'metadata_data_memo')
    quality_obj.append_metadata_bus_quality('metadata_data_id', 'metadata_data_title', 'error', 'metadata_data_memo')
    quality_obj.__xml_obj__.save_file('/Users/wangxiya/Downloads/test/a.xml')
