# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 09:02 
# @Author : 王西亚 
# @File : c_rasterMDReader.py
from imetadata.tool.mdreader.c_mdreader import CMDReader


class CRasterMDReader(CMDReader):
    """
    栅格数据文件的元数据读取器
    """

    def get_metadata_2_file(self, file_name_with_path: str):
        print('你的任务: 将文件{0}的元数据信息, 提取出来, 存储到文件{1}中'.format(self.__file_name_with_path__, file_name_with_path))
        pass


if __name__ == '__main__':
    CRasterMDReader('/aa/bb/cc.img').get_metadata_2_file('/aa/bb/cc.json')
