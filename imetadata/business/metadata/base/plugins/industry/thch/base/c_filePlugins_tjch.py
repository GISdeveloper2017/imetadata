# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_filePlugins_guotu.py
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CFilePlugins_tjch(CPlugins):
    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        information[self.Plugins_Info_Title] = information[self.Plugins_Info_ID]
        information[self.Plugins_Info_ViewEngine] = None
        information[self.Plugins_Info_SpatialEngine] = None
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_Group] = None
        information[self.Plugins_Info_Group_Title] = None
        information[self.Plugins_Info_TagsEngine] = None
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Module_Distribute_Engine] = None  # 同步的引擎，值是发布同步用的类的名字
        return information

    def classified(self):
        pass
