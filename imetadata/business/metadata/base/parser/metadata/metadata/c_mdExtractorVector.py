# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractor import CMDExtractor


class CMDExtractorVector(CMDExtractor):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取栅格数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
        :return:
        """
        return CUtils.merge_result_info(CUtils.merge_result(self.Success, '处理完毕!'), self.Name_Format, self.MetaDataFormat_Text)
