# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:24 
# @Author : 王西亚 
# @File : c_satPlugins.py
from abc import abstractmethod
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.content.c_virtualContent_Package import CVirtualContentPackage
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CSatPlugins(CPlugins):
    """
    在这个类中解决卫星压缩数据包解压至目录中, 再进行检查
    . 如果卫星数据是文件, 则先检查文件名是否在指定的列表中, 之后再检查文件主名是否匹配指定特征串
    . 如果卫星数据是目录, 则直接检查目录是否匹配指定特征串
    """
    __special_file_ext_list__ = ['tar.gz', 'rar', 'zip', '7z', 'tar', 'tgz']

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = None
        information[self.Plugins_Info_Name] = None
        information[self.Plugins_Info_Code] = '000001'
        information[self.Plugins_Info_Catalog] = '卫星数据'
        information[self.Plugins_Info_Type_Title] = '原始数据'
        information[self.Plugins_Info_Type] = 'sat'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = 'global_dim'
        information[self.Plugins_Info_DetailEngine] = 'same_file_mainname'
        information[self.Plugins_Info_QCEngine] = None

        return information

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        if self.__file_info__.__file_type__ == self.FileType_File:
            if self.__special_file_ext_list__.count(self.__file_info__.__file_ext__.lower()) == 0:
                self.__object_confirm__ = self.Object_Confirm_IUnKnown
                return self.__object_confirm__, self.get_classified_object_name()

        sat_classified_character, sat_classified_character_type = self.get_classified_character()
        if sat_classified_character_type == self.TextMatchType_Common:
            if CFile.file_match(self.get_classified_text(), sat_classified_character):
                self.__object_confirm__ = self.Object_Confirm_IKnown
        elif sat_classified_character_type == self.TextMatchType_Regex:
            if CUtils.text_match_re(self.get_classified_text(), sat_classified_character):
                self.__object_confirm__ = self.Object_Confirm_IKnown

        return self.__object_confirm__, self.get_classified_object_name()

    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)

        if self.__file_info__ is not None:
            if self.__file_info__.__file_type__ == self.FileType_Dir:
                self.__file_content__ = CVirtualContentDir(self.__file_info__.__file_name_with_full_path__)
            else:
                self.__file_content__ = CVirtualContentPackage(self.__file_info__.__file_name_with_full_path__)

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
        if self.__file_info__.__file_type__ == self.FileType_Dir:
            return self.__file_info__.__file_name_without_path__
        else:
            return self.__file_info__.__file_main_name__

    def get_classified_object_name(self):
        self.__object_name__ = self.get_classified_text()
        return self.__object_name__
