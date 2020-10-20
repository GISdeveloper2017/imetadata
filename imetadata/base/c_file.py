#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import os
import shutil
import time
import chardet
from fnmatch import fnmatch

from sortedcontainers import SortedList

from imetadata.base.c_utils import CUtils


class CFile:
    MatchType_Common = 1
    MatchType_Regex = 2

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
            return cls.file_or_path_exist(file_path)
        except OSError as error:
            return False

    @classmethod
    def file_relation_path(cls, file_name_with_path: str, file_root_path: str) -> str:
        if file_name_with_path.startswith(file_root_path):
            return file_name_with_path.replace(file_root_path, '', 1)
        else:
            return file_name_with_path

    @classmethod
    def file_or_subpath_of_path(cls, path: str, match_str: str = '*', match_type: int = MatchType_Common) -> SortedList:
        list_all_file = os.listdir(path)
        if match_str == '*':
            return SortedList(list_all_file)

        list_match_file = []
        for item_file_name in list_all_file:
            if cls.MatchType_Common == match_type:
                if cls.file_match(item_file_name, match_str):
                    list_match_file.append(item_file_name)
            else:
                if CUtils.text_match_re(item_file_name, match_str):
                    list_match_file.append(item_file_name)

        return SortedList(list_match_file)

    @classmethod
    def find_file_or_subpath_of_path(cls, path: str, match_str: str) -> bool:
        list_files = cls.file_or_subpath_of_path(path, match_str)
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
        if cls.file_or_path_exist(file_path):
            # os.removedirs(file_path)
            shutil.rmtree(file_path)

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
        if dir_name_with_path is None:
            return False
        return os.path.exists(dir_name_with_path)

    @classmethod
    def file_match(cls, file_name_with_path: str, pattern: str):
        return fnmatch(file_name_with_path, pattern)

    @classmethod
    def subpath_in_path(cls, sub_path: str, filepath: str):
        subpath_list = []
        file_path_str = filepath.replace("\\", "/")
        file_path_str, file_name_str = os.path.split(file_path_str)
        subpath_list.append(file_name_str.lower())
        while file_name_str != '':
            file_path_str, file_name_str = os.path.split(file_path_str)
            if file_name_str != '':
                subpath_list.append(file_name_str.lower())

        return subpath_list.count(sub_path.lower()) > 0

    @classmethod
    def identify_encoding(cls, text):
        """
        TODO 王学谦 编码格式识别
        :param text:需要转换的文本
        :return true_text:转换后的编码格式
        """
        identify_result = chardet.detect(text)
        identify_encoding = identify_result['encoding']
        # identify_probability = identify_result['confidence'] # 成功概率
        # 由于windows系统的编码有可能是Windows-1254,打印出来后还是乱码,所以不直接用UTF-8编码
        if CUtils.equal_ignore_case(identify_encoding, 'Windows-1254'):
            identify_encoding = 'UTF-8'
        return identify_encoding

    @classmethod
    def file_2_str(cls, file_name_with_path: str):
        if not cls.file_or_path_exist(file_name_with_path):
            return ''

        f = open(file_name_with_path, "rb")
        try:
            txt = f.read()
            encoding = cls.identify_encoding(txt[:1000])
            true_txt = txt.decode(encoding, "ignore")
            return true_txt
        finally:
            f.close()

    @classmethod
    def file_2_list(cls, file_name_with_path: str):
        if not cls.file_or_path_exist(file_name_with_path):
            return ''

        f = open(file_name_with_path, "rb")
        try:
            txt_tem = f.read(1000)
            encoding = CFile.identify_encoding(txt_tem)
            f.seek(0)
            txt_list = f.readlines()
            for index, txt in enumerate(txt_list):
                txt = txt.decode(encoding, "ignore")
                txt_list[index] = txt
            return txt_list
        finally:
            f.close()

    @classmethod
    def __file_or_dir_fullname_of_path_recurse(
            cls, result_file_fullname_list: [], path: str,
            is_recurse_subpath: bool = False, match_str: str = '*',
            match_type: int = MatchType_Common):
        """
            私有方法，递归路径获取路径下的所有文件和文件夹的全文件名，仅供内部函数file_or_dir_fullname_of_path调用
        @param result_file_fullname_list:
        @param path:
        @param is_recurse_subpath:
        @param match_str:
        @param match_type:
        @return:
        """
        list_file_name = cls.file_or_subpath_of_path(path, match_str, match_type)
        for file_name_temp in list_file_name:
            file_fullname_temp = cls.join_file(path, file_name_temp)
            result_file_fullname_list.append(file_fullname_temp)
            if is_recurse_subpath:
                if cls.is_dir(file_fullname_temp):
                    cls.__file_or_dir_fullname_of_path_recurse(result_file_fullname_list, file_fullname_temp,
                                                               is_recurse_subpath, match_str, match_type)

    @classmethod
    def file_or_dir_fullname_of_path(cls, path: str, is_recurse_subpath: bool = False, match_str: str = '*',
                                     match_type: int = MatchType_Common):
        """
            公共方法：根据路径获取文件和文件夹的全文件名，根据参数is_recurse_subpath支持是否递归子目录
        @param path: 扫描的目录
        @param is_recurse_subpath: 是否递归子目录
        @param match_str:
        @param match_type:
        @return:
        """
        list_file_fullname = []
        if cls.is_dir(path):
            cls.__file_or_dir_fullname_of_path_recurse(list_file_fullname, path, is_recurse_subpath, match_str,
                                                       match_type)
        return list_file_fullname

    @classmethod
    def copy_file_to(cls, file_name_with_path: str, target_path: str):
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        if cls.file_or_path_exist(file_name_with_path):
            shutil.copy(file_name_with_path, target_path)

    @classmethod
    def copy_path_to(cls, source_path: str, target_path: str):
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        if cls.file_or_path_exist(source_path):
            # root 所指的是当前正在遍历的这个文件夹的本身的地址
            # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
            # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    shutil.copy(src_file, target_path)


if __name__ == '__main__':
    pass
    # for file_or_path in CFile.file_or_subpath_of_path('/Users/wangxiya/Documents/交换'):
    #     print(file_or_path)
    # print('*'*10)
    # for file_or_path in CFile.search_file_or_subpath_of_path('/Users/wangxiya/Documents/交换', '*'):
    #     print(file_or_path)
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
