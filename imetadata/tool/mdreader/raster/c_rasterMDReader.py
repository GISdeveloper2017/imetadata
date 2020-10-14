# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 09:02 
# @Author : 王西亚 
# @File : c_rasterMDReader.py
from osgeo import gdal, osr
import math
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.tool.mdreader.c_mdreader import CMDReader


class CRasterMDReader(CMDReader):
    """
     TODO 张源博 栅格数据文件的元数据读取器（已修改过3次）
        新增修改内容：
         1 coordinate节点扩展子节点wkt/esri/proj4
         2 boundingbox扩展子节点，包含原始范围source节点，转为wgs84节点，msg节点（说明转wgs84的结果，转换失败需要说明原因）
         3 pyramid: true/false 判断是否有金字塔
    """

    def get_metadata_2_file(self, file_name_with_path: str):
        # print('你的任务:  将文件{0}的元数据信息, 提取出来, 存储到文件{1}中'.format(self.__file_name_with_path__, file_name_with_path))
        raster_ds = None
        json_raster = None
        try:
            result_success = abs(self.Success)  # 成功的标记，元数据json中的为1，而系统常量为-1，暂采用绝对值
            gdal.AllRegister()
            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")

            # 定义栅格数据的json对像
            json_raster = CJson()

            # 打开影像数据集
            raster_ds = gdal.Open(self.__file_name_with_path__, gdal.GA_ReadOnly)
            if raster_ds is None:
                message = '文件[{0}]打开失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]打开失败!'.format(self.__file_name_with_path__))

            # 基本信息
            driver = raster_ds.GetDriver()
            if driver is None:
                message = '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__))
            # 定义driver子节点,并添加到矢量json对象中
            json_driver = CJson()
            json_driver.set_value_of_name('longname', driver.LongName)
            json_driver.set_value_of_name('shortname', driver.ShortName)
            json_raster.set_value_of_name('driver', json_driver.__json_obj__)

            file_list = raster_ds.GetFileList()
            if file_list is None:
                message = '文件[{0}]读取文件列表失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取文件列表失败!'.format(self.__file_name_with_path__))
            # 定义files子对象
            json_files = [file_list[0]]
            for i in range(len(file_list)):
                if i > 0 and file_list[i] is not None:
                    json_files.append(file_list[i])
            json_raster.set_value_of_name('files', json_files)

            image_size_x = raster_ds.RasterXSize
            image_size_y = raster_ds.RasterYSize
            if image_size_x is None and image_size_y is None:
                message = '文件[{0}]读取文件大小失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取文件大小失败!'.format(self.__file_name_with_path__))
            # 定义size子节点
            json_size = CJson()
            json_size.set_value_of_name('width', image_size_x)
            json_size.set_value_of_name('height', image_size_y)
            json_raster.set_value_of_name('size', json_size.__json_obj__)

            # 投影信息
            projection = raster_ds.GetProjection()
            if projection is None:
                message = '文件[{0}]读取文件投影信息失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取文件投影信息失败!'.format(self.__file_name_with_path__))
            # 定义coordinate子对象
            json_coordinate = CJson()
            spatial = raster_ds.GetSpatialRef()
            if spatial.ImportFromWkt(projection) == gdal.CE_None:
                proj_wkt = spatial.ExportToWkt()
                json_coordinate.set_value_of_name('wkt', proj_wkt)
            else:
                json_coordinate.set_value_of_name('wkt', projection)
            proj4 = spatial.ExportToProj4()
            json_coordinate.set_value_of_name('proj4', proj4)
            esri = spatial.MorphToESRI()
            json_coordinate.set_value_of_name('esri', esri)
            spatial = None
            json_raster.set_value_of_name('coordinate', json_coordinate.__json_obj__)

            # 仿射变换信息
            geo_transform = raster_ds.GetGeoTransform()
            if geo_transform is None:
                message = '文件[{0}]读取文件仿射变换信息失败!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取仿射变换信息失败!'.format(self.__file_name_with_path__))
            # 定义origin、pixelsize、boundingbox子节点
            if geo_transform[2] == 0 and geo_transform[4] == 0:
                (json_origin, json_pixel, json_bounding) = self.get_geotramsform_by_raster(geo_transform, image_size_x,
                                                                                           image_size_y)
                json_raster.set_value_of_name('origin', json_origin.__json_obj__)
                json_raster.set_value_of_name('pixelsize', json_pixel.__json_obj__)
                json_raster.set_value_of_name('boundingbox', json_bounding.__json_obj__)
            else:
                (json_geo, json_bounding) = self.get_geotramsform_by_raster(geo_transform, image_size_x, image_size_y)
                json_raster.set_value_of_name('geotransform', json_geo.__json_obj__)
                json_raster.set_value_of_name('boundingbox', json_bounding.__json_obj__)

            # GCPs信息
            gcp_count = raster_ds.GetGCPCount()
            if gcp_count > 0:
                gcp_projection = raster_ds.GetGCPProjection()
                if gcp_projection is None:
                    message = '文件[{0}]读取GCP信息失败!'.format(self.__file_name_with_path__)
                    json_raster.set_value_of_name('result', self.Failure)
                    json_raster.set_value_of_name('message', message)
                    # 判断路径是否存在，不存在则创建
                    if CFile.check_and_create_directory(file_name_with_path):
                        json_raster.to_file(file_name_with_path)
                    return CResult.merge_result(CResult.Failure,
                                                '文件[{0}]读取GCP信息失败!'.format(self.__file_name_with_path__))
                # 定义gcp_projection、gcp子对象
                json_gcp_projection, gcp_list = self.get_gcp_by_raster(gcp_count, gcp_projection, raster_ds)
                json_raster.set_value_of_name('gcp_projection', json_gcp_projection.__json_obj__)
                json_raster.set_value_of_name('gcp', gcp_list)

            # metadata信息，定义metadata子节点
            metadata = raster_ds.GetMetadata()
            metadata_list = []
            if len(metadata) > 0:
                for i in metadata:
                    if metadata[i] is not None:
                        metadata_item = metadata[i]
                        metadata_list.append(metadata_item)
            json_raster.set_value_of_name('metadata', metadata_list)

            # 定义image_structure_metadata子节点
            image_metadata = raster_ds.GetMetadata('IMAGE_STRUCTURE')
            image_metadata_list = []
            if len(image_metadata) > 0:
                for i in image_metadata:
                    if image_metadata[i] is not None:
                        image_metadata_item = image_metadata[i]
                        image_metadata_list.append(image_metadata_item)
            json_raster.set_value_of_name('image_structure_metadata', image_metadata_list)

            # 定义subdatasets子节点
            sub_metadata = raster_ds.GetMetadata('SUBDATASETS')
            if len(sub_metadata) > 0:
                sub_data = self.get_other_metadata_by_raster(sub_metadata)
                json_raster.set_value_of_name('subdatasets', sub_data.__json_obj__)

            # 定义geolocation子节点
            geo_metadata = raster_ds.GetMetadata('GEOLOCATION')
            if len(geo_metadata) > 0:
                geo_data = self.get_other_metadata_by_raster(geo_metadata)
                json_raster.set_value_of_name('geolocation', geo_data.__json_obj__)

            # 定义rpc子节点
            rpc_metadata = raster_ds.GetMetadata('RPC')
            if len(rpc_metadata) > 0:
                rpc_data = self.get_other_metadata_by_raster(rpc_metadata)
                json_raster.set_value_of_name('rpc', rpc_data.__json_obj__)

            # 角坐标信息，定义corner_coordinates子节点
            json_corner = self.get_corner_by_raster(image_size_x, image_size_y)
            json_raster.set_value_of_name('corner_coordinates', json_corner.__json_obj__)

            # 波段信息
            band_count = raster_ds.RasterCount
            if band_count == 0:
                message = '文件[{0}]文件不存在波段信息!'.format(self.__file_name_with_path__)
                json_raster.set_value_of_name('result', self.Failure)
                json_raster.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_raster.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]不存在波段信息!'.format(self.__file_name_with_path__))
            # 定义bands子节点
            band_list = self.get_bands_by_raster(band_count, raster_ds)
            json_raster.set_value_of_name('bands', band_list)

            # 定义pyramid子节点
            band = raster_ds.GetRasterBand(1)
            overviews = band.GetOverviewCount()
            if overviews > 0:
                pyramid = True
            else:
                pyramid = False
            band = None
            json_raster.set_value_of_name('pyramid', pyramid)

            # 定义result子节点
            json_raster.set_value_of_name('result', result_success)

            if CFile.check_and_create_directory(file_name_with_path):
                json_raster.to_file(file_name_with_path)
            CLogger().info('文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))
            return CResult.merge_result(CResult.Failure,
                                        '文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))

        except Exception as error:
            CLogger().info('get_metadata_2_file解析错误：{0}'.format(error))
            message = 'get_metadata_2_file解析错误：文件：{0},错误信息为{1}'.format(self.__file_name_with_path__, error)
            json_raster.set_value_of_name('result', self.Failure)
            json_raster.set_value_of_name('message', message)
            # 判断路径是否存在，不存在则创建
            if CFile.check_and_create_directory(file_name_with_path):
                json_raster.to_file(file_name_with_path)
            return CResult.merge_result(CResult.Failure,
                                        '文件[{0}]读取异常!｛1｝'.format(self.__file_name_with_path__, error))
        finally:
            del raster_ds

    def get_other_metadata_by_raster(self, other_metadata: dict) -> CJson:
        """
        获取栅格文件的sub、geo、rpc元数据信息
        :param other_metadata:
        :return:
        """
        other_data = CJson()
        other_data.set_value_of_name('valid', True)
        other_metadata_list = []
        for i in other_metadata:
            if other_metadata[i] is not None:
                sub_metadata_item = other_metadata[i]
                other_metadata_list.append(sub_metadata_item)
        other_data.set_value_of_name('metadata', other_metadata_list)
        return other_data

    def get_gcp_by_raster(self, gcp_count: int, gcp_projection, raster_ds):
        """
        获取栅格文件的GCPs信息
        :param gcp_count:
        :param gcp_projection:
        :param raster_ds:
        :return:
        """
        # gcp_projection子对象
        spatial = osr.SpatialReference()
        if spatial.ImportFromWkt(gcp_projection) == gdal.CE_None:
            gcp_proj_wkt = spatial.ExportToWkt()
            gcp_projection = gcp_proj_wkt
        else:
            gcp_projection = gcp_projection
        spatial = None
        json_gcp_projection = CJson()
        json_gcp_projection.set_value_of_name('gcp_projection', gcp_projection)

        # gcp子对象
        gcp_list = []
        for i_gcp in range(gcp_count):
            gcp = raster_ds.GetGCPs() + i_gcp
            gcp_item = CJson()
            gcp_item.set_value_of_name('id', gcp.pszID)
            gcp_item.set_value_of_name('info', gcp.pszINFO)
            gcp_item.set_value_of_name('pixel', gcp.dfGCPPixel)
            gcp_item.set_value_of_name('line', gcp.dfGCPLine)
            gcp_item.set_value_of_name('x', gcp.dfGCPX)
            gcp_item.set_value_of_name('y', gcp.dfGCPY)
            gcp_item.set_value_of_name('z', gcp.dfGCPZ)
            gcp_list.append(gcp_item.__json_obj__)
        return json_gcp_projection, gcp_list

    def get_corner_by_raster(self, image_size_x: int, image_size_y: int) -> CJson:
        """
        处理栅格文件的角坐标信息
        :param image_size_x:
        :param image_size_y:
        :return:
        """
        json_corner = CJson()
        json_point_ul = CJson()
        json_point_ul.set_value_of_name('x', 0)
        json_point_ul.set_value_of_name('y', 0)
        json_corner.set_value_of_name('upper_left', json_point_ul.__json_obj__)
        json_point_ll = CJson()
        json_point_ll.set_value_of_name('x', 0)
        json_point_ll.set_value_of_name('y', image_size_y)
        json_corner.set_value_of_name('lower_left', json_point_ll.__json_obj__)
        json_point_ur = CJson()
        json_point_ur.set_value_of_name('x', image_size_x)
        json_point_ur.set_value_of_name('y', 0)
        json_corner.set_value_of_name('upper_right', json_point_ur.__json_obj__)
        json_point_lr = CJson()
        json_point_lr.set_value_of_name('x', image_size_x)
        json_point_lr.set_value_of_name('y', image_size_y)
        json_corner.set_value_of_name('lower_right', json_point_lr.__json_obj__)
        json_point_center = CJson()
        json_point_center.set_value_of_name('x', image_size_x / 2)
        json_point_center.set_value_of_name('y', image_size_y / 2)
        json_corner.set_value_of_name('center', json_point_center.__json_obj__)
        return json_corner

    def get_geotramsform_by_raster(self, geo_transform: tuple, image_size_x: int, image_size_y: int):
        """
        将仿射变换信息写入json对象
        :param geo_transform:
        :param image_size_x:
        :param image_size_y:
        :return:
        """
        if geo_transform[2] == 0 and geo_transform[4] == 0:
            json_origin = CJson()
            json_origin.set_value_of_name('geotransform0', geo_transform[0])
            json_origin.set_value_of_name('geotransform3', geo_transform[3])

            json_pixel = CJson()
            json_pixel.set_value_of_name('width', geo_transform[1])
            json_pixel.set_value_of_name('height', geo_transform[5])

            point_left_top_x = geo_transform[0]
            point_left_top_y = geo_transform[3]
            point_right_bottom_x = geo_transform[0] + image_size_x * geo_transform[1] + image_size_y * geo_transform[2]
            point_right_bottom_y = geo_transform[3] + image_size_x * geo_transform[4] + image_size_y * geo_transform[5]
            json_bounding = CJson()
            json_source = CJson()
            json_source.set_value_of_name('left', point_left_top_x)
            json_source.set_value_of_name('top', point_left_top_y)
            json_source.set_value_of_name('right', point_right_bottom_x)
            json_source.set_value_of_name('bottom', point_right_bottom_y)
            json_WGS84 = CJson()
            json_bounding.set_value_of_name('source', json_source.__json_obj__)
            json_bounding.set_value_of_name('wgs84', json_WGS84.__json_obj__)
            return json_origin, json_pixel, json_bounding
        else:
            json_geo_transform = CJson()
            json_geo_transform.set_value_of_name('geotransform0', geo_transform[0])
            json_geo_transform.set_value_of_name('geotransform1', geo_transform[1])
            json_geo_transform.set_value_of_name('geotransform2', geo_transform[2])
            json_geo_transform.set_value_of_name('geotransform3', geo_transform[3])
            json_geo_transform.set_value_of_name('geotransform4', geo_transform[4])
            json_geo_transform.set_value_of_name('geotransform5', geo_transform[5])

            point_left_top_x = geo_transform[0]
            point_left_top_y = geo_transform[3]
            point_right_bottom_x = geo_transform[0] + image_size_x * geo_transform[1] + image_size_y * geo_transform[2]
            point_right_bottom_y = geo_transform[3] + image_size_x * geo_transform[4] + image_size_y * geo_transform[5]
            json_bounding = CJson()
            json_source = CJson()
            json_source.set_value_of_name('left', point_left_top_x)
            json_source.set_value_of_name('top', point_left_top_y)
            json_source.set_value_of_name('right', point_right_bottom_x)
            json_source.set_value_of_name('bottom', point_right_bottom_y)
            json_WGS84 = CJson()
            json_bounding.set_value_of_name('source', json_source.__json_obj__)
            json_bounding.set_value_of_name('wgs84', json_WGS84.__json_obj__)
            return json_geo_transform, json_bounding

    def get_bands_by_raster(self, band_count: int, raster_ds) -> list:
        """
        获取波段信息
        :param band_count:
        :param raster_ds:
        :return:
        """
        band_list = []
        for i_band in range(band_count):
            band = raster_ds.GetRasterBand(i_band + 1)
            json_band = CJson()
            (x_block_size, y_block_size) = band.GetBlockSize()
            block = CJson()
            block.set_value_of_name('width', x_block_size)
            block.set_value_of_name('height', y_block_size)
            json_band.set_value_of_name('block', block.__json_obj__)

            band_type = gdal.GetDataTypeName(band.DataType)
            json_band.set_value_of_name('type', band_type)
            color_interp = gdal.GetColorInterpretationName(band.GetRasterColorInterpretation())
            json_band.set_value_of_name('color_interp', color_interp)
            description = band.GetDescription()
            if description is not None and len(description) > 0:
                json_band.set_value_of_name('description', description)

            b_min = band.GetMinimum()
            b_max = band.GetMaximum()
            if b_max is not None or b_min is not None:
                (b_min, b_max) = band.ComputeRasterMinMax(True)
                json_band.set_value_of_name('min', b_min)
                json_band.set_value_of_name('max', b_max)

            no_data = band.GetNoDataValue()
            if no_data is not None:
                if math.isnan(no_data):
                    json_band.set_value_of_name('has_no_data_value', False)
                else:
                    json_band.set_value_of_name('has_no_data_value', True)
                    json_band.set_value_of_name('no_data_value', no_data)

            overviews = band.GetOverviewCount()
            if overviews > 0:
                band_overviews = []
                for i_overview in range(overviews):
                    overview = band.GetOverview(i_overview)
                    if overview is not None:
                        json_overview = CJson()
                        json_overview_size = CJson()
                        json_overview_size.set_value_of_name('width', overview.XSize)
                        json_overview_size.set_value_of_name('height', overview.YSize)
                        json_overview.set_value_of_name('size', json_overview_size.__json_obj__)
                        resampling = overview.GetMetadataItem('RESAMPLING')
                        if resampling is not None and resampling == 'AVERAGE_BIT2':
                            json_overview.set_value_of_name('resampling', '*')
                        band_overviews.append(json_overview.__json_obj__)
                json_band.set_value_of_name('overviews', band_overviews)

            if band.HasArbitraryOverviews():
                json_band.set_value_of_name('has_arbitrary_overview', True)

            json_mask = CJson()
            json_mask.set_value_of_name('valid', True)
            mask_flags = band.GetMaskFlags()
            if mask_flags:
                mask_band = band.GetMaskBand()
                if mask_band is not None and mask_band.GetOverviewCount() > 0:
                    mask_overviews = []
                    for i_overview in range(mask_band.GetOverviewCount()):
                        mask_overview = mask_band.GetOverview(i_overview)
                        if mask_overview is not None:
                            json_mask_overview_size = CJson()
                            json_mask_overview_size.set_value_of_name('width', mask_overview.XSize)
                            json_mask_overview_size.set_value_of_name('height', mask_overview.YSize)
                            mask_overviews.append(json_mask_overview_size.__json_obj__)
                    json_mask.set_value_of_name('overviews', mask_overviews)
            json_band.set_value_of_name('mask', json_mask.__json_obj__)

            unit = band.GetUnitType()
            if len(unit) > 0:
                band_unit = CJson()
                band_unit.set_value_of_name('type', unit)
                json_band.set_value_of_name('unit', band_unit.__json_obj__)

            category = band.GetRasterCategoryNames()
            if category is not None:
                categories = []
                for i in category:
                    if category[i] is not None:
                        value = category[i]
                        categories.append(value)
                json_band.set_value_of_name('categories', categories)

            scale = band.GetScale()
            offset = band.GetOffset()
            if scale != 1.0 or offset != 0:
                json_band.set_value_of_name('scale', scale)
                json_band.set_value_of_name('offset', offset)

            band_metadata = band.GetMetadata()
            if band_metadata is not None:
                metadata = []
                for i in band_metadata:
                    value = band_metadata[i]
                    metadata.append(value)
                json_band.set_value_of_name('metadata', metadata)

            band_image_metadata = band.GetMetadata('IMAGE_STRUCTURE')
            if band_image_metadata is not None:
                image_metadata = []
                for i in band_image_metadata:
                    value = band_image_metadata[i]
                    image_metadata.append(value)
                json_band.set_value_of_name('image_structure_metadata', image_metadata)

            color_table = band.GetRasterColorTable()
            # print(dir(color_table))
            if color_interp == 'Palette' and color_table is not None:
                json_color_table = CJson()
                palette_interpretation = gdal.GetPaletteInterpretationName(color_table.GetPaletteInterpretation())
                entry_count = color_table.GetCount()
                json_color_table.set_value_of_name('palette_interpretation_name', palette_interpretation)
                json_color_table.set_value_of_name('entry_count', entry_count)

                color_entry = []
                for i in range(entry_count):
                    entry = color_table.GetColorEntry(i)
                    entry_RGB = color_table.GetColorEntryAsRGB(i, entry)
                    # print(dir(entry_RGB))
                    json_color_entry = CJson()
                    json_color_entry.set_value_of_name('color', entry_RGB)
                    color_entry.append(json_color_entry.__json_obj__)
                json_color_table.set_value_of_name('entrys', color_entry)
                json_band.set_value_of_name('color_table', json_color_table.__json_obj__)

            band_list.append(json_band.__json_obj__)
            band = None
        return band_list


if __name__ == '__main__':
    # CRasterMDReader('/aa/bb/cc.img').get_metadata_2_file('/aa/bb/cc.json')
    CRasterMDReader(r'D:\App\test\镶嵌影像\石嘴山市-3.img').get_metadata_2_file(r'D:\test\raster_test\石嘴山市-3.json')
    # CRasterMDReader(r'D:\test\wsiearth-tif\wsiearth.tif').get_metadata_2_file(
    #     r'D:\test\raster_test\wsiearth.json')
    # CRasterMDReader(r'D:\test\DOM\广西影像数据\2772.0-509.0\2772.0-509.0.img').get_metadata_2_file(
    #     r'D:\test\raster_test\2772.0-509.0-1.json')
    # CRasterMDReader(r'D:\test\DOM\湖北单个成果数据\H49G001026\H49G001026.tif').get_metadata_2_file(
    #     r'D:\test\raster_test\H49G001026.json')
    # CRasterMDReader(r'D:\test\DOM\湖北单个成果数据\H49G001026\HG.tif').get_metadata_2_file(
    #     r'D:\test\raster_test\HG.json')
    # CRasterMDReader(r'D:\test\DOM\湖南标准分幅成果数据\G49G001030\G49G001030.tif').get_metadata_2_file(
    #     r'D:\test\raster_test\G49G001030.json')
    # CRasterMDReader(r'D:\test\卫星数据\单目录单数据\GF1_PMS1_E65.2_N26.6_20130927_L1A0000090284\GF1_PMS1_E65.2_N26'
    #                 r'.6_20130927_L1A0000090284-PAN1.tiff').get_metadata_2_file(
    #     r'D:\test\raster_test\GF1_PMS1_E65.2_N26.6_20130927_L1A0000090284-PAN1.json')
    # CRasterMDReader(r'D:\test\卫星数据\一目录单数据\GF1_PMS1_E85.9_N44.1_20140821_L1A0000311315-PAN1.tiff').get_metadata_2_file(
    #     r'D:\test\raster_test\GF1_PMS1_E85.9_N44.1_20140821_L1A0000311315-PAN1_dem.json')
