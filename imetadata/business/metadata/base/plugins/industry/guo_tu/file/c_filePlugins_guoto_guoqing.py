# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:22
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_guoqing.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_GuoQing(CFilePlugins_GUOTU):
    """
    国情影像
    """

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将业务元数据xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        pass

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        :param parser:
        :return:
        """
        pass

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []