# -*- coding: utf-8 -*- 
# @Time : 2020/11/2 09:50
# @Author : 邢凯凯
# @File : c_satFilePlugins_gf3_hh.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf3 import CSatFilePlugins_gf3


class CSatFilePlugins_gf3_vhvv(CSatFilePlugins_gf3):

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
            return r'(?i)GF3.*_VHVV_.*', self.TextMatchType_Regex
        else:
            # GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VV_L10002039504_Strip_0.tiff
            # 暂定 gf3_mdj_wsc_*_l1a_vv_l1*_strip_0.tiff为主对象文件
            # 散列文件的识别方式后续有待开发，目前暂不测试
            return r'(?i)GF3.*(_AHV_|_HH_|_HHHV_).*_strip_0.tiff', self.TextMatchType_Regex

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 文件的质检列表
        质检项目应包括并不限于如下内容:
        1. 实体数据的附属文件是否完整, 实体数据是否可以正常打开和读取
        1. 元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        1. 业务元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        示例:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]
        :param parser:
        :return:
        """
        if self.__object_status__ == self.Sat_Object_Status_Dir:
            match_list = CFile.file_or_dir_fullname_of_path(self.file_info.file_name_with_full_path, False,
                                                            'GF3_.*_VV_.*.tiff', CFile.MatchType_Regex)
            if len(match_list) > 1:
                for match_file_name in match_list:
                    if '_Strip_0' in match_file_name:
                        return [
                            {
                                self.Name_FileName: CFile.file_name(match_file_name),
                                self.Name_ID: '影像tiff',
                                self.Name_Title: '影像文件',
                                self.Name_Group: self.QA_Group_Data_Integrity,
                                self.Name_Result: self.QA_Result_Error,
                                self.Name_Format: self.DataFormat_Raster_File
                            }
                        ]
                    break
            elif len(match_list) == 1:
                return [
                    {
                        self.Name_FileName: CFile.file_name(match_list[0]),
                        self.Name_ID: '影像tiff',
                        self.Name_Title: '影像文件',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Format: self.DataFormat_Raster_File
                    }
                ]

        if self.__object_status__ == self.Sat_Object_Status_Zip:
            match_list = CFile.file_or_dir_fullname_of_path(self.file_content.content_root_dir, False,
                                                            'GF3_.*_VV_.*.tiff', CFile.MatchType_Regex)
            if len(match_list) > 1:
                for match_file_name in match_list:
                    if '_Strip_0' in match_file_name:
                        return [
                            {
                                self.Name_FileName: CFile.file_name(match_file_name),
                                self.Name_ID: '影像tiff',
                                self.Name_Title: '影像文件',
                                self.Name_Group: self.QA_Group_Data_Integrity,
                                self.Name_Result: self.QA_Result_Error,
                                self.Name_Format: self.DataFormat_Raster_File
                            }
                        ]
                    break
            elif len(match_list) == 1:
                return [
                    {
                        self.Name_FileName: CFile.file_name(match_list[0]),
                        self.Name_ID: '影像tiff',
                        self.Name_Title: '影像文件',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Format: self.DataFormat_Raster_File
                    }
                ]
        else:
            return super().init_qa_file_list(parser)

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)GF3.*VH(?!.*(thumb|thumnail)).*.jpg', '{0}_thumb.jpg'.format(self.classified_object_name())
                )
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)GF3.*VH.*(thumb|thumnail).jpg', '{0}_thumb.jpg'.format(self.classified_object_name())
                )
            }
        ]
