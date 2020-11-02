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
    todo(提示) 在质检中或者在识别过程中, 可以直接确定业务元数据的类型和源文件名, 这样系统将按照内置的几种类型的标准处理方法进行自动处理,
        否则需要自行处理业务元数据
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
        information[self.Plugins_Info_SpatialEngine] = self.MetaDataEngine_Raster  # 国土的统一都是影像数据
        information[self.Plugins_Info_Group_Name] = self.DataGroup_Industry_Data
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])

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
        self._object_name = None
        self._object_confirm = self.Object_Confirm_IUnKnown
        return self._object_confirm, self._object_name
