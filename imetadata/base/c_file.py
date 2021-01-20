#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import os
import shutil
import time
from fnmatch import fnmatch
from typing import AnyStr

import chardet
from sortedcontainers import SortedList

from imetadata.base.c_utils import CUtils
from imetadata.base.c_exceptions import PathNotCreateException


class CFile:
    unify_seperator = '/'
    MatchType_Common = 1
    MatchType_Regex = 2

    __special_file_ext_list = ['tar.gz']

    def __init__(self):
        pass

    @classmethod
    def file_ext(cls, file_name_with_path: str) -> str:
        file_name_tmp = CFile.file_name(file_name_with_path)
        file_main_name = CFile.file_main_name(file_name_with_path)
        file_ext = file_name_tmp.replace('{0}.'.format(file_main_name), '', 1)
        return file_ext

    @classmethod
    def sep(cls):
        return cls.unify_seperator

    @classmethod
    def file_name(cls, file_name_with_path: str) -> str:
        return os.path.basename(file_name_with_path)

    @classmethod
    def file_path(cls, file_name_with_path: str) -> str:
        (input_file_path, input_file_main_name) = os.path.split(file_name_with_path)
        return input_file_path

    @classmethod
    def file_abs_path(cls, file_name_with_path: str) -> str:
        return os.path.abspath(file_name_with_path)

    @classmethod
    def file_main_name(cls, file_name_with_path: str):
        filename_without_path = cls.file_name(file_name_with_path)

        for ext_white in cls.__special_file_ext_list:
            if filename_without_path.lower().endswith(ext_white.lower()):
                return filename_without_path[:len(filename_without_path) - len(ext_white) - 1]
        else:
            file_info = os.path.splitext(filename_without_path)
            return file_info[0]

    @classmethod
    def change_file_ext(cls, file_name_with_path: str, file_ext: str):
        """
        改变文件的扩展名, 注意, 新扩展名不带前导点
        :param file_name_with_path:
        :param file_ext:
        :return:
        """
        file_path = cls.file_path(file_name_with_path)
        file_main_name = '{0}.{1}'.format(cls.file_main_name(file_name_with_path), file_ext)
        if CUtils.equal_ignore_case(file_path, ''):
            return file_main_name
        else:
            return cls.join_file(file_path, file_main_name)

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
        """
        获取指定目录下的一级文件和子目录
        1. 可以支持常规检索和正则表达式检索
        1. 返回当前目录下的文件和子目录(不包含路径!!!)
        :param path:
        :param match_str:
        :param match_type:
        :return:
        """
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
    def find_file_or_subpath_of_path(cls, path: str, match_str: str, match_type: int = MatchType_Common) -> bool:
        list_files = cls.file_or_subpath_of_path(path, match_str, match_type)
        return len(list_files) > 0

    @classmethod
    def join_file(cls, path: str, *paths: AnyStr) -> str:
        result = CUtils.any_2_str(path)
        for each_path in paths:
            real_file_name = CUtils.any_2_str(each_path)
            if real_file_name.startswith(r'/') or real_file_name.startswith('\\'):
                real_file_name = real_file_name[1:len(real_file_name)]
            result = '{0}{1}{2}'.format(result, cls.sep(), real_file_name)
        return result

    @classmethod
    def add_prefix(cls, path: str) -> str:
        real_path = CUtils.any_2_str(path)
        if real_path.startswith(r'/') or real_path.startswith('\\'):
            return real_path
        else:
            return '{0}{1}'.format(cls.sep(), real_path)

    @classmethod
    def unify(cls, file_or_path: str) -> str:
        result = file_or_path
        result = result.replace('\\', cls.sep())
        return result

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
    def file_match_list(cls, file_name_with_path: str, pattern_list):
        for pattern in pattern_list:
            if fnmatch(file_name_with_path, pattern):
                return True

        return False

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
        完成 王学谦 编码格式识别
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
    def str_2_file(cls, str_info: str, file_name_with_path: str, encoding_type='utf-8'):
        if not CFile.check_and_create_directory(file_name_with_path):
            raise PathNotCreateException(file_name_with_path)

        if CUtils.equal_ignore_case(str_info, "") \
                or CUtils.equal_ignore_case(file_name_with_path, ""):
            return
        try:
            if CFile.check_and_create_directory(file_name_with_path):
                with open(file_name_with_path, "w", encoding=encoding_type) as f:
                    f.write(str_info)
        except Exception as error:
            print(error.__str__())

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
            match_type: int = MatchType_Common, is_recurse_subpath_all_file: bool = False):
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
                    cls.__file_or_dir_fullname_of_path_recurse(
                        result_file_fullname_list, file_fullname_temp, is_recurse_subpath, match_str, match_type
                    )

        if is_recurse_subpath_all_file and (not is_recurse_subpath):
            list_all_file_name = cls.file_or_subpath_of_path(path)
            for all_file_name_temp in list_all_file_name:
                all_file_fullname_temp = cls.join_file(path, all_file_name_temp)
                if cls.is_dir(all_file_fullname_temp):
                    cls.__file_or_dir_fullname_of_path_recurse(
                        result_file_fullname_list, all_file_fullname_temp,
                        is_recurse_subpath, match_str, match_type, is_recurse_subpath_all_file
                    )

    @classmethod
    def file_or_dir_fullname_of_path(cls, path: str, is_recurse_subpath: bool = False, match_str: str = '*',
                                     match_type: int = MatchType_Common, is_recurse_subpath_all_file: bool = False):
        """
        公共方法：根据路径获取文件和文件夹的全文件名，根据参数is_recurse_subpath支持是否递归子目录
        @param path: 扫描的目录
        @param is_recurse_subpath: 是否递归子目录
        @param match_str:
        @param match_type:
        @param is_recurse_subpath_all_file:
        @return:
        """
        list_file_fullname = []
        if cls.is_dir(path):
            cls.__file_or_dir_fullname_of_path_recurse(
                list_file_fullname, path, is_recurse_subpath, match_str, match_type, is_recurse_subpath_all_file
            )
        return list_file_fullname

    @classmethod
    def __stat_of_path(
            cls,
            path: str,
            is_recurse_subpath: bool,
            match_str: str,
            match_type: int,
            sub_dir_count: int,
            file_count: int,
            file_size_sum: int
    ):
        """
        公共方法：根据路径获取路径下的统计信息，根据参数is_recurse_subpath支持是否递归子目录
        @param path: 扫描的目录
        @param is_recurse_subpath: 是否递归子目录
        @param match_str:
        @param match_type:
        @return:
        统计信息包括:
        1. 子目录个数
        2. 文件个数
        3. 文件总大小
        """
        result_sub_dir_count = sub_dir_count
        result_file_count = file_count
        result_file_size_sum = file_size_sum
        list_file_name = cls.file_or_subpath_of_path(path, match_str, match_type)
        for file_name_temp in list_file_name:
            file_fullname_temp = cls.join_file(path, file_name_temp)
            if cls.is_file(file_fullname_temp):
                result_file_count = result_file_count + 1
                result_file_size_sum = result_file_size_sum + cls.file_size(file_fullname_temp)
            else:
                result_sub_dir_count = result_sub_dir_count + 1
                if is_recurse_subpath:
                    result_sub_dir_count, result_file_count, result_file_size_sum = cls.__stat_of_path(
                        file_fullname_temp,
                        is_recurse_subpath,
                        match_str,
                        match_type,
                        result_sub_dir_count,
                        result_file_count,
                        result_file_size_sum
                    )
        return result_sub_dir_count, result_file_count, result_file_size_sum

    @classmethod
    def stat_of_path(cls, path: str, is_recurse_subpath: bool = False, match_str: str = '*',
                     match_type: int = MatchType_Common):
        """
        公共方法：根据路径获取路径下的统计信息，根据参数is_recurse_subpath支持是否递归子目录

        @param path: 扫描的目录
        @param is_recurse_subpath: 是否递归子目录
        @param match_str:
        @param match_type:
        @return:
        统计信息包括:
        1. 子目录个数
        2. 文件个数
        3. 文件总大小
        """

        if cls.is_dir(path):
            return cls.__stat_of_path(path, is_recurse_subpath, match_str, match_type, 0, 0, 0)
        else:
            return 0, 1, cls.file_size(path)

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
                    src_file = cls.join_file(root, file)
                    shutil.copy(src_file, target_path)

    @classmethod
    def move_file_to(cls, file_name_with_path: str, target_path: str, new_file_name=None) -> bool:
        if not cls.file_or_path_exist(target_path):
            if not cls.check_and_create_directory_itself(target_path):
                return False

        target_file_name = new_file_name
        if target_file_name is None:
            target_file_name = cls.file_name(file_name_with_path)

        target_file_with_path = cls.join_file(target_path, target_file_name)

        if cls.file_or_path_exist(file_name_with_path):
            try:
                shutil.move(file_name_with_path, target_file_with_path)

                return cls.file_or_path_exist(target_file_with_path)
            except:
                return False

    @classmethod
    def move_path_to(cls, file_path: str, target_path: str):
        """
        移动源目录至目标目录
        注意: 是将源目录下的所有内容, 直接移动至目标目录下; 而不是将源目录作为子目录, 移动至目标目录下!!!
        返回值:
        1. 是否完全正常移动: True/False
        2. 如果是错误, 则返回错误的文件列表, 是一个list
        :param file_path:
        :param target_path:
        :return:
        """
        # 计算源目录的名称
        file_path_name = cls.file_name(file_path)
        target_path_full_name = cls.join_file(target_path, file_path_name)
        result, failure_list = cls.move_subpath_and_file_of_path_to(file_path, target_path_full_name)

        if len(failure_list) == 0:
            shutil.rmtree(file_path)

        return result, failure_list

    @classmethod
    def move_subpath_and_file_of_path_to(cls, file_path: str, target_path: str):
        """
        移动源目录下的子目录和文件, 至目标目录
        :param file_path:
        :param target_path:
        :return:
        """
        failure_list = []

        if not cls.file_or_path_exist(target_path):
            if not cls.check_and_create_directory_itself(target_path):
                return False, failure_list

        for parent_path, sub_paths, sub_files in os.walk(file_path):
            relation_path = cls.file_relation_path(parent_path, file_path)
            for sub_file in sub_files:
                src_file = cls.join_file(parent_path, sub_file)
                if not cls.move_file_to(src_file, cls.join_file(target_path, relation_path)):
                    failure_list.append(cls.join_file(relation_path, sub_file))

        if len(failure_list) == 0:
            sub_path_list = cls.file_or_subpath_of_path(file_path)
            for sub_path in sub_path_list:
                sub_path_full_name = cls.join_file(file_path, sub_path)
                if cls.is_dir(sub_path_full_name):
                    shutil.rmtree(sub_path_full_name)

        return len(failure_list) == 0, failure_list

    @classmethod
    def file_locked(cls, file_name_with_path) -> bool:
        """
        检查文件是否被其他应用打开和锁定
        todo(全体) 这里放在最后实现, 目前暂时不判定文件是否被锁定, 而且一定要在windows和linux操作系统中调试
        :param file_name_with_path:
        :return:
        """
        return False

    @classmethod
    def find_locked_file_in_path(cls, file_path) -> list:
        """
        检查文件是否被其他应用打开和锁定
        :param file_path:
        :return:
        """
        locked_file_list = []

        for parent_path, sub_paths, sub_files in os.walk(file_path):
            relation_path = cls.file_relation_path(parent_path, file_path)
            for sub_file in sub_files:
                src_file = cls.join_file(parent_path, sub_file)
                if cls.file_locked(src_file):
                    locked_file_list.append(cls.join_file(relation_path, sub_file))

        return locked_file_list


if __name__ == '__main__':
    # print(CFile.join_file('', 'aa/bb/', '中国'))
    # print(os.path.normpath('c:\\a/bb\\c/dd'))
    # print(CFile.join_file('/aa/bb/', '/cc'))
    # print(CFile.join_file('/aa/bb', 'cc'))
    # print(CFile.join_file('/aa/bb/', ''))
    # print(CFile.join_file('/aa/bb/', '/'))
    # print(CFile.join_file('/aa/bb', ''))

    CFile.move_path_to('/Users/wangxiya/Downloads/axios1', '/Users/wangxiya/Downloads/axios/aa/bb')
    # CFile.move_subpath_and_file_of_path_to('/Users/wangxiya/Downloads/axios1', '/Users/wangxiya/Downloads/axios/aa/bb')
    # shutil.move('/Users/wangxiya/Downloads/axios1', '/Users/wangxiya/Downloads/axios')
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
    # CFile.str_2_file('1111我们', r'D:\data\wkt\11.wkt')
