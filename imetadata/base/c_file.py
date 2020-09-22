#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import

import glob
import os
import time
from fnmatch import fnmatch

from sortedcontainers import SortedList


class CFile:
    __special_file_ext_list__ = ['tar.gz']

    def __init__(self):
        pass

    @classmethod
    def file_ext(cls, file_name_with_path: str) -> str:
        file_name_tmp = CFile.file_name(file_name_with_path)
        file_main_name = CFile.file_main_name(file_name_with_path)
        file_ext = file_name_tmp.replace('{0}.'.format(file_main_name), '', 1)
        return file_ext

    @classmethod
    def file_name(cls, file_name_with_path: str) -> str:
        return os.path.basename(file_name_with_path)

    @classmethod
    def file_path(cls, file_name_with_path: str) -> str:
        (input_file_path, input_file_main_name) = os.path.split(file_name_with_path)
        return input_file_path

    @classmethod
    def file_main_name(cls, file_name_with_path: str):
        filename_without_path = cls.file_name(file_name_with_path)

        for ext_white in cls.__special_file_ext_list__:
            if filename_without_path.lower().endswith(ext_white.lower()):
                return filename_without_path[:len(filename_without_path) - len(ext_white) - 1]
        else:
            file_info = os.path.splitext(filename_without_path)
            return file_info[0]

    @classmethod
    def check_and_create_directory(cls, file_name_with_path: str) -> bool:
        return cls.check_and_create_directory_itself(cls.file_path(file_name_with_path))

    @classmethod
    def check_and_create_directory_itself(cls, file_path: str) -> bool:
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            return True
        except OSError as error:
            return False

    @classmethod
    def file_relation_path(cls, file_name_with_path: str, file_root_path: str) -> str:
        if file_name_with_path.startswith(file_root_path):
            return file_name_with_path.replace(file_root_path, '', 1)
        else:
            return file_name_with_path

    @classmethod
    def file_or_subpath_of_path(cls, path: str) -> SortedList:
        return SortedList(os.listdir(path))

    @classmethod
    def search_file_or_subpath_of_path(cls, path: str, match_str: str) -> SortedList:
        return SortedList(glob.glob(cls.join_file(path, match_str)))

    @classmethod
    def find_file_or_subpath_of_path(cls, path: str, match_str: str) -> bool:
        list_files = cls.search_file_or_subpath_of_path(path, match_str)
        return len(list_files) > 0

    @classmethod
    def join_file(cls, path, file_name: str) -> str:
        real_file_name = file_name
        if file_name.startswith(r'/') or file_name.startswith('\\'):
            real_file_name = real_file_name[1:len(real_file_name)]
        return os.path.join(path, real_file_name)

    @classmethod
    def remove_file(cls, file_name_with_path: str):
        os.remove(file_name_with_path)

    @classmethod
    def remove_dir(cls, file_path: str):
        os.removedirs(file_path)

    @classmethod
    def rename_file_or_dir(cls, old_file_name_with_path: str, new_file_name_with_path: str):
        os.renames(old_file_name_with_path, new_file_name_with_path)

    @classmethod
    def file_time_format(cls, time_value: float, time_format_str: str = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(time_format_str, time.localtime(time_value))

    @classmethod
    def file_modify_time(cls, file_name_with_path: str, time_format_str: str = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(time_format_str, time.localtime(os.path.getmtime(file_name_with_path)))

    @classmethod
    def file_create_time(cls, file_name_with_path: str, time_format_str: str = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(time_format_str, time.localtime(os.path.getctime(file_name_with_path)))

    @classmethod
    def file_access_time(cls, file_name_with_path: str, time_format_str: str = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(time_format_str, time.localtime(os.path.getatime(file_name_with_path)))

    @classmethod
    def file_size(cls, file_name_with_path: str):
        return os.path.getsize(file_name_with_path)

    @classmethod
    def is_file(cls, file_name_with_path: str):
        return os.path.isfile(file_name_with_path)

    @classmethod
    def is_dir(cls, file_name_with_path: str):
        return os.path.isdir(file_name_with_path)

    @classmethod
    def file_or_path_exist(cls, dir_name_with_path: str):
        return os.path.exists(dir_name_with_path)

    @classmethod
    def file_match(cls, file_name_with_path: str, pattern: str):
        return fnmatch(file_name_with_path, pattern)

    @classmethod
    def subpath_in_path(cls, sub_path:str, filepath: str):
        subpath_list = []
        file_path_str = filepath.replace("\\", "/")
        file_path_str, file_name_str = os.path.split(file_path_str)
        subpath_list.append(file_name_str.lower())
        while file_name_str != '':
            file_path_str, file_name_str = os.path.split(file_path_str)
            if file_name_str != '':
                subpath_list.append(file_name_str.lower())

        return subpath_list.count(sub_path.lower()) > 0


if __name__ == '__main__':
    pass
    # print(CFile.file_main_name(r'/Users/Clare/gf1.tar.gz'))
    # print(CFile.file_ext(r'/Users/Clare/gf1.tar.gz'))
    # print(CFile.file_main_name(r'/Users/Clare/gf1.xls'))
    # print(CFile.file_ext(r'/Users/Clare/gf1.xls'))
    # print(CFile.file_relation_path(r'/Users/Users/Clare/gf1.tar.gz', '/Users'))
    # file_name = '/Users/wangxiya/Documents/交换'
    # print('文件:{0}'.format(file_name))
    # print('是否存在:{0}'.format(CFile.file_or_path_exist(file_name)))
    # print('是否是目录:{0}'.format(CFile.is_dir(file_name)))
    # print('是否是文件:{0}'.format(CFile.is_file(file_name)))
    # if CFile.file_or_path_exist(file_name):
    #     print('修改时间:{0}'.format(CFile.file_modify_time(file_name)))
    #     print('大小:{0}'.format(CFile.file_size(file_name)))

    # for file_or_path in CFile.file_of_path('/Users/wangxiya/Documents/交换/1.给我的/get_luotu'):
    #     print(file_or_path)
    # subpath_list = []
    # file_path = '/Users/wangxiya/Documents/交换/1.给我的/get_luotu'
    # file_path1 = r'C:\Users\wangxiya\Documents\交换\1.给我的\get_luotu'
    # file_path = file_path.replace("\\", "/")
    # file_path, file_name = os.path.split(file_path)
    # subpath_list.append(file_name.lower())
    # while file_name != '':
    #     file_path, file_name = os.path.split(file_path)
    #     if file_name != '':
    #         subpath_list.append(file_name.lower())
    # print('*'*20)
    # for subpath in subpath_list:
    #     print('1.{0}'.format(subpath))
    #
    # print('*'*20)
    # if CFile.subpath_in_path('documents', file_path):
    #     print('in')
    # else:
    #     print('not in')
