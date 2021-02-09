# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:27
# @Author : 赵宇飞
# @File : plugins_8052_guoqing_frame.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing


class plugins_8052_guoqing_frame(CFilePlugins_GUOTU_GuoQing):
    """
    与国情影像-整景纠正有差别(业务元数据xml的字段),xml文件的识别也不同，也不是***_21at.xml模式，所以直接继承于CFilePlugins_GUOTU
        数据内容	    文件格式	是否有坐标系	内容样例	说明
        影像文件	    tif/TIF	有	H50E003006AP005P2011A.TIF	融合影像文件
        元数据文件	xml/XML	无	H50E003006AP005P2011M.XML	整体元数据文件
        关于正则表达式     https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '国情影像_分幅影像'
        information[self.Plugins_Info_Type_Title] = information[self.Plugins_Info_Type]
        # information[self.Plugins_Info_Name] = 'guoqing_frame'
        information[self.Plugins_Info_Type_Code] = '02010301'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_guoqing_frame'
        return information

    def classified(self):
        """
        设计国土行业数据guoqing_frame的验证规则（国情影像—分幅影像）
        完成 负责人 王学谦 在这里检验guoqing_frame的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_path = self.file_info.file_path
        file_object_name = file_main_name[:]

        if len(file_main_name) >= 21:  # 本类文件默认至少为20位
            file_object_name = file_main_name[:20]  # 截取前20位
        elif len(file_main_name) == 20:  # 20位基本为附属文件
            pass
        else:
            return self.Object_Confirm_IUnKnown, self._object_name

        match_str = '(?i)^' + file_object_name + r'[a-zA-Z][.]tif'
        check_file_main_name_exist = \
            CFile.find_file_or_subpath_of_path(file_path, match_str, CFile.MatchType_Regex)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        # 文件名第1，4，11，12，16，21位为字母，第2，3，5-10，14，15，17-20位是数字
        name_sub_1 = file_main_name[0:1]
        name_sub_2_to_3 = file_main_name[1:3]
        name_sub_4 = file_main_name[3:4]
        name_sub_5_to_10 = file_main_name[4:10]
        name_sub_11_to_12 = file_main_name[10:12]
        name_sub_14_to_15 = file_main_name[13:15]
        name_sub_16 = file_main_name[15:16]
        name_sub_17_to_20 = file_main_name[16:20]
        name_sub_21 = file_main_name[20:21]
        if CUtils.text_is_alpha(name_sub_1) is False \
                or CUtils.text_is_numeric(name_sub_2_to_3) is False \
                or CUtils.text_is_alpha(name_sub_4) is False \
                or CUtils.text_is_numeric(name_sub_5_to_10) is False \
                or CUtils.text_is_alpha(name_sub_11_to_12) is False \
                or CUtils.text_is_numeric(name_sub_14_to_15) is False \
                or CUtils.text_is_alpha(name_sub_16) is False \
                or CUtils.text_is_numeric(name_sub_17_to_20) is False \
                or CUtils.text_is_alpha(name_sub_21) is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        if len(file_main_name) == 21 and CUtils.equal_ignore_case(file_ext, 'tif'):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
            self.add_file_to_detail_list(file_object_name)  # 在这里设置不同名的附属文件
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

    def add_file_to_detail_list(self, match_name):
        """
        设定国土行业数据国情的附属文件的验证规则（镶嵌影像）
        完成 负责人 王学谦 在这里检验国情的附属文件
        :return:
        """
        file_main_name = self._object_name
        file_path = self.file_info.file_path
        # 正则匹配附属文件
        if not CUtils.equal_ignore_case(file_path, ''):
            match_str = '{0}*.*'.format(match_name)
            match_file_list = CFile.file_or_dir_fullname_of_path(file_path, False, match_str, CFile.MatchType_Common)

            ext_list = ['rar', 'zip', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'xml']
            for file_with_path in match_file_list:
                if CUtils.equal_ignore_case(CFile.file_main_name(file_with_path), file_main_name):  # 去除自身与同名文件
                    pass
                elif CFile.file_ext(file_with_path).lower() in ext_list:
                    self.add_file_to_details(file_with_path)
                else:
                    pass

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        metadata_main_name_with_path = metadata_main_name_with_path[:-1]  # 剪切文件最后的a/o
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_M = '{0}M.xml'.format(metadata_main_name_with_path)  # 三种元数据
        if CFile.file_or_path_exist(temp_metadata_bus_file_M):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_M

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
                    self.Name_Message: '业务元数据[{0}]存在'.format(
                        CFile.file_name(self.metadata_bus_src_filename_with_path)
                    )
                }
            )
