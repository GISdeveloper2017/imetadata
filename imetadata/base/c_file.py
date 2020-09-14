#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import
import os
import time
import glob
from fnmatch import fnmatch, fnmatchcase


class CFile:
    def __init__(self):
        pass

    @classmethod
    def file_name(cls, file_name_with_path: str) -> str:
        return os.path.basename(file_name_with_path)

    @classmethod
    def file_path(cls, file_name_with_path: str) -> str:
        (input_file_path, input_file_main_name) = os.path.split(file_name_with_path)
        return input_file_path

    @classmethod
    def file_main_name(cls, file_name_with_path: str, file_ext_whitelist: str = '',
                       file_ext_whitelist_seperator: str = ';'):
        filename_without_path = cls.file_name(file_name_with_path)

        if (file_ext_whitelist is None) or (file_ext_whitelist == ''):
            file_info = os.path.splitext(filename_without_path)
            return file_info[0]
        else:
            ext_white_list = file_ext_whitelist.split(file_ext_whitelist_seperator)
            for ext_white in ext_white_list:
                if filename_without_path.lower().endswith(ext_white.lower()):
                    return filename_without_path[:len(filename_without_path) - len(ext_white) - 1]

    @classmethod
    def check_and_create_directory(cls, file_name_with_path: str) -> bool:
        return cls.check_and_create_dir(cls.file_path(file_name_with_path))

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
    def file_or_subpath_of_path(cls, path: str) -> list:
        return os.listdir(path)

    @classmethod
    def search_file_or_subpath_of_path(cls, path: str, match_str: str, recursive: bool) -> list:
        return glob.glob(cls.join_file(path, match_str), recursive)

    @classmethod
    def join_file(cls, path, file_name: str) -> str:
        return os.path.join(path, file_name)

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


if __name__ == '__main__':
    print('文件:{0}'.format(CFile.join_file(r'/Users/Clare', '')))

    # print(CFile.file_main_name(r'/Users/Clare/gf1.tar.gz', 'tar.gz'))
    # print(CFile.file_relation_path(r'/Users/Users/Clare/gf1.tar.gz', '/Users'))
    # file_name = '/Users/wangxiya/Documents/我的文稿/私人/我的/重要/ADSL.docx'
    # print('文件:{0}'.format(file_name))
    # print('是否存在:{0}'.format(CFile.file_or_path_exist(file_name)))
    # print('是否是目录:{0}'.format(CFile.is_dir(file_name)))
    # print('是否是文件:{0}'.format(CFile.is_file(file_name)))
    # if CFile.file_or_path_exist(file_name):
    #     print('修改时间:{0}'.format(CFile.file_modify_time(file_name)))
    #     print('大小:{0}'.format(CFile.file_size(file_name)))

    # for file_or_path in CFile.file_of_path('/Users/wangxiya/Documents/交换/1.给我的/get_luotu'):
    #     print(file_or_path)
