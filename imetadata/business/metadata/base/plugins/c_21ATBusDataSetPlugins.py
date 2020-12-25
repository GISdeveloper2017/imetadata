# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_3002_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class C21ATBusDataSetPlugins(CDirPlugins):
    __classified_object_type = None
    __metadata_xml_obj__ = None
    __bus_metadata_xml_file_name__ = None

    def get_information(self) -> dict:
        information = super().get_information()
        if self.__metadata_xml_obj__ is not None:
            information[self.Plugins_Info_Title] = CXml.get_element_text(
                self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName))
        information[self.Plugins_Info_Type_Code] = None  # '110001'
        information[self.Plugins_Info_Group] = self.DataGroup_Industry_Land_DataSet
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Land  # 'land'
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(
            information[self.Plugins_Info_Catalog])  # '国土行业'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Busdataset
        information[self.Plugins_Info_HasChildObj] = self.DB_True

        return information

    def classified(self):
        self._object_confirm = self.Object_Confirm_IUnKnown
        self._object_name = None

        current_path = self.file_info.file_name_with_full_path
        metadata_file_name = CFile.join_file(current_path, self.FileName_MetaData_Bus_21AT)
        if CFile.file_or_path_exist(metadata_file_name):
            self.__bus_metadata_xml_file_name__ = metadata_file_name
            self.__metadata_xml_obj__ = CXml()
            try:
                self.__metadata_xml_obj__.load_file(metadata_file_name)
                self.__classified_object_type = CXml.get_element_text(
                    self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductType))

                if CUtils.equal_ignore_case(
                        self.__classified_object_type,
                        CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Type, None)
                ):
                    self._object_confirm = self.Object_Confirm_IKnown
                    self._object_name = CXml.get_element_text(
                        self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName)
                    )
            except:
                self.__metadata_xml_obj__ = None
                CLogger().warning('发现文件{0}符合二十一世纪业务数据集标准, 但该文件格式有误, 无法打开! ')

        return self._object_confirm, self._object_name

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        if not CFile.file_or_path_exist(self.__bus_metadata_xml_file_name__):
            return CResult.merge_result(self.Failure,
                                        '元数据文件[{0}]不存在, 无法解析! '.format(self.__bus_metadata_xml_file_name__))

        try:
            parser.metadata.set_metadata_bus_file(
                self.Success,
                '元数据文件[{0}]成功加载! '.format(self.__bus_metadata_xml_file_name__),
                self.MetaDataFormat_XML,
                self.__bus_metadata_xml_file_name__)
            return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(self.__bus_metadata_xml_file_name__))
        except:
            parser.metadata.set_metadata_bus(
                self.Failure,
                '元数据文件[{0}]格式不合法, 无法处理! '.format(self.__bus_metadata_xml_file_name__),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]格式不合法, 无法处理! '.format(self.__bus_metadata_xml_file_name__))

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 李宪
        :param parser:
        :return:
        """
        pass
