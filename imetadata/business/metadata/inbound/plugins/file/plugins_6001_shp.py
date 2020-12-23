# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:25 
# @Author : 王西亚 
# @File : plugins_6001_shp.py.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.common.c_vectorFilePlugins import CVectorFilePlugins


class plugins_6001_shp(CVectorFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'shp'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        # information[self.Plugins_Info_Group_Name] = self.DataGroup_Vector
        # information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_shp'
        return information

    def classified(self):
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_object_name = file_main_name[:]
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)

        if CUtils.equal_ignore_case(file_ext, self.Name_Shp):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        else:
            if CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Shp)):
                self._object_confirm = self.Object_Confirm_IKnown_Not
                self._object_name = None
            else:
                self._object_confirm = self.Object_Confirm_IUnKnown
                self._object_name = None

        return self._object_confirm, self._object_name

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 文件的质检列表
        质检项目应包括并不限于如下内容:
        1. 实体数据的附属文件是否完整, 实体数据是否可以正常打开和读取
        1. 元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        1. 业务元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        示例:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]
        :param parser:
        :return:
        """
        return self.init_qa_file_integrity_default_list(
            self.file_info.file_name_with_full_path)  # 调用默认的规则列表,对对象及其附属文件进行质检

    def init_qa_metadata_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_bus_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式业务元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        完成 负责人 李宪
        :param parser:
        :return:
        """
        return [
            # {
            #     self.Name_Type: self.QA_Type_XML_Node_Exist,
            #     self.Name_NotNull: True,
            #     self.Name_DataType: self.value_type_decimal_or_integer_positive,
            #     self.Name_XPath: 'pixelsize.width',
            #     self.Name_ID: 'width',
            #     self.Name_Title: '影像宽度',
            #     self.Name_Group: self.QA_Group_Data_Integrity,
            #     self.Name_Result: self.QA_Result_Error
            # },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000,
                self.Name_XPath: 'layers[0].wgs84.coordinate',
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标参考系',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'layers[0].wgs84.extent.maxy',
                self.Name_ID: 'maxy',
                self.Name_Title: 'maxy',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'layers[0].wgs84.extent.maxx',
                self.Name_ID: 'maxx',
                self.Name_Title: 'maxx',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'layers[0].wgs84.extent.minx',
                self.Name_ID: 'minx',
                self.Name_Title: 'minx',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'layers[0].wgs84.extent.miny',
                self.Name_ID: 'miny',
                self.Name_Title: 'miny',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Not_List: ['0'],
                self.Name_XPath: 'layers[0].features.count',
                self.Name_ID: 'features_count',
                self.Name_Title: 'features_count',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            }
        ]
