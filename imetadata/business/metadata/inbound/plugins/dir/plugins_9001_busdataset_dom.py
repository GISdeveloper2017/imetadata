# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:35 
# @Author : 王西亚 
# @File : plugins_9001_busdataset_dom.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9001_busdataset_dom(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'DOM'
        information[self.Plugins_Info_Type_Title] = 'DOM数据集'
        information[self.Plugins_Info_Type_Code] = '020105'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_dom'
        return information

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 李宪
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//DSName",
                self.Name_ID: 'DSName',
                self.Name_Title: 'DSName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ProductType",
                self.Name_ID: 'ProductType',
                self.Name_Title: 'ProductType',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_List: ['单景正射', '镶嵌影像', '国情影像_整景纠正', '国情影像_分幅影像', '三调影像', 'DOM', 'DEM_分幅', 'DEM_非分幅', '自定义影像'],
                # self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Date",
                self.Name_ID: 'Date',
                self.Name_Title: 'Date',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_nosep,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//ScaleDenominator",
                self.Name_ID: 'ScaleDenominator',
                self.Name_Title: 'ScaleDenominator',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_integer,
                self.Name_List: [1000000, 500000, 250000, 100000, 50000, 25000, 10000, 5000, 2000, 1000, 500],
                # self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Resolution",
                self.Name_ID: 'Resolution',
                self.Name_Title: 'Resolution',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                # self.Name_Width: 10
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//MajorSource",
                self.Name_ID: 'MajorSource',
                self.Name_Title: 'MajorSource',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Number: 5,
                # self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//RegionCode",
                self.Name_ID: 'RegionCode',
                self.Name_Title: 'RegionCode',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//RegionName",
                self.Name_ID: 'RegionName',
                self.Name_Title: 'RegionName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//BeginDate",
                self.Name_ID: 'BeginDate',
                self.Name_Title: 'BeginDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_month_nosep,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//EndDate",
                self.Name_ID: 'EndDate',
                self.Name_Title: 'EndDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_month_nosep,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//Remark",
                self.Name_ID: 'Remark',
                self.Name_Title: 'Remark',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            }
        ]
