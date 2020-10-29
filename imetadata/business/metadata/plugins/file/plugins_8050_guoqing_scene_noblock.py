# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:21
# @Author : 赵宇飞
# @File : plugins_8050_guoqing_scene_noblock.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
import re


class plugins_8050_guoqing_scene_noblock(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	文件格式	是否有坐标系	内容样例	                说明
    影像文件
    （至少有一个img）	img/IMG	有	GF2398924020190510F.img	融合影像文件，xxxF-n、xxxM-n、xxxP-n为一组
                                GF2398924020190510M.img	多光谱影像文件
                                GF2398924020190510P.img	全色波段影像文件
    元数据文件	    xml/XML	无	GF2398924020190510M.XML	多光谱元数据文件
                                GF2398924020190510P.XML	全色元数据文件
                                GF2398924020190510Y.XML	整体元数据文件
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-整景纠正'
        information[self.Plugins_Info_Name] = 'guoqing_scene_noblock'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_noblock的验证规则（国情影像—非分块）,不带数字
        todo 负责人 王学谦 在这里检验guoqing_scene_noblock的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数
        file_path = self.file_info.__file_path__
        file_object_name = file_main_name[:]

        if len(file_main_name) < 11:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        if CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                r'\d{4}[01]\d[0123]\d[a-z]$'):
            file_object_name = file_main_name[:-1]
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                  r'\d{4}[01]\d[0123]\d\S+$'):
            file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)\S+$',
                                               file_main_name)
            file_object_name = file_object_name_list[0]
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                  r'[0-9]{4}[01][0-9][0123][0-9]$'):
            pass

        match_str = '(?i)^' + file_object_name + r'[FMP].img$'
        check_file_main_name_exist = CFile.find_file_or_subpath_of_path(file_path, match_str, 2)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        """文件名第1-2位为字母，最后1位是字母在F/P/M中，倒数2-9位是数字"""
        name_sub_1_to_2 = file_object_name[0:2]
        name_sub_backwards_9_to_2 = file_object_name[-8:]
        if CUtils.text_is_alpha(name_sub_1_to_2) is False \
                or CUtils.text_is_numeric(name_sub_backwards_9_to_2) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        match_str_f = '(?i)^' + file_object_name + r'[F].img$'
        match_str_fm = '(?i)^' + file_object_name + r'[FM].img$'
        name_sub_backwards_1 = file_main_name[-1:]
        if CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'f') \
                and CUtils.equal_ignore_case(file_ext, 'img'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'm') \
                and CUtils.equal_ignore_case(file_ext, 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_f, 2):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'p') \
                and CUtils.equal_ignore_case(file_ext, 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_fm, 2):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__)
        metadata_main_name_with_path = metadata_main_name_with_path[:-1]
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_Y = '{0}Y.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_M = '{0}M.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_P = '{0}P.xml'.format(metadata_main_name_with_path)
        if CFile.file_or_path_exist(temp_metadata_bus_file_Y):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_Y
        elif CFile.file_or_path_exist(temp_metadata_bus_file_M):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_M
        elif CFile.file_or_path_exist(temp_metadata_bus_file_P):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_P

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


if __name__ == '__main__':
    pass
