# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_3002_mbtiles.py

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class plugins_3002_mbtiles(CFilePlugins):
    __metadata_xml_file_name__ = None

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '二十一世纪公司切片'
        # information[self.Plugins_Info_Name] = '21at_mbtiles'
        information[self.Plugins_Info_Type_Code] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Raster
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name

        return information

    def classified(self):
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_object_name = file_main_name[:]
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)

        if CUtils.equal_ignore_case(file_ext, self.FileExt_Mbtiles):
            if CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[01HQ]\d[_][0]$') \
                    or CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[_][0]$'):  # 结尾为0
                self._object_confirm = self.Object_Confirm_IKnown
                self._object_name = file_main_name
            elif CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[01HQ]\d[_]\d+$') \
                    or CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[_]\d+$'):  # 结尾为单个字母的情况
                self._object_confirm = self.Object_Confirm_IKnown_Not
                self._object_name = None
            else:
                self._object_confirm = self.Object_Confirm_IUnKnown
                self._object_name = None
        elif CUtils.equal_ignore_case(file_ext, self.Transformer_XML) \
                and CFile.file_or_path_exist('{0}_0.mbtiles'.format(file_main_name_with_path)):
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        else:
            self._object_confirm = self.Object_Confirm_IUnKnown
            self._object_name = None

        return self._object_confirm, self._object_name

    def add_file_to_details(self, file_full_name):
        """
        追加到附属文件集合中
        """
        self._object_detail_file_full_name_list.append(file_full_name)

    def add_file_to_detail_list(self):
        """
        设定国土行业数据mosaic的附属文件的验证规则（镶嵌影像）
        完成 负责人 李宪 在这里检验mosaic的附属文件的识别规则
        :return:
        """
        file_detail_xml = '{0}.xml'.format(self.file_info.file_main_name_with_full_path[:-2])
        self.add_file_to_details(file_detail_xml)  # 将文件加入到附属文件列表中
        file_detail_mbtiles = '{0}_*.mbtiles'.format(self.file_info.file_main_name[:-2])
        if not CUtils.equal_ignore_case(self.file_info.file_path, ''):
            list_file_fullname_xq = CFile.file_or_dir_fullname_of_path(
                self.file_info.file_path,
                False,
                file_detail_mbtiles,
                CFile.MatchType_Common)  # 模糊匹配文件列表
            for list_file_fullname in list_file_fullname_xq:
                if not CUtils.equal_ignore_case(CFile.file_main_name(list_file_fullname),
                                                self.file_info.file_main_name):
                    self.add_file_to_details(list_file_fullname)  # 将文件加入到附属文件列表中

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file = '{0}.xml'.format(metadata_main_name_with_path[:-2])
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

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        完成 负责人 王学谦 在这里将业务元数据***_21at.xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_src_filename_with_path is None:
            return CResult.merge_result(
                self.Failure,
                '数据{0}无业务元数据文件，请检查数据业务元数据文件是否存在!'.format(self.file_info.file_main_name)
            )

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
