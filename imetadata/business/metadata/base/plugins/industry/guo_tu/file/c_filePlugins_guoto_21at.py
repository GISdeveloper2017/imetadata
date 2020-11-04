# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 13:28
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_21at.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_21AT(CFilePlugins_GUOTU):
    """
    todo 赵宇飞 业务元数据为***_21at.xml模式的基础类，用于插件识别业务元数据文件、设置业务元数据对象的通用方法
    涉及的插件类别为：
        5.1 单景正射（***_21at.xml）
        5.2 镶嵌影像（***_21at.xml）
        5.8 DEM-非分幅影像（***_21at.xml）
        5.9 自定义影像（***_21at.xml/无xml文件）
    """
    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将业务元数据***_21at.xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_src_filename_with_path is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        transformer = CMDTransformerCommon(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file = '{0}_21at.xml'.format(metadata_main_name_with_path)
        if CFile.file_or_path_exist(temp_metadata_bus_file):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file

        if not check_file_metadata_bus_exist:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(self.metadata_bus_src_filename_with_path)
                }
            )

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '//ProduceDate',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '//ProduceDate',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '//ProduceDate',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]