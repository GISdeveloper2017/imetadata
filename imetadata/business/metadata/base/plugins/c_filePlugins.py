# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:50 
# @Author : 王西亚 
# @File : c_filePlugins.py

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent_File import CVirtualContentFile
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CFilePlugins(CPlugins):
    """
    常规文件识别插件
    """

    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)
        if self.file_info is not None:
            self.__file_content__ = CVirtualContentFile(self.file_info.__file_name_with_full_path__)

    def classified(self):
        """
        对目标目录或文件进行分类
        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        return self.classified_by_character_common()

    def get_classified_character(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return '', self.TextMatchType_Common

    def get_classified_text(self):
        """
        获取待识别验证的字符串
        :return:
        """
        return self.file_info.__file_name_without_path__

    def classified_object_name(self):
        """
        设置默认的识别出的对象名称
        :return:
        """
        self._object_name = self.file_info.__file_main_name__
        return self._object_name

    def classified_by_character_common(self):
        """
        默认的识别模式
        根据文件名的特征, 进行对象类型识别

        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        self._object_confirm = self.Object_Confirm_IUnKnown
        sat_classified_character, sat_classified_character_type = self.get_classified_character()
        if sat_classified_character_type == self.TextMatchType_Common:
            if CFile.file_match(self.get_classified_text(), sat_classified_character):
                self._object_confirm = self.Object_Confirm_IKnown
        elif sat_classified_character_type == self.TextMatchType_Regex:
            if CUtils.text_match_re(self.get_classified_text(), sat_classified_character):
                self._object_confirm = self.Object_Confirm_IKnown

        return self._object_confirm, self.classified_object_name()
