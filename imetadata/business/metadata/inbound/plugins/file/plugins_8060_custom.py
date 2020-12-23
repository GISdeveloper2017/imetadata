# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:39
# @Author : 赵宇飞
# @File : plugins_8060_custom.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_8060_custom(CFilePlugins_GUOTU_21AT):
    """
     完成 李宪
     注意5.9 自定义影像包含2中模式（***_21at.xml/无xml文件）
    数据内容	    文件格式	是否有坐标系	内容样例	        说明
    影像文件	    img/IMG
                tif/TIF	    有	    XXXXXX.img	    以影像文件为单位
    元数据文件 	xml/XML	    无	    XXXXXX_21at.xml	元数据生产工具生成
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '其它成果影像'
        # information[self.Plugins_Info_Name] = 'custom'
        information[self.Plugins_Info_Type_Code] = '020107'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_custom'
        return information

    def classified(self):
        """
        设计国土行业数据custom的验证规则（自定义影像）
        完成 负责人 李宪 在这里检验custom的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext
        file_object_name = file_main_name
        file_name_with_full_path = self.file_info.file_name_with_full_path  # 初始化需要的参数

        if file_name_with_full_path.endswith('_21at.xml'):
            file_object_name = file_main_name[:-5]

        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)
        check_file_main_name_exist_tif = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))
        check_file_main_name_exist_img = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Img))
        if (not check_file_main_name_exist_tif) and (not check_file_main_name_exist_img):
            return self.Object_Confirm_IUnKnown, self._object_name

        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) \
                or CUtils.equal_ignore_case(file_ext, self.Name_Img):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_main_name
            file_detail_xml = '{0}_21at.xml'.format(self.file_info.file_main_name_with_full_path)
            self.add_file_to_details(file_detail_xml)  # 将文件加入到附属文件列表中
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        return self._object_confirm, self._object_name

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 文件的质检列表
        完成 负责人 李宪
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
        list_qa = list()
        list_qa.extend(self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))
        return list_qa

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        xml的质检字段列表
        完成 负责人 李宪
        @return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100,
                self.Name_XPath: "//ProductName",
                self.Name_ID: 'ProductName',
                self.Name_Title: '产品名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                self.Name_XPath: "//ProduceDate",
                self.Name_ID: 'ProduceDate',
                self.Name_Title: '产品日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
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
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                self.Name_XPath: "//ReceiveTime",
                self.Name_ID: 'ReceiveTime',
                self.Name_Title: '接受时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50,
                self.Name_XPath: "//SatelliteID",
                self.Name_ID: 'SatelliteID',
                self.Name_Title: '星源',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10,
                self.Name_XPath: "//Resolution",
                self.Name_ID: 'Resolution',
                self.Name_Title: '分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 500,
                self.Name_XPath: "//Description",
                self.Name_ID: 'Description',
                self.Name_Title: '说明',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_8060_custom.FileType_File,
                            r'D:\迅雷下载\数据入库3\自定义影像\qwe124513asa.tif',
                            r'D:\迅雷下载\数据入库3\自定义影像\tif', '<root><type>dem</type></root>')
    plugins = plugins_8060_custom(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_8060_custom.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_8060_custom.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_8060_custom.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_8060_custom.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
