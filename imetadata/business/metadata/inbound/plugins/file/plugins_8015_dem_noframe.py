# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:24
# @Author : 赵宇飞
# @File : plugins_8015_dem_noframe.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_8015_dem_noframe(CFilePlugins_GUOTU_21AT):
    """
    完成 负责人 李宪
    数据内容	    文件格式	    是否有坐标系	内容样例	            说明
    影像文件	    img/IMG
                tif/TIF	    有	    XXXX区域5米DEM.img	    以影像文件为单位
    元数据文件 	xml/XML	    无	    XXXX区域5米DEM_21at.xml	元数据生产工具生成
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'DEM_非分幅'
        # information[self.Plugins_Info_Name] = 'dem_noframe'
        information[self.Plugins_Info_Type_Code] = '02010602'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_dem_noframe'
        return information

    def classified(self):
        """
        设计国土行业数据的dem_noframe非分幅数据的验证规则
        完成 负责人 李宪 在这里检验dem_noframe的识别规则
        :return:
        """
        super().classified()
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        check_file_main_name_exist_tif = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))
        check_file_main_name_exist_img = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Img))
        if (not check_file_main_name_exist_tif) and (not check_file_main_name_exist_img):
            return self.Object_Confirm_IUnKnown, self._object_name

        if CUtils.equal_ignore_case(self.file_info.file_ext, self.Name_Tif) \
                or CUtils.equal_ignore_case(self.file_info.file_ext, self.Name_Img):
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

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 李宪
        :param parser:
        :return:
        """
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
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据，是正常现象'
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

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        完成 负责人 王学谦 在这里将业务元数据***Y/M/P.xml, 存储到parser.metadata.set_metadata_bus_file中
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

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        xml的质检字段列表
        完成 负责人 李宪
        @return:
        """
        file_name_with_full_path = self.file_info.file_name_with_full_path
        if file_name_with_full_path.endswith('_21at.xml'):
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
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8,
                    self.Name_XPath: "//GridCellSize",
                    self.Name_ID: 'GridCellSize',
                    self.Name_Title: '网格尺寸',
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
        else:
            return []

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        file_name_with_full_path = self.file_info.file_name_with_full_path
        if file_name_with_full_path.endswith('_21at.xml'):
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
        else:
            return []


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_8015_dem_noframe.FileType_File,
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\6369.0-796.0\6369.0-796.0.tif',
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\6369.0-796.0\tif', '<root><type>dem</type></root>')
    plugins = plugins_8015_dem_noframe(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_8015_dem_noframe.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_8015_dem_noframe.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_8015_dem_noframe.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_8015_dem_noframe.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
