# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 09:08 
# @Author : 王西亚 
# @File : c_metaDataParser.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorMng import CMDExtractorMng
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

        # 处理元数据
        metadata_extract_result, metadata_extract_memo, metadata_type, metadata_text = self.metadata.metadata()
        metadata_json = None
        metadata_xml = None
        if metadata_type == self.MetaDataFormat_XML:
            metadata_xml = metadata_text
        elif metadata_type == self.MetaDataFormat_Json:
            metadata_json = metadata_text

        # 处理业务元数据
        metadata_bus_extract_result, metadata_bus_extract_memo, metadata_bus_type, metadata_bus_text = self.metadata.metadata_bus()
        metadata_bus_json = None
        metadata_bus_xml = None
        if metadata_bus_type == self.MetaDataFormat_XML:
            metadata_bus_xml = metadata_bus_text
        elif metadata_bus_type == self.MetaDataFormat_Json:
            metadata_bus_json = metadata_bus_text

        # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute(
            '''
            update dm2_storage_object
            set dso_quality = :dso_quality
                , dso_quality_result = :dso_quality_result
                , dso_metadata_result = :dso_metadata_result
                , dsometadataparsememo = :dsometadataparsememo
                , dsometadatatype = :dsometadatatype
                , dsometadatatext = :dsometadatatext
                , dsometadatajson = :dsometadatajson
                , dsometadataxml = :dsometadataxml
                , dso_metadata_bus_result = :dso_metadata_bus_result
                , dsometadata_bus_parsememo = :dsometadata_bus_parsememo
                , dsometadatatype_bus = :dsometadatatype_bus
                , dsometadatatext_bus = :dsometadatatext_bus
                , dsometadatajson_bus = :dsometadatajson_bus
                , dsometadataxml_bus = :dsometadataxml_bus
            where dsoid = :dsoid
            ''',
            {
                'dso_quality': file_quality_text,
                'dsoid': self.object_id,
                'dso_quality_result': quality_result,
                'dso_metadata_result': metadata_extract_result,
                'dsometadataparsememo': metadata_extract_memo,
                'dsometadatatype': metadata_type,
                'dsometadatatext': metadata_text,
                'dsometadatajson': metadata_json,
                'dsometadataxml': metadata_xml,
                'dso_metadata_bus_result': metadata_extract_result,
                'dsometadata_bus_parsememo': metadata_bus_extract_memo,
                'dsometadatatype_bus': metadata_bus_type,
                'dsometadatatext_bus': metadata_bus_text,
                'dsometadatajson_bus': metadata_bus_json,
                'dsometadataxml_bus': metadata_bus_xml
            }
        )
        return CResult.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        pass

    def batch_qa_file(self, list_qa: list):
        """
        批量处理数据完整性方面的质检项目
        :param list_qa:
        :return:
        """
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            self.metadata.quality.append_total_quality(
                CAudit.a_file(
                    CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                    CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                    CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                    CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                    CFile.join_file(
                        self.file_content.content_root_dir,
                        CUtils.dict_value_by_name(qa_item, self.Name_FileName, '')
                    ),
                    qa_item
                )
            )

    def batch_qa_metadata_xml(self, list_qa: list):
        """
        批量处理xml格式的元数据中的质检项目
        :param list_qa:
        :return:
        """
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
        """
        批量处理xml格式的业务元数据中的质检项目
        :param list_qa:
        :return:
        """
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            list_result = CAudit.a_xml_element(
                CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                self.metadata.metadata_bus_xml(),
                CUtils.dict_value_by_name(qa_item, self.Name_XPath, ''),
                qa_item
            )
            for item_result in list_result:
                self.metadata.quality.append_metadata_bus_quality(item_result)

    def batch_qa_metadata_json_item(self, list_qa: list):
        """
        批量处理json格式的元数据中的质检项目
        :param list_qa:
        :return:
        """
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            list_result = CAudit.a_json_element(
                CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                self.metadata.metadata_json(),
                CUtils.dict_value_by_name(qa_item, self.Name_XPath, ''),
                qa_item
            )
            for item_result in list_result:
                self.metadata.quality.append_metadata_data_quality(item_result)

    def batch_qa_metadata_bus_json_item(self, list_qa: list):
        """
        批量处理json格式的业务元数据中的质检项目
        :param list_qa:
        :return:
        """
        if len(list_qa) == 0:
            return

        for qa_item in list_qa:
            list_result = CAudit.a_json_element(
                CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Level, self.QA_Level_Min),
                CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                self.metadata.metadata_bus_json(),
                CUtils.dict_value_by_name(qa_item, self.Name_XPath, ''),
                qa_item
            )
            for item_result in list_result:
                self.metadata.quality.append_metadata_bus_quality(item_result)

    def process_default_metadata(self, metadata_engine_type):
        """
        内置的元数据提取
        :param metadata_engine_type:
        :return:
        """
        md_extractor = CMDExtractorMng.give_me_extractor(metadata_engine_type, self.object_id, self.object_name,
                                                         self.file_info, self.file_content)
        if not isinstance(md_extractor, CParserCustom):
            return md_extractor.process()

    def save_metadata_time(self) -> str:
        """
        完成时间元数据的入库更新操作
        :return:
        """
        mdt_ext_result, mdt_ext_memo, mdt_ext_content = self.metadata.metadata_time()
        if mdt_ext_result == self.DB_False:
            mdt_ext_content = None

        # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute(
            '''
            update dm2_storage_object
            set dso_time_result = :dso_time_result
                , dso_time_parsermemo = :dso_time_parsermemo
                , dso_time = :dso_time
            where dsoid = :dsoid
            ''',
            {
                'dsoid': self.object_id,
                'dso_time_result': mdt_ext_result,
                'dso_time_parsermemo': mdt_ext_memo,
                'dso_time': mdt_ext_content
            }
        )
        return CResult.merge_result(self.Success, '时间元数据处理完毕!')

    def save_metadata_view(self) -> str:
        """
        完成可视元数据的入库更新操作
        :return:
        """
        mdt_view_result, mdt_view_memo, mdt_view_thumb_file, mdt_view_browse_file = self.metadata.metadata_view()
        if mdt_view_result == self.DB_False:
            mdt_view_thumb_file = None
            mdt_view_browse_file = None

        # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute(
            '''
            update dm2_storage_object
            set dso_view_result = :dso_view_result
                , dso_view_parsermemo = :dso_view_parsermemo
                , dso_browser = :dso_browser
                , dso_thumb = :dso_thumb
            where dsoid = :dsoid
            ''',
            {
                'dsoid': self.object_id,
                'dso_view_result': mdt_view_result,
                'dso_view_parsermemo': mdt_view_memo,
                'dso_browser': mdt_view_browse_file,
                'dso_thumb': mdt_view_thumb_file
            }
        )
        return CResult.merge_result(self.Success, '可视化元数据处理完毕!')

    def save_metadata_spatial(self) -> str:
        """
        完成空间元数据的入库更新操作
        :return:
        """
        mdt_spatial_result, mdt_spatial_memo, mdt_spatial = self.metadata.metadata_spatial()

        # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute(
            '''
            update dm2_storage_object
            set dso_spatial_result = :dso_spatial_result
                , dso_spatial_parsermemo = :dso_spatial_parsermemo
                , dso_center_native = :dso_center_native
                , dso_geo_bb_native = :dso_geo_bb_native
                , dso_geo_native = :dso_geo_native
                , dso_center_wgs84 = :dso_center_wgs84
                , dso_geo_bb_wgs84 = :dso_geo_bb_wgs84
                , dso_geo_wgs84 = :dso_geo_wgs84
            where dsoid = :dsoid
            ''',
            {
                'dsoid': self.object_id,
                'dso_spatial_result': mdt_spatial_result,
                'dso_spatial_parsermemo': mdt_spatial_memo,
                'dso_center_native': mdt_spatial.native_center,
                'dso_geo_bb_native': mdt_spatial.native_box,
                'dso_geo_native': mdt_spatial.native_geom,
                'dso_center_wgs84': mdt_spatial.wgs84_center,
                'dso_geo_bb_wgs84': mdt_spatial.wgs84_bbox,
                'dso_geo_wgs84': mdt_spatial.wgs84_geom
            }
        )
        return CResult.merge_result(self.Success, '空间元数据处理完毕!')
