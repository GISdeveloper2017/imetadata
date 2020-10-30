# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:26
# @Author : 赵宇飞
# @File : plugins_8051_guoqing_scene_block.py

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
import re


class plugins_8051_guoqing_scene_block(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	    文件格式	是否有坐标系	内容样例	                    说明
    影像文件
    （影像分块）	img/IMG	有	    GF2398924020190510F-1.img	分块影像文件，全色、多光谱、融合至少包含一种类型IMG，支持多块分割
                                GF2398924020190510F-2.img   优先顺序: F、P、M
                                GF2398924020190510M-1.img
                                GF2398924020190510M-2.img
                                GF2398924020190510P-1.img
                                GF2398924020190510P-2.img
    元数据文件	xml/XML	无	    GF2398924020190510M.XML	    元数据文件优先顺序: Y、P、M
                                GF2398924020190510P.XML
                                GF2398924020190510Y.XML
    关于正则表达式     https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-整景纠正'
        information[self.Plugins_Info_Name] = 'guoqing_scene_block'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_block的验证规则（国情影像—分块）,带数字 F-1/F-2
        todo 负责人 王学谦 在这里检验guoqing_scene_block的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数
        file_path = self.file_info.__file_path__
        file_object_name = file_main_name[:]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母等字符的名

        # 正则表达式，(?i)代表大小写不敏感，^代表字符串开头，$代表字符串结尾
        # [a-z]指匹配所有小写字母，配合(?i)匹配所有字母，{2}代表前面的匹配模式匹配2次，即[a-z]{2}匹配两个字母
        # \d匹配数字，即[0-9]，即\d+匹配一个或多个非空字符，\d{4}匹配四个任意数字
        # [0123]一般指匹配一个括号中任意字符，即匹配0到3
        # \S用于匹配所有非空字符，+代表匹配前面字符的数量为至少一个，即\S+匹配一个或多个非空字符
        if len(file_main_name) < 13:
            return self.Object_Confirm_IUnKnown, self.__object_name__
        # 下面正则：开头两个字母，字母后任意数量字符,而后匹配8位时间，4位任意数字（年份），[01]\d为月份，[0123]\d日
        if CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                r'\d{4}[01]\d[0123]\d[a-z][-]\d+$'):  # [a-z][-]\d+$结尾为字母-数字
            # re.findall获取在正则表达式中所加括号，括号中的字符，这里去剔除结尾字母-数字后的字符
            file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)[a-z][-]\d+$',
                                               file_main_name)
            file_object_name = file_object_name_list[0]
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 尾部只有单个字母的情况
                                                  r'\d{4}[01]\d[0123]\d[a-z]$'):
            file_object_name = file_main_name[:-1]
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 尾部无字母，但是有任意附加字符的情况
                                                  r'\d{4}[01]\d[0123]\d\S+$'):
            file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)\S+$',
                                               file_main_name)
            file_object_name = file_object_name_list[0]
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 其他情况默认取原本主名
                                                  r'[0-9]{4}[01][0-9][0123][0-9]$'):
            pass

        match_str = '(?i)^' + file_object_name + r'[FMP][-]\d+.img$'
        check_file_main_name_exist = \
            CFile.find_file_or_subpath_of_path(file_path, match_str, CFile.MatchType_Regex)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        """文件名第1-2位为字母，倒数1-3位是在F-1/P-1/M-1中，倒数4-11位是数字"""
        name_sub_1_to_2 = file_object_name[0:2]
        name_sub_backwards_11_to_4 = file_object_name[-8:]
        if CUtils.text_is_alpha(name_sub_1_to_2) is False \
                or CUtils.text_is_numeric(name_sub_backwards_11_to_4) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__
        # 取得尾部的字母
        name_sub_backwards_fmp_list = re.findall(r'(?i)^[a-z]{2}\S+\d{4}[01]\d[0123]\d([a-z])[-]\d+$',
                                                 file_main_name)
        # 取得尾部的数字
        name_sub_backwards_num_list = re.findall(r'(?i)^[a-z]{2}\S+\d{4}[01]\d[0123]\d[a-z][-](\d+)$',
                                                 file_main_name)
        # 如果尾部没有数字与字母，但是已经通过前面的过滤，则默认为附属文件
        if len(name_sub_backwards_fmp_list) > 0 and len(name_sub_backwards_num_list) > 0:
            name_sub_backwards_fmp = name_sub_backwards_fmp_list[0]
            name_sub_backwards_num = name_sub_backwards_num_list[0]
            match_str_f = '(?i)^' + file_object_name + r'[F][-][' + name_sub_backwards_num + '].img$'
            match_str_fm = '(?i)^' + file_object_name + r'[FM][-][' + name_sub_backwards_num + '].img$'
            # 作为对象的主文件存在优先级，F-M-P,比如需要F的文件不存在，M才能是主文件
            if CUtils.equal_ignore_case(name_sub_backwards_fmp.lower(), 'f') \
                    and CUtils.equal_ignore_case(file_ext, 'img'):
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = file_main_name
            elif CUtils.equal_ignore_case(name_sub_backwards_fmp.lower(), 'm') \
                    and CUtils.equal_ignore_case(file_ext, 'img') \
                    and not CFile.find_file_or_subpath_of_path(file_path, match_str_f, CFile.MatchType_Regex):
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = file_main_name
            elif CUtils.equal_ignore_case(name_sub_backwards_fmp.lower(), 'p') \
                    and CUtils.equal_ignore_case(file_ext, 'img') \
                    and not CFile.find_file_or_subpath_of_path(file_path, match_str_fm, CFile.MatchType_Regex):
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = file_main_name
            else:
                self.__object_confirm__ = self.Object_Confirm_IKnown_Not
                self.__object_name__ = None
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
        file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)[a-z][-]\d+$',
                                           self.file_info.__file_main_name__)
        file_object_name = file_object_name_list[0]  # 去除尾部的F/M/P-数字
        metadata_main_name_with_path = CFile.join_file(self.file_info.__file_path__, file_object_name)

        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_Y = '{0}Y.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_M = '{0}M.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_P = '{0}P.xml'.format(metadata_main_name_with_path)
        if CFile.file_or_path_exist(temp_metadata_bus_file_Y):  # 存在Y-M-P的优先级
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
