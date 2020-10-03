# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_filePlugins_guotu.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class CFilePlugins_GUOTU(CFilePlugins):
    """
    国土行业文件入库插件
    todo 在这里补充国土行业数据的其他类型
    """

    MetaData_Rule_Type_DOM = 'dom'
    MetaData_Rule_Type_DEM = 'dem'
    MetaData_Rule_Type_SD = 'sd'

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = None
        information[self.Plugins_Info_Name] = None
        information[self.Plugins_Info_Code] = '000001'
        information[self.Plugins_Info_Catalog] = '行业数据'
        information[self.Plugins_Info_Type_Title] = '国土行业数据'
        information[self.Plugins_Info_Type] = '国土'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        information[self.Plugins_Info_QCEngine] = None

        return information

    def classified(self):
        """
        1. 验证当前数据的规则, 比如是DOM方可进行当前插件的识别, 否则当前插件无效
        2. 如果当前数据的规则有效, 则进行深度的识别, 比如dom-10, dom-12类型的

        由于父类CFilePlugins中主要对文件名称进行特征识别, 所以这里需要全部重写业务数据集的识别, 就不再调用super().classified()了!!!

        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        self.__object_name__ = None
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        if not self.get_classified_rule_valid():
            return self.__object_confirm__, self.__object_name__
        else:
            return self.classified_by_character_guotu()

    def get_classified_rule_valid(self) -> bool:
        """
        验证当前验证规则是否有效
        :return:
        """
        metadata_rule_type = self.get_metadata_rule_type()
        if CUtils.equal_ignore_case(metadata_rule_type, self.MetaData_Rule_Type_None):
            file_path = self.file_info.__file_path_with_rel_path__
            return CFile.subpath_in_path(self.get_classified_metadata_rule_type(), file_path)
        else:
            return CUtils.equal_ignore_case(self.get_metadata_rule_type(), self.get_classified_metadata_rule_type())

    @abstractmethod
    def get_classified_metadata_rule_type(self):
        """
        设置需要提前验证的元数据规则类型
        :return:
        """
        return self.MetaData_Rule_Type_None

    @abstractmethod
    def classified_by_character_guotu(self):
        """
        默认的识别模式
        根据文件名的特征, 进行对象类型识别

        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        return self.__object_confirm__, self.__object_name__
