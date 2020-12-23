# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractor import CMDExtractor


class CMDExtractorAttachedFile(CMDExtractor):
    def process(self) -> str:
        """
        在这里提取矢量数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
        :return:
        """
        result = super().process()

        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        metadata_filename = '{0}.xml'.format(metadata_main_name_with_path[:-2])
        format_metadata = self.Transformer_XML

        result = CResult.merge_result_info(result, self.Name_FileName, metadata_filename)
        return CResult.merge_result_info(result, self.Name_Format, format_metadata)
