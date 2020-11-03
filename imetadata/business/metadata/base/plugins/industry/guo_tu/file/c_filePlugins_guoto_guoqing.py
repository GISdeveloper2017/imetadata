# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:22
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_guoqing.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_GuoQing(CFilePlugins_GUOTU):
    """
    国情影像
    """

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化国情文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        todo 负责人 王学谦 在这里检验初始化国情的质检列表
        """
        # file_main_name = self.classified_object_name()
        # file_ext = self.file_info.file_ext
        # file_main_name_with_path = '{0}.{1}'.format(
        #     CFile.join_file(self.file_info.file_path, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表

        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return [
            {
                self.Name_XPath: 'pixelsize.width',
                self.Name_ID: 'pixelsize.width',
                self.Name_Title: '影像宽度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer_positive
            }, {
                self.Name_XPath: "coordinate",
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标系参考存在',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000
            }, {
                self.Name_XPath: "boundingbox.top",
                self.Name_ID: 'boundingbox.top',
                self.Name_Title: '经纬度坐标（top）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }, {
                self.Name_XPath: "boundingbox.left",
                self.Name_ID: 'boundingbox.left',
                self.Name_Title: '经纬度坐标（left）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.right",
                self.Name_ID: 'boundingbox.right',
                self.Name_Title: '经纬度坐标（right）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.bottom",
                self.Name_ID: 'boundingbox.bottom',
                self.Name_Title: '经纬度坐标（bottom）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将业务元数据***Y/M/P.xml, 存储到parser.metadata.set_metadata_bus_file中
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

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//ProduceDate",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//ProduceDate",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//ProduceDate",
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]
