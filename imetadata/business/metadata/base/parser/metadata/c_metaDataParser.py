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
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorMng import CMDExtractorMng
from imetadata.business.metadata.base.parser.metadata.quality.c_audit import CAudit
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractorMng import CSpatialExtractorMng
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreatorMng import CViewCreatorMng
from imetadata.database.base.c_dataset import CDataSet
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
            list_result = CAudit.a_file(
                CUtils.dict_value_by_name(qa_item, self.Name_ID, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Title, ''),
                CUtils.dict_value_by_name(qa_item, self.Name_Group, self.QA_Group_Data_Integrity),
                CUtils.dict_value_by_name(qa_item, self.Name_Result, self.QA_Result_Pass),
                CFile.join_file(
                    self.file_content.content_root_dir,
                    CUtils.dict_value_by_name(qa_item, self.Name_FileName, '')
                ),
                qa_item
            )
            for item_result in list_result:
                self.metadata.quality.append_total_quality(item_result)

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
                CUtils.dict_value_by_name(qa_item, self.Name_Group, self.QA_Group_Data_Integrity),
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
                CUtils.dict_value_by_name(qa_item, self.Name_Group, self.QA_Group_Data_Integrity),
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
                CUtils.dict_value_by_name(qa_item, self.Name_Group, self.QA_Group_Data_Integrity),
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
                CUtils.dict_value_by_name(qa_item, self.Name_Group, self.QA_Group_Data_Integrity),
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
        return md_extractor.process()

    def process_default_view(self, engine_type):
        """
        内置的可视化元数据提取
        :param engine_type:
        :return:
        """
        md_view_creator = CViewCreatorMng.give_me_creator(engine_type, self.object_id, self.object_name,
                                                          self.file_info, self.file_content)
        return md_view_creator.process()

    def process_default_spatial(self, engine_type):
        """
        内置的可视化元数据提取
        :param parser:
        :param engine_type:
        :return:
        """
        md_spatial_extractor = CSpatialExtractorMng.give_me_extractor(engine_type, self.object_id, self.object_name,
                                                                      self.file_info, self.file_content, self.metadata)
        return md_spatial_extractor.process()

    def save_metadata_data_and_bus(self) -> str:
        file_quality_text = self.metadata.quality.to_xml()
        file_quality_summary_text = self.metadata.quality.summary()

        metadata_extract_result, metadata_extract_memo, metadata_type, metadata_text = self.metadata.metadata()

        # 处理业务元数据
        metadata_bus_extract_result, metadata_bus_extract_memo, metadata_bus_type, metadata_bus_text = self.metadata.metadata_bus()

        commands = [(
            '''
            update dm2_storage_object
            set dso_quality = :dso_quality
                , dso_quality_summary = :dso_quality_summary
            where dsoid = :dsoid
            ''', {
                'dso_quality': file_quality_text,
                'dso_quality_summary': file_quality_summary_text,
                'dsoid': self.object_id,
            }
        ), (
            '''
            update dm2_storage_object
            set dso_metadata_result = :dso_metadata_result
                , dsometadataparsememo = :dsometadataparsememo
                , dsometadatatype = :dsometadatatype
                , dsometadatatext = :dsometadatatext
                , dsometadatajson = null
                , dsometadataxml = null
            where dsoid = :dsoid
            ''', {
                'dsoid': self.object_id,
                'dso_metadata_result': metadata_extract_result,
                'dsometadataparsememo': metadata_extract_memo,
                'dsometadatatype': metadata_type,
                'dsometadatatext': metadata_text
            }
        ), (
            '''
            update dm2_storage_object
            set dso_metadata_bus_result = :dso_metadata_bus_result
                , dsometadata_bus_parsememo = :dsometadata_bus_parsememo
                , dsometadatatype_bus = :dsometadatatype_bus
                , dsometadatatext_bus = :dsometadatatext_bus
                , dsometadatajson_bus = null
                , dsometadataxml_bus = null
            where dsoid = :dsoid
            ''', {
                'dsoid': self.object_id,
                'dso_metadata_bus_result': metadata_extract_result,
                'dsometadata_bus_parsememo': metadata_bus_extract_memo,
                'dsometadatatype_bus': metadata_bus_type,
                'dsometadatatext_bus': metadata_bus_text
            }
        )]

        if metadata_type == self.MetaDataFormat_XML:
            commands.append(
                (
                    '''
                    update dm2_storage_object
                    set dsometadataxml = dsometadatatext::xml
                    where dsoid = :dsoid
                    ''', {'dsoid': self.object_id}
                )
            )
        elif metadata_type == self.MetaDataFormat_Json:
            commands.append(
                (
                    '''
                    update dm2_storage_object
                    set dsometadatajson = dsometadatatext::json
                    where dsoid = :dsoid
                    ''', {'dsoid': self.object_id}
                )
            )

        if metadata_bus_type == self.MetaDataFormat_XML:
            commands.append(
                (
                    '''
                    update dm2_storage_object
                    set dsometadataxml_bus = dsometadatatext_bus::xml
                    where dsoid = :dsoid
                    ''', {'dsoid': self.object_id}
                )
            )
        elif metadata_bus_type == self.MetaDataFormat_Json:
            commands.append(
                (
                    '''
                    update dm2_storage_object
                    set dsometadatajson_bus = dsometadatatext_bus::json
                    where dsoid = :dsoid
                    ''', {'dsoid': self.object_id}
                )
            )
        # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute_batch(commands)
        return CResult.merge_result(self.Success, '元数据和业务元数据处理完毕!')

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
        params = {
            'dsoid': self.object_id,
            'dso_spatial_result': mdt_spatial_result,
            'dso_spatial_parsermemo': mdt_spatial_memo,
            'dso_prj_wkt': mdt_spatial.prj_wkt,
            'dso_prj_proj4': mdt_spatial.prj_proj4,
            'dso_prj_project': mdt_spatial.prj_project,
            'dso_prj_coordinate': mdt_spatial.prj_coordinate,
            'dso_prj_degree': mdt_spatial.prj_degree,
            'dso_prj_zone': mdt_spatial.prj_zone,
            'dso_prj_source': mdt_spatial.prj_source
        }
        database = CFactory().give_me_db(self.file_info.__db_server_id__)

        CDataSet.file2param(params, 'dso_center_native', mdt_spatial.native_center)
        CDataSet.file2param(params, 'dso_geo_bb_native', mdt_spatial.native_box)
        CDataSet.file2param(params, 'dso_geo_native', mdt_spatial.native_geom)

        if CFile.file_or_path_exist(mdt_spatial.wgs84_center):
            dso_center_wgs84 = database.sql.func_wkt2geometry(CFile.file_2_str(mdt_spatial.wgs84_center), self.SRID_WGS84)
        else:
            dso_center_wgs84 = 'null'

        if CFile.file_or_path_exist(mdt_spatial.wgs84_bbox):
            dso_geo_bb_wgs84 = database.sql.func_wkt2geometry(CFile.file_2_str(mdt_spatial.wgs84_bbox), self.SRID_WGS84)
        else:
            dso_geo_bb_wgs84 = 'null'

        if CFile.file_or_path_exist(mdt_spatial.wgs84_geom):
            dso_geo_wgs84 = database.sql.func_wkt2geometry(CFile.file_2_str(mdt_spatial.wgs84_geom), self.SRID_WGS84)
        else:
            dso_geo_wgs84 = 'null'
            # 所有元数据入库
        CFactory().give_me_db(self.file_info.__db_server_id__).execute(
            '''
            update dm2_storage_object
            set dso_spatial_result = :dso_spatial_result
                , dso_spatial_parsermemo = :dso_spatial_parsermemo
                , dso_center_native = :dso_center_native
                , dso_geo_bb_native = :dso_geo_bb_native
                , dso_geo_native = :dso_geo_native
                , dso_center_wgs84 = {0}
                , dso_geo_bb_wgs84 = {1}
                , dso_geo_wgs84 = {2}
                , dso_prj_wkt = :dso_prj_wkt
                , dso_prj_proj4 = :dso_prj_proj4
                , dso_prj_project = :dso_prj_project
                , dso_prj_coordinate = :dso_prj_coordinate
                , dso_prj_degree = :dso_prj_degree
                , dso_prj_zone = :dso_prj_zone
                , dso_prj_source = :dso_prj_source
            where dsoid = :dsoid
            '''.format(dso_center_wgs84, dso_geo_bb_wgs84, dso_geo_wgs84),
            params
        )
        return CResult.merge_result(self.Success, '空间元数据处理完毕!')
