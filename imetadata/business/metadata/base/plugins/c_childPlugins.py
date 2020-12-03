# -*- coding: utf-8 -*- 
# @Time : 2020/11/26 15:03 
# @Author : 王西亚 
# @File : c_childPlugins.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CChildPlugins(CPlugins):
    """
    子对象插件基类
    . 子对象是对象的一部分, 以gdb为例, 其中的每一个层, 是gdb对象的子对象
    . 子对象不需要识别, 是在父对象解析完毕后, 直接创建的, 无需识别
    """

    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)
        if self.file_info is not None:
            self._file_content = CVirtualContentDir(self.file_info.file_name_with_full_path)

    def classified(self):
        return self.Object_Confirm_IKnown, ''

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Group] = self.DataGroup_Vector
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Module_Distribute_Engine] = None
        return information
