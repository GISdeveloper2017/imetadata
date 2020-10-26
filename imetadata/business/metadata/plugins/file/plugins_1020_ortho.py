# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:00
# @Author : 赵宇飞
# @File : plugins_1020_ortho.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_1020_ortho(CFilePlugins_GUOTU_21AT):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '单景正射'
        information[self.Plugins_Info_Name] = 'ortho'

        return information

    def classified(self):
        """
        设计国土行业数据ortho的验证规则（单景正射）
        todo 负责人 王学谦 在这里检验ortho的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数

        file_main_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
        check_file_main_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif)) or \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Img))

        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        # 检查后缀名
        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) or CUtils.equal_ignore_case(file_ext, self.Name_Img):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        todo 负责人 王学谦 在这里检验初始化ortho的质检列表
        """
        # file_main_name = self.classified_object_name()
        # file_ext = self.file_info.__file_ext__
        # file_main_name_with_path = '{0}.{1}'.format(
        #     CFile.join_file(self.file_info.__file_path__, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.__file_name_with_full_path__))  # 调用默认的规则列表

        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 元数据xml文件的检验列表
        todo 负责人 王学谦
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

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ProductName",
                self.Name_ID: 'ProductName',
                self.Name_Title: 'ProductName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ProduceDate",
                self.Name_ID: 'ProduceDate',
                self.Name_Title: 'ProduceDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ReceiveTime",
                self.Name_ID: 'ReceiveTime',
                self.Name_Title: 'ReceiveTime',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//SatelliteID",
                self.Name_ID: 'SatelliteID',
                self.Name_Title: 'SatelliteID',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Resolution",
                self.Name_ID: 'Resolution',
                self.Name_Title: 'Resolution',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Description",
                self.Name_ID: 'Description',
                self.Name_Title: 'Description',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 500
            }
        ]
