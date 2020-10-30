# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractor import CSpatialExtractor


class CSpatialExtractorVector(CSpatialExtractor):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取矢量数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
            注意返回的串中有空间信息的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        # result = CResult.merge_result(self.Success, '处理完毕!')
        # result = CResult.merge_result_info(result, self.Name_Native_Center, '/aa/bb_native_center.wkt')
        # result = CResult.merge_result_info(result, self.Name_Native_BBox, '/aa/bb_native_bbox.wkt')
        # result = CResult.merge_result_info(result, self.Name_Native_Geom, '/aa/bb_native_geom.wkt')
        # result = CResult.merge_result_info(result, self.Name_Wgs84_Center, '/aa/bb_wgs84_center.wkt')
        # result = CResult.merge_result_info(result, self.Name_Wgs84_BBox, '/aa/bb_wgs84_bbox.wkt')
        # result = CResult.merge_result_info(result, self.Name_Wgs84_Geom, '/aa/bb_wgs84_geom.wkt')
        # return result

        result_process = self.process_vector()
        if CResult.result_success(result_process):
            result = CResult.merge_result(self.Success, '处理完毕!')
            result = CResult.merge_result_info(result, self.Name_Native_Center,
                                               '/{0}_native_center.wkt'.format(self.object_name))
            result = CResult.merge_result_info(result, self.Name_Native_BBox,
                                               '/{0}_native_bbox.wkt'.format(self.object_name))
            result = CResult.merge_result_info(result, self.Name_Native_Geom,
                                               '/{0}_native_geom.wkt'.format(self.object_name))
            result = CResult.merge_result_info(result, self.Name_Wgs84_Center,
                                               '/{0}_wgs84_center.wkt'.format(self.object_name))
            result = CResult.merge_result_info(result, self.Name_Wgs84_BBox,
                                               '/{0}_wgs84_bbox.wkt'.format(self.object_name))
            result = CResult.merge_result_info(result, self.Name_Wgs84_Geom,
                                               '/{0}_wgs84_geom.wkt'.format(self.object_name))
        else:
            result = CResult.merge_result(self.Failure, CResult.result_message(result_process))
        return result

    def process_vector(self) -> bool:
        try:
            # file_name_with_full_path = r'D:\test\vector_test\石嘴山市-3xq.json'
            # file_main_name = CFile.file_main_name(file_name_with_full_path)
            # file_path = CFile.file_path(file_name_with_full_path)
            str_metadata_json = self.metadata.metadata_json()
            json_obj = CJson()
            json_obj.load_json_text(str_metadata_json)
            # json_obj.load_file(file_name_with_full_path)

            wkt_info = 'POLYGON((min_x max_y,max_x max_y,max_x min_y,min_x min_y,min_x max_y))'

            native_max_x = json_obj.xpath_one('layers[0].extent.maxx', 0)
            native_max_y = json_obj.xpath_one('layers[0].extent.maxy', 0)
            native_min_x = json_obj.xpath_one('layers[0].extent.minx', 0)
            native_min_y = json_obj.xpath_one('layers[0].extent.miny', 0)

            native_dict = {'max_x': CUtils.any_2_str(native_max_x),
                           'max_y': CUtils.any_2_str(native_max_y),
                           'min_x': CUtils.any_2_str(native_min_x),
                           'min_y': CUtils.any_2_str(native_min_y)}

            center_x = (native_max_x - native_min_x) / 2 + native_min_x
            center_y = (native_max_y - native_min_y) / 2 + native_min_y
            native_center = 'POINT({0} {1})'.format(center_x, center_y)

            native_bbox = wkt_info
            for name, value in native_dict.items():
                native_bbox = native_bbox.replace(name, value)
            geom_native = native_bbox

            file_path = self.file_content.work_root_dir
            file_main_name = self.object_name

            native_center_filepath = CFile.join_file(file_path, file_main_name + '_native_center.wkt')
            CFile.str_2_file(native_center, native_center_filepath)
            native_bbox_filepath = CFile.join_file(file_path, file_main_name + '_native_bbox.wkt')
            CFile.str_2_file(native_bbox, native_bbox_filepath)
            native_geom_filepath = CFile.join_file(file_path, file_main_name + '_native_geom.wkt')
            CFile.str_2_file(geom_native, native_geom_filepath)

            wgs84_max_x = CUtils.to_decimal(json_obj.xpath_one('layers[0].wgs84.extent.maxx', 0))
            wgs84_max_y = CUtils.to_decimal(json_obj.xpath_one('layers[0].wgs84.extent.maxy', 0))
            wgs84_min_x = CUtils.to_decimal(json_obj.xpath_one('layers[0].wgs84.extent.minx', 0))
            wgs84_min_y = CUtils.to_decimal(json_obj.xpath_one('layers[0].wgs84.extent.miny', 0))

            wgs84_dict = {'max_x': CUtils.any_2_str(wgs84_max_x),
                          'max_y': CUtils.any_2_str(wgs84_max_y),
                          'min_x': CUtils.any_2_str(wgs84_min_x),
                          'min_y': CUtils.any_2_str(wgs84_min_y)}

            center_x = (wgs84_max_x - wgs84_min_x) / 2 + wgs84_min_x
            center_y = (wgs84_max_y - wgs84_min_y) / 2 + wgs84_min_y
            wgs84_center = 'POINT({0} {1})'.format(center_x, center_y)

            wgs84_bbox = wkt_info
            for name, value in wgs84_dict.items():
                wgs84_bbox = wgs84_bbox.replace(name, value)
            wgs84_geom = wgs84_bbox

            wgs84_center_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_center.wkt')
            CFile.str_2_file(wgs84_center, wgs84_center_filepath)
            wgs84_bbox_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_bbox.wkt')
            CFile.str_2_file(wgs84_bbox, wgs84_bbox_filepath)
            wgs84_geom_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_geom.wkt')
            CFile.str_2_file(wgs84_geom, wgs84_geom_filepath)
            return CResult.merge_result(self.Success, '处理完毕!')
        except Exception as error:
            CLogger().warning('影像数据的空间信息处理出现异常, 错误信息为: {0}'.format(error.__str__))
            return CResult.merge_result(self.Failure, '影像数据的空间信息处理出现异常,错误信息为：{0}!'.format(error.__str__))
