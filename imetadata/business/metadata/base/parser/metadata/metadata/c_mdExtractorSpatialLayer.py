# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractor import CMDExtractor
from imetadata.database.c_factory import CFactory


class CMDExtractorSpatialLayer(CMDExtractor):
    def process(self) -> str:
        """
        在这里提取矢量数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
        :return:
        """
        result = super().process()
        ds_metadata = CFactory().give_me_db(self.file_info.db_server_id).one_row(
            '''
            select dsometadatatext, dsometadatajson, dsometadataxml
            from dm2_storage_object
            where dsoid = :object_id
            ''',
            {'object_id': self.object_id}
        )
        metadata_filename = CFile.join_file(self.file_content.work_root_dir, '{0}.metadata'.format(self.object_name))
        text_metadata = ds_metadata.value_by_name(0, 'dsometadatatext', None)
        json_metadata = ds_metadata.value_by_name(0, 'dsometadatajson', None)
        xml_metadata = ds_metadata.value_by_name(0, 'dsometadataxml', None)

        format_metadata = self.MetaDataFormat_Text
        if json_metadata is not None:
            format_metadata = self.MetaDataFormat_Json
            CJson.str_2_file(json_metadata, metadata_filename)
        elif xml_metadata is not None:
            format_metadata = self.MetaDataFormat_XML
            CXml.str_2_file(xml_metadata, metadata_filename)
        elif text_metadata is not None:
            format_metadata = self.MetaDataFormat_XML
            CFile.str_2_file(text_metadata, metadata_filename)
        else:
            return result

        result = CResult.merge_result_info(result, self.Name_FileName, metadata_filename)
        return CResult.merge_result_info(result, self.Name_Format, format_metadata)
