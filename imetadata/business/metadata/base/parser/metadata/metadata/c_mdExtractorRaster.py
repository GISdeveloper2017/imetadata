# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:36 
# @Author : 王西亚 
# @File : c_mdExtractorRaster.py
from imetadata.base.c_file import CFile
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractor import CMDExtractor
from imetadata.tool.mdreader.raster.c_rasterMDReader import CRasterMDReader
from multiprocessing import Process


class CMDExtractorRaster(CMDExtractor):
    def process(self) -> str:
        """
        完成 负责人 赵宇飞 在这里提取影像数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        out_metadata_file_fullname = CFile.join_file(self.file_content.work_root_dir, self.FileName_MetaData)
        raster_mdreader = CRasterMDReader(self.file_info.file_name_with_full_path)
        result = CProcessUtils.processing_method(raster_mdreader.get_metadata_2_file, out_metadata_file_fullname)
        # 进程调用模式
        # p_one = Process(target=raster_mdreader.get_metadata_2_file, args=(out_metadata_file_fullname,))
        # p_one.start()
        # p_one.join()
        return CResult.merge_result_info(result, self.Name_Format, self.MetaDataFormat_Json)
        # return CResult.merge_result_info(CResult.merge_result(self.Success, '处理完毕!'), self.Name_Format,
        #                                  self.MetaDataFormat_Text)
