# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:36 
# @Author : 王西亚 
# @File : c_mdExtractorRaster.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractor import CSpatialExtractor


class CSpatialExtractorRaster(CSpatialExtractor):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取影像数据的空间信息, 以文件形式存储在self.file_content.work_root_dir下
            注意返回的串中有空间信息的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        file_name_with_full_path = self.file_info.__file_name_with_full_path__
        file_main_name = self.file_info.__file_main_name__
        self.metadata.metadata_json().json_attr_value()

        result = CResult.merge_result(self.Success, '处理完毕!')
        result = CResult.merge_result_info(result, self.Name_Native_Center, '/aa/bb_native_center.wkt')
        result = CResult.merge_result_info(result, self.Name_Native_BBox, '/aa/bb_native_bbox.wkt')
        result = CResult.merge_result_info(result, self.Name_Native_Geom, '/aa/bb_native_geom.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_Center, '/aa/bb_wgs84_center.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_BBox, '/aa/bb_wgs84_bbox.wkt')
        result = CResult.merge_result_info(result, self.Name_Wgs84_Geom, '/aa/bb_wgs84_geom.wkt')
        return result
