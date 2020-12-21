# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:36 
# @Author : 王西亚 
# @File : c_mdExtractorRaster.py
from osgeo import osr

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractor import CSpatialExtractor
from imetadata.tool.geomwkt_tool.md_img2wkt import process_bus


class CSpatialExtractorRaster(CSpatialExtractor):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取影像数据的空间信息, 以文件形式存储在self.file_content.work_root_dir下
            注意返回的串中有空间信息的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        result_process = self.process_raster()
        if CResult.result_success(result_process):
            file_path = self.file_content.work_root_dir
            dict_temp_file_name = {
                self.Name_Native_Center: '{0}_native_center.wkt'.format(self.object_name),
                self.Name_Native_BBox: '{0}_native_bbox.wkt'.format(self.object_name),
                self.Name_Native_Geom: '{0}_native_geom.wkt'.format(self.object_name),
                self.Name_Wgs84_Center: '{0}_wgs84_center.wkt'.format(self.object_name),
                self.Name_Wgs84_BBox: '{0}_wgs84_bbox.wkt'.format(self.object_name),
                self.Name_Wgs84_Geom: '{0}_wgs84_geom.wkt'.format(self.object_name)
            }
            dict_temp_prj_name = {
                self.Name_Prj_Wkt: CResult.result_info(result_process, self.Name_Prj_Wkt, None),
                self.Name_Prj_Proj4: CResult.result_info(result_process, self.Name_Prj_Proj4, None),
                self.Name_Prj_Project: CResult.result_info(result_process, self.Name_Prj_Project, None),
                self.Name_Prj_Coordinate: CResult.result_info(result_process, self.Name_Prj_Coordinate, None),
                self.Name_Prj_Source: CResult.result_info(result_process, self.Name_Prj_Source, None),
                self.Name_Prj_Zone: CResult.result_info(result_process, self.Name_Prj_Zone, None),
                self.Name_Prj_Degree: CResult.result_info(result_process, self.Name_Prj_Degree, None)
            }
            result = CResult.merge_result(self.Success, '处理完毕!')
            for file_type, file_name in dict_temp_file_name.items():
                result = CResult.merge_result_info(result, file_type, CFile.join_file(file_path, file_name))
            for prj_type, prj_name in dict_temp_prj_name.items():
                result = CResult.merge_result_info(result, prj_type, prj_name)
        else:
            result = CResult.merge_result(self.Failure, CResult.result_message(result_process))
        return result

    def process_raster(self) -> str:
        try:
            # file_name_with_full_path = r'D:\test\raster_test\石嘴山市.json'
            # file_main_name = CFile.file_main_name(file_name_with_full_path)
            # file_path = CFile.file_path(file_name_with_full_path)
            json_obj = self.metadata.metadata_json()
            # json_obj.load_file(file_name_with_full_path)

            # <editor-fold desc="1.空间坐标信息">
            wkt_info = 'POLYGON((min_x max_y,max_x max_y,max_x min_y,min_x min_y,min_x max_y))'

            # 四至坐标
            native_max_x = CUtils.to_decimal(json_obj.xpath_one('boundingbox.right', None))
            native_max_y = CUtils.to_decimal(json_obj.xpath_one('boundingbox.top', None))
            native_min_x = CUtils.to_decimal(json_obj.xpath_one('boundingbox.left', None))
            native_min_y = CUtils.to_decimal(json_obj.xpath_one('boundingbox.bottom', None))
            if (native_max_x is None) or (native_max_y is None) or (native_min_x is None) or (native_min_y is None):
                native_center_wkt = None
                native_bbox_wkt = None
                native_geom_wkt = None
            else:
                dict_native = {'max_x': CUtils.any_2_str(native_max_x),
                               'max_y': CUtils.any_2_str(native_max_y),
                               'min_x': CUtils.any_2_str(native_min_x),
                               'min_y': CUtils.any_2_str(native_min_y)}

                # 中心点坐标
                center_x = (native_max_x - native_min_x) / 2 + native_min_x
                center_y = (native_max_y - native_min_y) / 2 + native_min_y
                native_center_wkt = 'POINT({0} {1})'.format(center_x, center_y)

                # 外边框、外包框
                native_bbox_wkt = wkt_info
                for name, value in dict_native.items():
                    native_bbox_wkt = native_bbox_wkt.replace(name, value)
                native_geom_wkt = native_bbox_wkt

            file_path = self.file_content.work_root_dir
            file_main_name = self.object_name
            native_center_filepath = CFile.join_file(file_path, file_main_name + '_native_center.wkt')
            CFile.str_2_file(native_center_wkt, native_center_filepath)
            native_bbox_filepath = CFile.join_file(file_path, file_main_name + '_native_bbox.wkt')
            CFile.str_2_file(native_bbox_wkt, native_bbox_filepath)
            native_geom_filepath = CFile.join_file(file_path, file_main_name + '_native_geom.wkt')
            CFile.str_2_file(native_geom_wkt, native_geom_filepath)

            # wgs84转换后的四至坐标
            wgs84_max_x = CUtils.to_decimal(json_obj.xpath_one('wgs84.boundingbox.right', None))
            wgs84_max_y = CUtils.to_decimal(json_obj.xpath_one('wgs84.boundingbox.top', None))
            wgs84_min_x = CUtils.to_decimal(json_obj.xpath_one('wgs84.boundingbox.left', None))
            wgs84_min_y = CUtils.to_decimal(json_obj.xpath_one('wgs84.boundingbox.bottom', None))
            if (wgs84_max_x is None) or (wgs84_max_y is None) or (wgs84_min_x is None) or (wgs84_min_y is None):
                wgs84_center_wkt = None
                wgs84_bbox_wkt = None
            else:
                dict_wgs84 = {'max_x': CUtils.any_2_str(wgs84_max_x),
                              'max_y': CUtils.any_2_str(wgs84_max_y),
                              'min_x': CUtils.any_2_str(wgs84_min_x),
                              'min_y': CUtils.any_2_str(wgs84_min_y)}

                # 中心点坐标（wgs84）
                center_x = (wgs84_max_x - wgs84_min_x) / 2 + wgs84_min_x
                center_y = (wgs84_max_y - wgs84_min_y) / 2 + wgs84_min_y
                wgs84_center_wkt = 'POINT({0} {1})'.format(center_x, center_y)

                # 外边框、外包框（wgs84)
                wgs84_bbox_wkt = wkt_info
                for name, value in dict_wgs84.items():
                    wgs84_bbox_wkt = wgs84_bbox_wkt.replace(name, value)
                # wgs84_geom_wkt = wgs84_bbox_wkt
                wgs84_geom_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_geom.wkt')
                # CFile.str_2_file(wgs84_geom_wkt, wgs84_geom_filepath)
                object_file_path = self.file_info.file_name_with_full_path
                process_bus(object_file_path, wgs84_geom_filepath, None)

            wgs84_center_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_center.wkt')
            CFile.str_2_file(wgs84_center_wkt, wgs84_center_filepath)
            wgs84_bbox_filepath = CFile.join_file(file_path, file_main_name + '_wgs84_bbox.wkt')
            CFile.str_2_file(wgs84_bbox_wkt, wgs84_bbox_filepath)
            # </editor-fold>

            # <editor-fold desc="2.投影信息">
            native_wkt = json_obj.xpath_one('coordinate.wkt', None)
            native_proj4 = json_obj.xpath_one('coordinate.proj4', None)
            native_source = CResource.Prj_Source_Data

            # 坐标系
            native_coordinate = None
            # 3度带/6度带
            native_degree = None
            # 投影方式
            native_project = None
            # 带号
            native_zone = None

            # 创建SpatialReference对象，导入wkt信息
            spatial_ref = osr.SpatialReference(wkt=native_wkt)
            if spatial_ref.IsProjected():
                native_coordinate = spatial_ref.GetAttrValue('GEOGCS')
                native_project = spatial_ref.GetAttrValue('PROJECTION')
                # native_degree = spatial_ref.GetAttrValue('GEOGCS|UNIT', 1)
                # pixel_size = json_obj.xpath_one('pixelsize.width', None)
                # native_zone = self.get_prj_zone(spatial_ref, pixel_size)
                native_degree, native_zone = self.get_prj_degree_zone(spatial_ref)
            elif spatial_ref.IsGeocentric():
                native_project = None
                native_coordinate = spatial_ref.GetAttrValue('GEOGCS')
                native_degree = None
                native_zone = None
            # </editor-fold>

            result = CResult.merge_result(self.Success, '处理完毕!')
            result = CResult.merge_result_info(result, self.Name_Prj_Wkt, native_wkt)
            result = CResult.merge_result_info(result, self.Name_Prj_Proj4, native_proj4)
            result = CResult.merge_result_info(result, self.Name_Prj_Project, native_project)
            result = CResult.merge_result_info(result, self.Name_Prj_Coordinate, native_coordinate)
            result = CResult.merge_result_info(result, self.Name_Prj_Source, native_source)
            result = CResult.merge_result_info(result, self.Name_Prj_Zone, native_zone)
            result = CResult.merge_result_info(result, self.Name_Prj_Degree, native_degree)
            return result
            # return CResult.merge_result(self.Success, '处理完毕!')
        except Exception as error:
            CLogger().warning('影像数据的空间信息处理出现异常, 错误信息为: {0}'.format(error.__str__))
            return CResult.merge_result(self.Failure, '影像数据的空间信息处理出现异常,错误信息为：{0}!'.format(error.__str__))
