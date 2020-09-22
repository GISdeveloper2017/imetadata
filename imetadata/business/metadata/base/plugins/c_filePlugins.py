# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:50 
# @Author : 王西亚 
# @File : c_filePlugins.py
from abc import abstractmethod

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
        if self.__file_info__ is not None:
            self.__file_content__ = CVirtualContentFile(self.__file_info__.__file_name_with_full_path__)

    def classified(self):
        """
        对目标目录或文件进行分类
        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        sat_classified_character, sat_classified_character_type = self.get_classified_character()
        if sat_classified_character_type == self.TextMatchType_Common:
            if CFile.file_match(self.get_classified_text(), sat_classified_character):
                self.__object_confirm__ = self.Object_Confirm_IKnown
        elif sat_classified_character_type == self.TextMatchType_Regex:
            if CUtils.text_match_re(self.get_classified_text(), sat_classified_character):
                self.__object_confirm__ = self.Object_Confirm_IKnown

        return self.__object_confirm__, self.get_classified_object_name()

    @abstractmethod
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
        return self.__file_info__.__file_name_without_path__

    def get_classified_object_name(self):
        self.__object_name__ = self.get_classified_text()
        return self.__object_name__