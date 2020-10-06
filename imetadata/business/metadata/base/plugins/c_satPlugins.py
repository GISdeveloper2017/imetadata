# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:24 
# @Author : 王西亚 
# @File : c_satPlugins.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.content.c_virtualContent_Package import CVirtualContentPackage
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CSatPlugins(CPlugins):
    """
    卫星数据插件
    . 如果卫星数据是文件, 则先检查文件名是否在指定的列表中, 之后再检查文件主名是否匹配指定特征串
    . 如果卫星数据是目录, 则直接检查目录是否匹配指定特征串
    """
    Sat_Object_Status_Zip = 'zip'
    Sat_Object_Status_Dir = 'dir'
    Sat_Object_Status_File = 'file'
    Sat_Object_Status_Unknown = 'unknown'

    __object_status__ = Sat_Object_Status_Unknown

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = None
        information[self.Plugins_Info_Name] = None
        information[self.Plugins_Info_Code] = '000001'
        information[self.Plugins_Info_Catalog] = '卫星数据'
        information[self.Plugins_Info_Type_Title] = '原始数据'
        information[self.Plugins_Info_Type] = 'sat'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.get_runtime_detail_engine()

        return information

    def create_file_content(self):
        if self.__object_status__ == self.Sat_Object_Status_Dir:
            self.__file_content__ = CVirtualContentDir(self.file_info.__file_name_with_full_path__)
        elif self.__object_status__ == self.Sat_Object_Status_Zip:
            self.__file_content__ = CVirtualContentPackage(self.file_info.__file_name_with_full_path__)
        else:
            self.__file_content__ = CVirtualContentDir(self.file_info.__file_path__)

    def special_zip_file_ext_list(self) -> list:
        """
        设定卫星数据压缩包的扩展名
        :return:
        """
        return ['tar.gz', 'rar', 'zip', '7z', 'tar', 'tgz']

    def special_file_ext_list(self) -> list:
        """
        设定卫星数据实体的扩展名
        :return:
        """
        return ['tiff', 'tif']

    def classified(self):
        self.__object_status__ = self.Sat_Object_Status_Unknown
        self.__object_name__ = None
        self.__object_confirm__ = self.Object_Confirm_IUnKnown

        if self.file_info.__file_type__ == self.FileType_File:
            if self.special_zip_file_ext_list().count(self.file_info.__file_ext__.lower()) > 0:
                sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                    self.Sat_Object_Status_Zip)
                if (self.classified_with_character(self.file_info.__file_main_name__, sat_classified_character,
                                                   sat_classified_character_type)):
                    self.__object_status__ = self.Sat_Object_Status_Zip
                    self.__object_confirm__ = self.Object_Confirm_IKnown
                    self.__object_name__ = self.file_info.__file_main_name__
            else:
                sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                    self.Sat_Object_Status_File)
                if (self.classified_with_character(self.file_info.__file_name_without_path__, sat_classified_character,
                                                   sat_classified_character_type)):
                    self.__object_status__ = self.Sat_Object_Status_File
                    self.__object_confirm__ = self.Object_Confirm_IKnown
                    self.__object_name__ = self.get_classified_object_name_of_sat(self.Sat_Object_Status_File)
        elif self.file_info.__file_type__ == self.FileType_Dir:
            sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                self.Sat_Object_Status_Dir)
            if (self.classified_with_character(self.file_info.__file_name_without_path__, sat_classified_character,
                                               sat_classified_character_type)):
                self.__object_status__ = self.Sat_Object_Status_Dir
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = self.file_info.__file_name_without_path__

        return self.__object_confirm__, self.__object_name__

    def classified_with_character(self, text, sat_classified_character, sat_classified_character_type) -> bool:
        """
        根据给定的特征和类型, 对指定的文本进行检查
        :param text:
        :param sat_classified_character:
        :param sat_classified_character_type:
        :return: 是否匹配
        """
        if sat_classified_character_type == self.TextMatchType_Common:
            return CFile.file_match(text.lower(), sat_classified_character)
        elif sat_classified_character_type == self.TextMatchType_Regex:
            return CUtils.text_match_re(text.lower(), sat_classified_character)
        else:
            return False

    @abstractmethod
    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return '', self.TextMatchType_Common

    @abstractmethod
    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        """
        return self.file_info.__file_main_name__

    @abstractmethod
    def get_bus_metadata_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return self.file_info.__file_main_name__

    def get_runtime_detail_engine(self):
        """
        返回运行时的详情引擎
        :return:
        """
        if self.__object_status__ == self.Sat_Object_Status_Zip:
            return None
        elif self.__object_status__ == self.Sat_Object_Status_Dir:
            return self.DetailEngine_All_File_Of_Dir
        elif self.__object_status__ == self.Sat_Object_Status_File:
            return self.DetailEngine_Same_File_Main_Name
        else:
            return None

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        metadata_xml_file_name = self.get_bus_metadata_filename_by_file()
        if not CFile.file_or_path_exist(metadata_xml_file_name):
            return CResult.merge_result(self.Failure, '元数据文件[{0}]不存在, 无法解析! '.format(metadata_xml_file_name))

        try:
            parser.metadata.set_metadata_bus_file(self.MetaDataFormat_XML, metadata_xml_file_name)
            return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(metadata_xml_file_name))
        except:
            parser.metadata.set_metadata_bus(self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]格式不合法, 无法处理! '.format(metadata_xml_file_name))
