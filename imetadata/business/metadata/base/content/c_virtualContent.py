# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:57 
# @Author : 王西亚 
# @File : c_virtualContent.py

from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils


class CVirtualContent(CResource):
    __temp_subpath_name__: str
    __target_name__ = None
    __virtual_content_root_dir__ = None
    __work_root_dir__ = None

    """
    虚拟内容目录
    . 在读取普通文件数据时, 虚拟内容目录是文件所在的子目录
    . 在读取普通子目录数据时, 虚拟内容目录是子目录本身
    . 在读取压缩数据时, 虚拟目录时压缩包解压的临时子目录
    """

    def __init__(self, target_name):
        self.__target_name__ = target_name
        self.__temp_subpath_name__ = CUtils.one_id()
        self.__work_root_dir__ = CFile.join_file(CSys.get_work_root_dir(), self.__temp_subpath_name__)

    @abstractmethod
    def create_virtual_content(self) -> bool:
        CFile.check_and_create_directory_itself(self.__work_root_dir__)
        return CFile.file_or_path_exist(self.__work_root_dir__)

    def virtual_content_valid(self) -> bool:
        return CFile.file_or_path_exist(self.__virtual_content_root_dir__)

    def destroy_virtual_content(self):
        CFile.remove_dir(self.__work_root_dir__)

    @property
    def content_root_dir(self):
        return self.__virtual_content_root_dir__

    @property
    def work_root_dir(self):
        return self.__work_root_dir__
