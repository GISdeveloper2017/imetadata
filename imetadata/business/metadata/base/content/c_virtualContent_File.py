# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 18:03 
# @Author : 王西亚 
# @File : c_virtualContent_File.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent


class CVirtualContentFile(CVirtualContent):
    """
    虚拟内容目录
    . 在读取普通文件数据时, 虚拟内容目录是文件所在的子目录
    . 在读取普通子目录数据时, 虚拟内容目录是子目录本身
    . 在读取压缩数据时, 虚拟目录时压缩包解压的临时子目录
    """

    def __init__(self, target_name):
        super().__init__(target_name)
        self.__virtual_content_root_dir__ = CFile.file_path(self.__target_name__)

    def create_virtual_content(self) -> bool:
        return super().create_virtual_content() and CFile.file_or_path_exist(self.__virtual_content_root_dir__)
