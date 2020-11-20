# -*- coding: utf-8 -*- 
# @Time : 2020/10/26 13:30
# @Author : 赵宇飞
# @File : c_gdalUtils.py
from osgeo import gdal, ogr

from imetadata.base.c_file import CFile
from imetadata.base.c_processUtils import CProcessUtils
# import numpy
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils


class CGdalUtils(CResource):
    @classmethod
    def is_vector_file_can_read(cls, vector_file_with_path: str) -> bool:
        """
        完成 张源博 判断矢量文件的可读性，采用进程读取
        @param vector_file_with_path:
        @return:
        """
        vector_ds = ogr.Open(vector_file_with_path)
        if vector_ds is not None:
            return True
        return False

    @classmethod
    def is_vector_file_can_read_process(cls, vector_file_with_path: str) -> bool:
        """
        进程方式调用方法
        @param vector_file_with_path:
        @return:
        """
        return CProcessUtils.processing_method(CGdalUtils.is_vector_file_can_read, vector_file_with_path)

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
    def is_vector_dataset_can_read_process(cls, vector_dataset_with_path: str) -> bool:
        """
        进程方式调用方法
        @param vector_dataset_with_path:
        @return:
        """
        return CProcessUtils.processing_method(CGdalUtils.is_vector_dataset_can_read, vector_dataset_with_path)

    @classmethod
    def is_raster_file_can_read(cls, raster_file_with_path: str) -> bool:
        """
        完成 张源博 判断影像文件的可读性,除了能正常打开外，还需要获取块的大小，并且读取第1个块和最后一个块有值，才能确定影像正常可以读取
          采用进程读取
        @param raster_file_with_path:
        @return:
        """
        sample_width = 6
        sample_height = 3
        try:
            if not cls.is_raster_file_integrity(raster_file_with_path):
                return False
            raster_ds = gdal.Open(raster_file_with_path, gdal.GA_ReadOnly)
            if raster_ds is None:
                return False
            elif not CUtils.equal_ignore_case(CSys.get_os_name(), cls.OS_MacOS):
                """测试需要numpy的包，同时需要检验gdal安装环境的正确性, 没有安装则会band.ReadAsArray读取异常"""
                band_count = raster_ds.RasterCount
                if band_count > 0:
                    band = raster_ds.GetRasterBand(band_count)
                    data1 = band.ReadAsArray(xoff=1, yoff=1, win_xsize=sample_width, win_ysize=sample_height)
                    image_size_x = raster_ds.RasterXSize
                    image_size_y = raster_ds.RasterYSize
                    block_size_x = image_size_x - sample_width
                    block_size_y = image_size_y - sample_height
                    data2 = band.ReadAsArray(xoff=block_size_x, yoff=block_size_y, win_xsize=sample_width, win_ysize=sample_height)
                    band = None
                    raster_ds = None
                    if data1 is not None and data2 is not None:
                        return True
                    else:
                        return False
            else:
                return True
        except Exception as error:
            print(error.__str__())
            return False

    @classmethod
    def is_raster_file_can_read_process(cls, raster_file_with_path: str) -> bool:
        """
        进程方式调用方法
        @param raster_file_with_path:
        @return:
        """
        return CProcessUtils.processing_method(CGdalUtils.is_raster_file_can_read, raster_file_with_path)

    @classmethod
    def is_raster_file_integrity(cls, raster_file_with_path: str) -> bool:
        """
        判断影像数据的文件完整性，img
            xxx.img	文件	栅格数据可读	错误
            xxx.ige	文件	img小于1M时必须存在	警告
        @param raster_file_with_path:
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


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    file_src = r'/Users/wangxiya/Documents/我的测试数据/11.入库存储/湖南标准分幅成果数据/G49G001030/G49G001030.tif'
    print(CGdalUtils.is_raster_file_can_read(file_src))
