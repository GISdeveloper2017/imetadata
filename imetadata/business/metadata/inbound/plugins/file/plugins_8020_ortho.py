# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:00
# @Author : 赵宇飞
# @File : plugins_8020_ortho.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_8020_ortho(CFilePlugins_GUOTU_21AT):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '单景正射'
        information[self.Plugins_Info_Type_Code] = '020101'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_ortho'
        return information

    def classified(self):
        """
        设计国土行业数据ortho的验证规则（单景正射）
        完成 负责人 王学谦 在这里检验ortho的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_object_name = file_main_name[:]
        file_name_with_full_path = self.file_info.file_name_with_full_path
        if file_name_with_full_path.endswith('_21at.xml'):
            file_object_name = file_main_name[:-5]
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)

        check_file_main_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif)) or \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Img))

        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        # 检查后缀名
        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) or CUtils.equal_ignore_case(file_ext, self.Name_Img):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            file_detail_xml = '{0}_21at.xml'.format(self.file_info.file_main_name_with_full_path)
            self.add_file_to_details(file_detail_xml)  # 将文件加入到附属文件列表中
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里检验初始化ortho的质检列表
        """
        # file_main_name = self.classified_object_name()
        # file_ext = self.file_info.file_ext
        # file_main_name_with_path = '{0}.{1}'.format(
        #     CFile.join_file(self.file_info.file_path, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表
        return list_qa

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 王学谦
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
                self.Name_XPath: "//DataDate",
                self.Name_ID: 'DataDate',
                self.Name_Title: 'DataDate',
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
