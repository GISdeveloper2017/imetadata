# -*- coding: utf-8 -*- 
# @Time : 2020/9/18 09:56 
# @Author : 王西亚 
# @File : c_vectorMDReader.py

from imetadata.tool.mdreader.c_mdreader import CMDReader


class CVectorMDReader(CMDReader):
    """
    矢量数据文件的元数据读取器
    """

    def get_metadata_2_file(self, file_name_with_path: str):
        print('你的任务: 将文件{0}的元数据信息, 提取出来, 存储到文件{1}中'.format(self.__file_name_with_path__, file_name_with_path))
        pass


if __name__ == '__main__':
    CVectorMDReader('/aa/bb/cc1.shp').get_metadata_2_file('/aa/bb/cc1.json')
    CVectorMDReader('/aa/bb/cc2.gdb').get_metadata_2_file('/aa/bb/cc2.json')
