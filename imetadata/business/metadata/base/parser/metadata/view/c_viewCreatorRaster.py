# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 12:03 
# @Author : 王西亚 
# @File : c_viewCreatorRaster.py

import os
import numpy as np
from PIL import Image
from osgeo import gdal, gdalconst

from imetadata.base.c_json import CJson
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_time import CTime
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreator import CViewCreator
from imetadata.database.c_factory import CFactory


class CViewCreatorRaster(CViewCreator):
    """
    单个影像抽取快视图、拇指图，生成重采样后的geotiff文件（可用于数据集（多个影像）抽取快视图）
    """

    def process(self) -> str:
        """
        完成 负责人 张源博、赵宇飞 在这里提取影像数据的快视图, 将元数据文件存储在self.file_content.view_root_dir下
            注意返回的串中有快视图和拇指图的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        # 获取对象类型
        sql_query = '''
                    select dsodtitle from dm2_storage_object_def 
                    left join dm2_storage_object on dm2_storage_object.dsoobjecttype = dm2_storage_object_def.dsodid
                    where dm2_storage_object.dsoid = '{0}'
                '''.format(self.object_id)
        object_def_title = CFactory().give_me_db(self.file_info.db_server_id).one_value(sql_query)

        create_time = CTime.today()
        create_format_time = CTime.format_str(create_time, '%Y%m%d')
        year = CTime.format_str(create_time, '%Y')
        month = CTime.format_str(create_time, '%m')
        day = CTime.format_str(create_time, '%d')
        relative_path_part = r'{0}\{1}\{2}\{3}'.format(object_def_title, year, month, day)  # 相对路径格式
        view_relative_path_browse = r'\{0}\{1}_browse.png'.format(relative_path_part, self.object_id)
        view_relative_path_thumb = r'\{0}\{1}_thumb.jpg'.format(relative_path_part, self.object_id)
        view_relative_path_geotiff = r'\{0}\{1}_browse.tiff'.format(relative_path_part, self.object_id)

        browse_full_path = CFile.join_file(self.file_content.view_root_dir, view_relative_path_browse)
        thumb_full_path = CFile.join_file(self.file_content.view_root_dir, view_relative_path_thumb)
        geotiff_full_path = CFile.join_file(self.file_content.view_root_dir, view_relative_path_geotiff)

        # 进程调用模式
        json_out_view = CJson()
        json_out_view.set_value_of_name('image_path', self.file_info.file_name_with_full_path)
        json_out_view.set_value_of_name('browse_full_path', browse_full_path)
        json_out_view.set_value_of_name('thumb_full_path', thumb_full_path)
        json_out_view.set_value_of_name('geotiff_full_path', geotiff_full_path)

        result_view = CProcessUtils.processing_method(self.create_view_json, json_out_view)
        # result_view = self.create_view(self.file_info.file_name_with_full_path, browse_full_path, thumb_full_path,
        #                                geotiff_full_path)
        # result_view = self.create_view_json(json_out_view)
        if CResult.result_success(result_view):
            result = CResult.merge_result(self.Success, '处理完毕!')
            result = CResult.merge_result_info(result, self.Name_Browse, view_relative_path_browse)
            result = CResult.merge_result_info(result, self.Name_Thumb, view_relative_path_thumb)
            result = CResult.merge_result_info(result, self.Name_Browse_GeoTiff, view_relative_path_geotiff)
        else:
            result = CResult.merge_result(self.Failure, CResult.result_message(result_view))
        return result

    def create_view_json(self, params_json: CJson):
        """
        设置为一个参数，供进程调用
        """
        image_path = params_json.xpath_one('image_path', None)
        browse_full_path = params_json.xpath_one('browse_full_path', None)
        thumb_full_path = params_json.xpath_one('thumb_full_path', None)
        geotiff_full_path = params_json.xpath_one('geotiff_full_path', None)
        result = self.create_view(image_path, browse_full_path, thumb_full_path, geotiff_full_path)
        return result

    def create_view(self, image_path: str, browse_path: str, thumb_path: str, geotiff_path: str):
        """
        由影像文件生成拇指图(jpg)、快视图(png)。
        对多波段影像、单波段影像，波段数据类型为Byte（8位无符号整型）、UInt16（16位无符号整型）、Int16（16位有符号整型）的影像，均可进行转换。
        注意：转换过程中重采样会生成影像临时文件(tiff),保留原影像基本信息，仅压缩影像尺寸。
        快视图：500*xxx（width固定为500，height根据对应比例计算）
        拇指图：50*50（按固定尺寸生成）
        :param image_path: 单个影像文件
        :param browse_path: 指定的快视图地址
        :param thumb_path: 指定的拇指图地址
        :param geotiff_path: 临时文件存放地址
        :return:
        """
        # 注册所有驱动，支持中文
        gdal.AllRegister()
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        try:
            # <editor-fold desc="重采样">
            # 获取并检查影像文件
            source_ds = gdal.Open(image_path, gdalconst.GA_ReadOnly)
            if source_ds is None:
                CLogger().warning('文件[{0}]打开失败！请检查！'.format(image_path))
                return CResult.merge_result(self.Failure, '文件[{0}]打开失败！请检查！'.format(image_path))
            band_count = source_ds.RasterCount
            if band_count == 0:
                CLogger().warning('文件[{0}]不存在波段信息！请检查!'.format(image_path))
                return CResult.merge_result(self.Failure, '文件[{0}]不存在波段信息！请检查!'.format(image_path))

            # 获取影像的大小、投影、仿射变换参数、第一个波段信息、数据类型
            cols = source_ds.RasterXSize
            rows = source_ds.RasterYSize
            projection = source_ds.GetProjection()
            geo_transform = list(source_ds.GetGeoTransform())
            in_band1 = source_ds.GetRasterBand(1)
            data_type = in_band1.DataType
            # 获取MEM的驱动（GDAL内存文件）、GTiff驱动
            driver_mem = gdal.GetDriverByName('MEM')
            driver_GeoTiff = gdal.GetDriverByName('GTiff')

            # 制作拇指图
            # 设置拇指图尺寸
            thumb_cols = 50
            thumb_rows = 50
            scale1 = thumb_cols / cols
            scale2 = thumb_rows / rows
            geo_transform[1] = geo_transform[1] / scale1
            geo_transform[5] = geo_transform[5] / scale2

            # 配置拇指图内存临时文件thumb_ds
            thumb_ds = driver_mem.Create("", xsize=thumb_cols, ysize=thumb_rows, bands=band_count, eType=data_type)
            thumb_ds.SetProjection(projection)
            thumb_ds.SetGeoTransform(geo_transform)
            for index in range(band_count):
                in_band = source_ds.GetRasterBand(index + 1)
                data = in_band.ReadAsArray(buf_xsize=thumb_cols, buf_ysize=thumb_rows)
                out_band = thumb_ds.GetRasterBand(index + 1)
                out_band.WriteArray(data)
                out_band.FlushCache()
                out_band.ComputeBandStats(False)

            # 制作快视图
            # 设置快视图尺寸
            browse_cols = 500
            scale = browse_cols / cols
            browse_rows = rows * scale
            browse_rows = CUtils.to_integer(browse_rows)
            geo_transform[1] = geo_transform[1] / scale
            geo_transform[5] = geo_transform[5] / scale

            # 如果已存在同名影像，则删除之
            if os.path.exists(geotiff_path) and os.path.isfile(geotiff_path):  # 如果已存在同名影像
                os.remove(geotiff_path)
            # 配置快视图内存临时文件browse_ds
            CFile.check_and_create_directory(geotiff_path)  # 创建目录
            browse_ds = driver_GeoTiff.Create(geotiff_path, xsize=browse_cols, ysize=browse_rows, bands=band_count,
                                              eType=data_type)
            browse_ds.SetProjection(projection)
            browse_ds.SetGeoTransform(geo_transform)
            for index in range(band_count):
                in_band = source_ds.GetRasterBand(index + 1)
                data = in_band.ReadAsArray(buf_xsize=browse_cols, buf_ysize=browse_rows)
                out_band = browse_ds.GetRasterBand(index + 1)
                out_band.WriteArray(data)
                out_band.FlushCache()
                out_band.ComputeBandStats(False)
            # </editor-fold>

            # 由重采样后的影像制作快视图、拇指图
            browse_path = self.image2view(browse_ds, browse_path)
            thumb_path = self.image2view(thumb_ds, thumb_path)

            if os.path.exists(thumb_path) and os.path.exists(browse_path) and os.path.exists(geotiff_path):
                CLogger().info('文件[{0}]的快视图、拇指图制作成功!'.format(image_path))
                return CResult.merge_result(self.Success, '文件[{0}]快视图、拇指图制作成功!'.format(image_path))
            else:
                CLogger().warning('文件[{0}]处理失败！未生成相应的快视图、拇指图！'.format(image_path))
                return CResult.merge_result(self.Failure, '文件[{0}]处理失败！未生成相应的快视图、拇指图！'.format(image_path))
        except Exception as error:
            CLogger().warning('影像数据的快视图、拇指图信息处理出现异常，错误信息为：{0}'.format(error.__str__))
            return CResult.merge_result(self.Failure, '影像数据的快视图、拇指图信息处理出现异常，错误信息为：{0}!'.format(error.__str__))
        finally:
            del source_ds
            del thumb_ds
            del browse_ds

    def image2view(self, target_ds, view_path: str) -> str:
        """
        影像文件转jpg或png
        对波段数据类型为Byte（8位无符号整型）的影像，可采用gdal.Translate()方法直接进行文件格式转换。
        对波段数据类型为UInt16（16位无符号整型）、Int16（16位有符号整型）的影像：
        由于JPEG不支持16位影像的转换，且PNG转换效果非常不理想，图像轮廓模糊。
        因此对16位影像采用百分比截断的方法压缩至0~255的范围，改变了像素深度，降低到8位。
        该方法生成的快视图的转换效果与gdal.Translate()方法生成的相比，图像轮廓清晰，可辨识度高。
        注：gdal == 3.1.3
        :param target_ds: 影像临时文件的数据集
        :param view_path: 快视图或拇指图文件地址
        :return:
        """
        cols = target_ds.RasterXSize
        rows = target_ds.RasterYSize
        band_count = target_ds.RasterCount
        band = target_ds.GetRasterBand(1)
        data_type_name = gdal.GetDataTypeName(band.DataType)

        # 检查影像位深度（波段数据类型）
        if CUtils.equal_ignore_case(data_type_name, 'Byte'):
            # 对波段数据类型为Byte（8位无符号整型）的影像进行转换
            if CFile.check_and_create_directory(view_path):
                if CFile.file_ext(view_path).lower() == 'jpg':
                    out = gdal.Translate(view_path, target_ds, format='JPEG')
                elif CFile.file_ext(view_path).lower() == 'png':
                    out = gdal.Translate(view_path, target_ds, format='PNG')
        else:
            # 对波段数据类型为UInt16（16位无符号整型）、Int16（16位有符号整型）的影像进行转换
            # 检查影像波段数并读取
            if band_count >= 3:
                bandsOrder = [3, 2, 1]
                data = np.empty([rows, cols, 3], dtype=float)
                for i in range(3):
                    band = target_ds.GetRasterBand(bandsOrder[i])
                    data1 = band.ReadAsArray(0, 0, cols, rows)
                    data[:, :, i] = data1

                if CFile.check_and_create_directory(view_path):
                    # 百分比截断压缩影像，将像元取值限定在0~255
                    lower_percent = 0.6
                    higher_percent = 99.4
                    n = data.shape[2]
                    out = np.zeros_like(data, dtype=np.uint8)
                    for i in range(n):
                        a = 0
                        b = 255
                        c = np.percentile(data[:, :, i], lower_percent)
                        d = np.percentile(data[:, :, i], higher_percent)
                        t = a + (data[:, :, i] - c) * (b - a) / (d - c)
                        t[t < a] = a
                        t[t > b] = b
                        out[:, :, i] = t
                    outImg = Image.fromarray(np.uint8(out))
                    outImg.save(view_path)
            else:
                data = np.empty([rows, cols], dtype=float)
                band = target_ds.GetRasterBand(1)
                data1 = band.ReadAsArray(0, 0, cols, rows)
                data[:, :] = data1

                if CFile.check_and_create_directory(view_path):
                    # 百分比截断压缩影像，将像元取值限定在0~255
                    lower_percent = 0.6
                    higher_percent = 99.4
                    out = np.zeros_like(data, dtype=np.uint8)
                    a = 0
                    b = 255
                    c = np.percentile(data[:, :], lower_percent)
                    d = np.percentile(data[:, :], higher_percent)
                    t = a + (data[:, :] - c) * (b - a) / (d - c)
                    t[t < a] = a
                    t[t > b] = b
                    out[:, :] = t
                    outImg = Image.fromarray(np.uint8(out))
                    outImg.save(view_path)
        del target_ds
        del out
        return view_path


if __name__ == "__main__":
    # 进程调用模式
    out_list = []
    out_list.append(r'D:\test\view\F47E001007BJ210M2017A_browse.png')
    out_list.append(r'D:\test\view\F47E001007BJ210M2017A_thumb.jpg')
    out_list.append(r'D:\test\view\F47E001007BJ210M2017A_browse.tiff')
    view_creator = CViewCreatorRaster(r'D:\test\云南高分影像\F47\F47E001007BJ210M2017A.TIF')
    result = CProcessUtils.processing_method(view_creator.process(), out_list)
