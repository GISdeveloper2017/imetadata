# -*- coding: utf-8 -*- 
# @Time : 2020/10/26 13:30
# @Author : 赵宇飞
# @File : c_gdalUtils.py

from osgeo import gdal, ogr

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
        raster_ds = gdal.Open(raster_file_with_path, gdal.GA_ReadOnly)
        if raster_ds is None:
            return False
        else:
            """
              在这里获取块的大小，并且读取第1个块和最后一个块有值，才能确定影像正常可以读取
            """
            pass
        return True