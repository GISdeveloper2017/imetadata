# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:57 
# @Author : 王西亚 
# @File : c_virtualContent.py
from abc import abstractmethod


class CVirtualContent:
    __target_name__ = None

    """
    虚拟内容目录
    . 在读取普通文件数据时, 虚拟内容目录是文件所在的子目录
    . 在读取普通子目录数据时, 虚拟内容目录是子目录本身
    . 在读取压缩数据时, 虚拟目录时压缩包解压的临时子目录
    """

    def __init__(self, target_name):
        self.__target_name__ = target_name

    @abstractmethod
    def create_virtual_content(self) -> str:
        pass

    def destroy_virtual_content(self):
        pass