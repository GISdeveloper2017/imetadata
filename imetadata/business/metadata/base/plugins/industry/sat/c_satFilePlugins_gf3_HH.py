# -*- coding: utf-8 -*- 
# @Time : 2020/11/2 09:50
# @Author : 邢凯凯
# @File : c_satFilePlugins_gf3_HH.py
import re

from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf3 import CSatFilePlugins_gf3


class CSatFilePlugins_gf3_HH(CSatFilePlugins_gf3):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF3_WSC'
        information[self.Plugins_Info_Type_Title] = '高分三号WSC传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
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
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)GF3.*(_AHV_|_HH_|_HHHV_).*', self.TextMatchType_Regex
        else:
            # GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VV_L10002039504_Strip_0.tiff
            # 暂定 gf3_mdj_wsc_*_l1a_vv_l1*_strip_0.tiff为主对象文件
            # 散列文件的识别方式后续有待开发，目前暂不测试
            return r'(?i)GF3.*(_AHV_|_HH_|_HHHV_).*_strip_0.tiff', self.TextMatchType_Regex

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
        if sat_file_status == self.Sat_Object_Status_Zip:
            return self.file_info.file_main_name
        elif sat_file_status == self.Sat_Object_Status_Dir:
            return self.file_info.file_name_without_path
        else:
            # 散列文件的识别方式有待调整
            return self.file_info.file_main_name.replace('VV', 'VHVV').replace('_Strip_0', '')

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                # 补个属性，再调整
                self.Name_FileName: '{0}.tiff'.format(self.classified_object_name()),
                self.Name_ID: '影像tiff',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        if self.__object_status__ == self.Sat_Object_Status_Dir:
            thumb_match_list = CFile.file_or_dir_fullname_of_path(self.file_info.file_name_with_full_path, False,
                                                                  r'(?i)GF3.*HH.*(thumb|thumnail).jpg',
                                                                  CFile.MatchType_Regex)
            # .*HH(?!.*(thumb | thumnail)).*.jpg
            browser_match_list = CFile.file_or_dir_fullname_of_path(self.file_info.file_name_with_full_path, False,
                                                                    r'(?i)GF3.*HH(?!.*(thumb | thumnail)).*.jpg',
                                                                    CFile.MatchType_Regex)
            if len(thumb_match_list) > 0 and len(browser_match_list) > 0:
                thumb_file_name = CFile.file_name(thumb_match_list[0])
                browser_file_name = CFile.file_name(browser_match_list[0])
                return [
                    {
                        self.Name_ID: self.View_MetaData_Type_Browse,
                        self.Name_FileName: '{0}'.format(browser_file_name)

                    },
                    {
                        self.Name_ID: self.View_MetaData_Type_Thumb,
                        self.Name_FileName: '{0}'.format(thumb_file_name)
                    }
                ]
        elif self.__object_status__ == self.Sat_Object_Status_Zip:
            thumb_match_list = CFile.file_or_dir_fullname_of_path(self.file_content.content_root_dir, False,
                                                                  r'(?i)GF3.*HH.*(thumb|thumnail).jpg',
                                                                  CFile.MatchType_Regex)
            # .*HH(?!.*(thumb | thumnail)).*.jpg
            browser_match_list = CFile.file_or_dir_fullname_of_path(self.file_content.content_root_dir, False,
                                                                    r'(?i)GF3.*HH(?!.*(thumb | thumnail)).*.jpg',
                                                                    CFile.MatchType_Regex)
            if len(thumb_match_list) > 0 and len(browser_match_list) > 0:
                thumb_file_name = CFile.file_name(thumb_match_list[0])
                browser_file_name = CFile.file_name(browser_match_list[0])
                return [
                    {
                        self.Name_ID: self.View_MetaData_Type_Browse,
                        self.Name_FileName: '{0}'.format(browser_file_name)

                    },
                    {
                        self.Name_ID: self.View_MetaData_Type_Thumb,
                        self.Name_FileName: '{0}'.format(thumb_file_name)
                    }
                ]
