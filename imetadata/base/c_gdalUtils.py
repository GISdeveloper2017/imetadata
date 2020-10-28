# -*- coding: utf-8 -*- 
# @Time : 2020/10/26 13:30
# @Author : 赵宇飞
# @File : c_gdalUtils.py

from osgeo import gdal, ogr

from imetadata.base.c_file import CFile


class CGdalUtils:
    @classmethod
    def is_vector_file_can_read(cls, vector_file_with_path: str) -> bool:
        """
        todo 张源博 判断矢量文件的可读性，采用进程读取
        @param vector_file_with_path:
        @return:
        """
        vector_ds = ogr.Open(vector_file_with_path)
        if vector_ds is not None:
            return True
        return False

    @classmethod
    def is_vector_dataset_can_read(cls, vector_dataset_with_path: str) -> bool:
        """
        todo 判断矢量数据集的可读性（mdb中的矢量图层，gdb中的矢量图层），注意函数的参数可能不够，先预留
              采用进程读取
        @param vector_dataset_with_path:
        @return:
        """
        return False

    @classmethod
    def is_raster_file_can_read(cls, raster_file_with_path: str) -> bool:
        """
        todo 张源博 判断影像文件的可读性,除了能正常打开外，还需要获取块的大小，并且读取第1个块和最后一个块有值，才能确定影像正常可以读取
          采用进程读取
        @param raster_file_with_path:
        @return:
        """
        if not cls.is_raster_file_integrity(raster_file_with_path):
            return False
        raster_ds = gdal.Open(raster_file_with_path, gdal.GA_ReadOnly)
        if raster_ds is None:
            return False
        else:
            band_count = raster_ds.RasterCount
            if band_count > 0:
                band = raster_ds.GetRasterBand(band_count)
                data1 = band.ReadAsArray(xoff=0, yoff=0, win_xsize=6, win_ysize=3)
                image_size_x = raster_ds.RasterXSize
                image_size_y = raster_ds.RasterYSize
                block_size_x = image_size_x - 6
                block_size_y = image_size_y - 3
                data2 = band.ReadAsArray(xoff=block_size_x, yoff=block_size_y, win_xsize=6, win_ysize=3)
                band = None
                raster_ds = None
                if data1 is not None and data2 is not None:
                    return True
                else:
                    return False
        return False

    def is_raster_file_integrity(self, raster_file_with_path: str) -> bool:
        """
        判断影像数据的文件完整性，img
            xxx.img	文件	栅格数据可读	错误
            xxx.ige	文件	img小于1M时必须存在	警告
        @param img_file_with_path:
        @return:
        """
        file_ext = CFile.file_ext(raster_file_with_path)
        if file_ext.lower() == 'img':
            size = CFile.file_size(raster_file_with_path)
            if size < 1024 * 1024:
                file_main_name = CFile.file_main_name(raster_file_with_path)
                file_path = CFile.file_path(raster_file_with_path)
                ige = CFile.join_file(file_path, file_main_name + '.ige')
                if not CFile.file_or_path_exist(ige):
                    return False
        return True