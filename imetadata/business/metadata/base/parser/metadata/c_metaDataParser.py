# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 09:08 
# @Author : 王西亚 
# @File : c_metaDataParser.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData
from imetadata.business.metadata.base.parser.metadata.quality.c_audit import CAudit
from imetadata.database.c_factory import CFactory


class CMetaDataParser(CParser):
    """
    对象元数据处理类
    在本对象中, 要处理如下内容:
    . 对象的质检
    . 对象的业务元数据
    . 对象的基础元数据
    . 对象的可视元数据
    . 对象的元数据优化
    """
    __information__: dict
    __file_content__: CVirtualContent = None
    __metadata__: CMetaData = None

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                 file_content: CVirtualContent, information: dict):
        self.__metadata__ = CMetaData()
        self.__information__ = information
        self.__file_content__ = file_content
        super().__init__(object_id, object_name, file_info)

    @property
    def metadata(self):
        return self.__metadata__

    @property
    def file_content(self):
        return self.__file_content__

    def process(self) -> str:
        """
        完成元数据的所有处理操作
        1. 数据解析处理
        1. 文件命名检查
        1. 文件完整性检查
        1. 文件元数据提取并分析
        1. 业务元数据提取并分析
        :return:
        """
        file_quality_text = self.metadata.quality.to_xml()
        quality_result = self.metadata.quality.quality_result()

        metadata_type, metadata_text = self.metadata.metadata()
        metadata_json = None
        metadata_xml = None
        if metadata_type == self.MetaDataFormat_XML:
            metadata_xml = metadata_text
        elif metadata_type == self.MetaDataFormat_Json:
            metadata_json = metadata_text

        metadata_bus_type, metadata_bus_text = self.metadata.metadata_bus()
        metadata_bus_json = None
        metadata_bus_xml = None
        if metadata_bus_type == self.MetaDataFormat_XML:
            metadata_bus_xml = metadata_bus_text
        elif metadata_bus_type == self.MetaDataFormat_Json:
            metadata_bus_json = metadata_bus_text

        CFactory().give_me_db(self.file_info.__db_server_id__).execute('''
            update dm2_storage_object
            set dso_quality = :dso_quality
                , dso_quality_result = :dso_quality_result
                , dsometadatatype = :dsometadatatype
                , dsometadatatext = :dsometadatatext
                , dsometadatajson = :dsometadatajson
                , dsometadataxml = :dsometadataxml
                , dsometadatatype_bus = :dsometadatatype_bus
                , dsometadatatext_bus = :dsometadatatext_bus
                , dsometadatajson_bus = :dsometadatajson_bus
                , dsometadataxml_bus = :dsometadataxml_bus
            where dsoid = :dsoid
            ''', {'dso_quality': file_quality_text,
                  'dsoid': self.object_id,
                  'dso_quality_result': quality_result,
                  'dsometadatatype': metadata_type,
                  'dsometadatatext': metadata_text,
                  'dsometadatajson': metadata_json,
                  'dsometadataxml': metadata_xml,
                  'dsometadatatype_bus': metadata_bus_type,
                  'dsometadatatext_bus': metadata_bus_text,
                  'dsometadatajson_bus': metadata_bus_json,
                  'dsometadataxml_bus': metadata_bus_xml
                  }
                                                                       )
        return CUtils.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        pass

    def batch_qa_file_exist(self, list_qa: list):
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            self.metadata.quality.append_total_quality(
                CAudit.a_file_exist(CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                                    CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                                    CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                                    CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                                    CFile.join_file(
                                        self.file_content.content_root_dir,
                                        CUtils.dict_value_by_name(qa_item, self.Name_FileName, '')
                                    )
                                    )
            )

    def batch_qa_metadata_xml(self, list_qa: list):
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            list_result = CAudit.a_xml_attribute(
                CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                self.metadata.metadata_xml(),
                CUtils.dict_value_by_name(qa_item, self.Name_XPath, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Attr_Name, ''),
                qa_item
            )
            for item_result in list_result:
                self.metadata.quality.append_metadata_data_quality(item_result)

    def batch_qa_metadata_bus_xml_item(self, list_qa: list):
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            if CUtils.equal_ignore_case(qa_item[self.Name_Type], self.QA_Type_XML_Node_Exist):
                list_result = CAudit.a_xml_element(
                    CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                    CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                    CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                    CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                    self.metadata.metadata_bus_xml(),
                    CUtils.dict_value_by_name(qa_item, self.Name_XPath, '')
                )
                for item_result in list_result:
                    self.metadata.quality.append_metadata_bus_quality(item_result)

    def batch_qa_metadata_json_item(self, list_qa: list):
        if len(list_qa) == 0:
            return

    def batch_qa_metadata_bus_json_item(self, list_qa: list):
        if len(list_qa) == 0:
            return
