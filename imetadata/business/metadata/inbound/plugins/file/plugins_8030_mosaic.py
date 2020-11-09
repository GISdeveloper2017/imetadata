# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:03
# @Author : 赵宇飞
# @File : plugins_8030_mosaic.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_8030_mosaic(CFilePlugins_GUOTU_21AT):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '镶嵌影像'
        information[self.Plugins_Info_Name] = 'mosaic'

        return information

    def classified(self):
        """
        设计国土行业数据mosaic的验证规则（镶嵌影像）
        完成 负责人 王学谦 在这里检验mosaic的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_name_with_full_path = self.file_info.file_name_with_full_path
        file_object_name = file_main_name[:]  # 主要名称截取
        if file_name_with_full_path.endswith('_21at.xml'):  # 元数据文件的情况
            if len(file_main_name) > 5:
                file_object_name = file_main_name[:-5]
            else:
                return self.Object_Confirm_IUnKnown, self._object_name
        else:  # 矢量文件的情况
            xq_list = ['xq.shp', 'xq.shx', 'xq.dbf', 'xq.sbx', 'xq.prj', 'xq.sbn']
            for xq_end in xq_list:
                if file_name_with_full_path.lower().endswith(xq_end):
                    if len(file_main_name) > 2:
                        file_object_name = file_main_name[:-2]
                        break
                    else:
                        return self.Object_Confirm_IUnKnown, self._object_name
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)

        check_file_main_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif)) or \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Img))
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        check_file_shp_exist = CFile.file_or_path_exist('{0}xq.shp'.format(file_main_name_with_path))
        if not check_file_shp_exist:  # 检查矢量文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        # 检查后缀名
        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) or CUtils.equal_ignore_case(file_ext, self.Name_Img):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            self.add_file_to_detail_list()
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

    def add_file_to_detail_list(self):
        """
        设定国土行业数据mosaic的附属文件的验证规则（镶嵌影像）
        完成 负责人 李宪 在这里检验mosaic的附属文件的识别规则
        :return:
        """
        file_detail_xml = '{0}_21at.xml'.format(self.file_info.file_main_name_with_full_path)
        self.add_file_to_details(file_detail_xml)       #将文件加入到附属文件列表中
        file_detail_xq = '{0}xq.*'.format(self.file_info.file_main_name)
        if not CUtils.equal_ignore_case(self.file_info.file_path, ''):
            list_file_fullname_xq = CFile.file_or_dir_fullname_of_path(
                self.file_info.file_path,
                False,
                file_detail_xq,
                CFile.MatchType_Common)         #模糊匹配文件列表
            for list_file_fullname in list_file_fullname_xq:
                self.add_file_to_details(list_file_fullname)        #将文件加入到附属文件列表中

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        设定镶嵌影像的质检列表,调用默认的主文件质检列表方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里检验设定镶嵌影像的质检列表
        """
        file_main_name = self.classified_object_name()

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表
        # 获取xq.shp数据并判断完整性
        xq_shp_with_full_path = CFile.join_file(self.file_info.file_path, '{0}xq.shp'.format(file_main_name))
        list_qa.extend(
            self.init_qa_file_integrity_default_list(xq_shp_with_full_path))

        # list_qa.extend([
        #     {
        #         self.Name_FileName: '{0}xq.shp'.format(file_main_name),
        #         self.Name_ID: 'shp',
        #         self.Name_Title: 'shp文件',
        #         self.Name_Group: self.QA_Group_Data_Integrity,
        #         self.Name_Result: self.QA_Result_Error,
        #         self.Name_Format: self.DataFormat_Vector_File
        #     }, {
        #         self.Name_FileName: '{0}xq.shx'.format(file_main_name),
        #         self.Name_ID: 'shx',
        #         self.Name_Title: 'shx文件',
        #         self.Name_Group: self.QA_Group_Data_Integrity,
        #         self.Name_Result: self.QA_Result_Error
        #     }, {
        #         self.Name_FileName: '{0}xq.dbf'.format(file_main_name),
        #         self.Name_ID: 'dbf',
        #         self.Name_Title: 'dbf文件',
        #         self.Name_Group: self.QA_Group_Data_Integrity,
        #         self.Name_Result: self.QA_Result_Error
        #     }, {
        #         self.Name_FileName: '{0}xq.sbx'.format(file_main_name),
        #         self.Name_ID: 'sbx',
        #         self.Name_Title: 'sbx文件',
        #         self.Name_Group: self.QA_Group_Data_Integrity,
        #         self.Name_Result: self.QA_Result_Warn
        #     }, {
        #         self.Name_FileName: '{0}xq.prj'.format(file_main_name),
        #         self.Name_ID: 'prj',
        #         self.Name_Title: 'prj文件',
        #         self.Name_Group: self.QA_Group_Data_Integrity,
        #         self.Name_Result: self.QA_Result_Warn
        #     }
        # ])
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
                self.Name_XPath: "//ImageSource",
                self.Name_ID: 'ImageSource',
                self.Name_Title: 'ImageSource',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
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
