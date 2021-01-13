# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:24 
# @Author : 王西亚 
# @File : c_satPlugins.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class COpticalSatPlugins(CSatPlugins):
    """
    光学卫星数据插件
    . 如果卫星数据是文件, 则先检查文件名是否在指定的列表中, 之后再检查文件主名是否匹配指定特征串
    . 如果卫星数据是目录, 则直接检查目录是否匹配指定特征串
    """

    def get_information(self) -> dict:
        return super().get_information()

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置光学卫星识别的特征
        """
        return super().get_classified_character_of_sat(sat_file_status)

    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        if sat_file_status == self.Sat_Object_Status_Zip:
            return self.file_info.file_main_name
        elif sat_file_status == self.Sat_Object_Status_Dir:
            return self.file_info.file_name_without_path
        elif sat_file_status == self.Sat_Object_Status_File:
            return CFile.file_name(self.file_info.file_path)
        else:
            return self.file_info.file_main_name

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i){0}.xml'.format(self.classified_object_name()), '{0}.xml'.format(self.classified_object_name())
            )
        )
