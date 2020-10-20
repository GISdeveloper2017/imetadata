# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_wfv.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_time import CTime
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class CSatFilePlugins_gf1_pms(CSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'gf1_pms'
        information[self.Plugins_Info_Name] = 'gf1_pms'

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
            return 'gf1_pms1_*_l1a*', self.TextMatchType_Common
        else:
            return 'gf1_pms1_*_l1a*-pan1.tiff', self.TextMatchType_Common

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
            return self.file_info.__file_main_name__
        elif sat_file_status == self.Sat_Object_Status_Dir:
            return self.file_info.__file_name_without_path__
        else:
            return self.file_info.__file_main_name__.replace('-PAN1', '')

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            '{0}-PAN1.xml'.format(self.classified_object_name())
        )

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
        return [
            {
                self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '全色文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()),
                self.Name_ID: 'mss_tif',
                self.Name_Title: '多光谱文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser):
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/SceneID',
                self.Name_ID: 'SceneID',
                self.Name_Title: '景编号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/OrbitID',
                self.Name_ID: 'OrbitID',
                self.Name_Title: '轨道编号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def parser_metadata_time_after_qa(self, parser) -> str:
        """
        继承本方法, 对详细的时间元数据信息进行处理
        todo(全体) 继承本方法, 对详细的时间元数据信息进行处理, 一般包括具体的time, start_time, end_time进行设置, 示例:
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Start_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_End_Time, CTime.now())
        :param parser:
        :return:
        """
        parser.metadata.set_metadata_time(
            self.Success,
            '时间信息[{0}]成功解析! '.format(self.file_info.__file_name_with_full_path__),
            self.Name_Time,
            CXml.get_element_text(parser.metadata.metadata_bus_xml().xpath_one('/ProductMetaData/CenterTime'))
        )
        parser.metadata.set_metadata_time(
            self.Success,
            '时间信息[{0}]成功解析! '.format(self.file_info.__file_name_with_full_path__),
            self.Name_Start_Time,
            CXml.get_element_text(parser.metadata.metadata_bus_xml().xpath_one('/ProductMetaData/StartTime'))
        )
        parser.metadata.set_metadata_time(
            self.Success,
            '时间信息[{0}]成功解析! '.format(self.file_info.__file_name_with_full_path__),
            self.Name_End_Time,
            CXml.get_element_text(parser.metadata.metadata_bus_xml().xpath_one('/ProductMetaData/EndTime'))
        )
        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的时间信息解析成功! '.format(self.file_info.__file_name_with_full_path__)
        )

    def parser_metadata_spatial_after_qa(self, parser):
        """
        继承本方法, 对详细的空间元数据信息进行处理
        todo(全体) 继承本方法, 对详细的空间元数据信息进行处理, 一般包括原生的中心点, 外包框, 外边框, 以及Wgs84的中心点, 外包框, 外边框, 示例:
            parser.metadata.set_metadata_spatial(self.Success, '', self.Spatial_MetaData_Type_Native_Center, 'Point(0 0)')
        :param parser:
        :return:
        """
        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的空间信息解析成功! '.format(self.file_info.__file_name_with_full_path__)
        )

    def parser_metadata_view_after_qa(self, parser):
        """
        继承本方法, 对详细的可视元数据信息进行处理
        :param parser:
        :return:
        """
        data_date_time = CXml.get_element_text(
            parser.metadata.metadata_bus_xml().xpath_one('/ProductMetaData/CenterTime'))

        if CUtils.equal_ignore_case(data_date_time, ''):
            data_date = CTime.today()
        else:
            data_date = CTime.from_datetime_str(data_date_time)

        data_year = CTime.format_str(data_date, '%Y')
        data_month = CTime.format_str(data_date, '%m')

        data_view_sub_path = CFile.join_file(data_year, data_month)
        data_view_sub_path = CFile.join_file(data_view_sub_path, self.classified_object_name())
        data_view_sub_path = CFile.join_file(data_view_sub_path, self.file_info.__my_id__)
        data_view_path = CFile.join_file(
            self.file_content.view_root_dir,
            data_view_sub_path
        )

        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-PAN1.jpg'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-PAN1_thumb.jpg'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-MSS1.jpg'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-MSS1_thumb.jpg'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-PAN1.xml'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-PAN1.rpb'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-MSS1.xml'.format(self.classified_object_name())
            ), data_view_path)
        CFile.copy_file_to(
            CFile.join_file(
                self.file_content.content_root_dir,
                '{0}-MSS1.rpb'.format(self.classified_object_name())
            ), data_view_path)

        browse_file = CFile.join_file(data_view_sub_path, '{0}-PAN1.jpg'.format(self.classified_object_name()))
        parser.metadata.set_metadata_view(
            self.DB_True,
            '文件[{0}]的预览图成功加载! '.format(self.file_info.__file_name_with_full_path__),
            self.View_MetaData_Type_Browse,
            browse_file
        )

        thumb_file = CFile.join_file(data_view_sub_path, '{0}-PAN1.jpg'.format(self.classified_object_name()))
        parser.metadata.set_metadata_view(
            self.DB_True,
            '文件[{0}]的拇指图成功加载! '.format(self.file_info.__file_name_with_full_path__),
            self.View_MetaData_Type_Thumb,
            thumb_file
        )

        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的可视化信息解析成功! '.format(self.file_info.__file_name_with_full_path__)
        )
