# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractor import CSpatialExtractor


class CSpatialExtractorVector(CSpatialExtractor):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取矢量数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
            注意返回的串中有空间信息的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        result = CResult.merge_result(self.Success, '处理完毕!')
        result = CResult.merge_result_info(result, self.Name_Native_Center, '/aa/bb_native_center.wkt')
        result = CResult.merge_result_info(result, self.Name_Native_BBox, '/aa/bb_native_bbox.wkt')
        result = CResult.merge_result_info(result, self.Name_Native_Geom, '/aa/bb_native_geom.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_Center, '/aa/bb_wgs84_center.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_BBox, '/aa/bb_wgs84_bbox.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_Geom, '/aa/bb_wgs84_geom.wkt')
        return result
