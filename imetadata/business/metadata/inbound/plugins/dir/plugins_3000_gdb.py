# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_2000_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class plugins_3000_gdb(CDirPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '矢量数据集'
        information[self.Plugins_Info_Name] = 'gdb'
        information[self.Plugins_Info_Code] = None
        information[self.Plugins_Info_Catalog] = '矢量'
        information[self.Plugins_Info_Type] = 'vector'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Vector
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        information[self.Plugins_Info_Group_Name] = self.DataGroup_Vector_DataSet
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])
        return information

    def classified(self):
        self._object_confirm = self.Object_Confirm_IUnKnown
        self._object_name = None

        current_path = self.file_info.file_name_with_full_path
        if (self.file_info.file_name_without_path.lower().endswith('.gdb')) \
                and CFile.find_file_or_subpath_of_path(current_path, '*.gdbtable'):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_main_name
        return self._object_confirm, self._object_name
