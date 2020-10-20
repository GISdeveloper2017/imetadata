#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
import re
import uuid
import pinyin
from imetadata.base.c_resource import CResource


class CUtils(CResource):
    @classmethod
    def one_id(cls) -> str:
        name = 'metadata.org'
        uuid_text = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid4())))
        uuid_text = uuid_text.replace('-', '')
        return uuid_text

    @classmethod
    def plugins_id_by_file_main_name(cls, file_main_name) -> str:
        super_id = file_main_name
        id_list = super_id.split('_', 2)
        if len(id_list) > 2:
            return id_list[2]
        else:
            return super_id

    @classmethod
    def equal_ignore_case(cls, str1: str, str2: str) -> bool:
        return str1.strip().lower() == str2.strip().lower()

    @classmethod
    def quote(cls, str1: str) -> str:
        return "'{0}'".format(str1.strip())

    @classmethod
    def dict_value_by_name(cls, dict_obj: dict, name: str, default_value, ignore_case=True) -> any:
        keys = dict_obj.keys()
        for key in keys:
            if ignore_case:
                if cls.equal_ignore_case(key, name):
                    return dict_obj[key]
            else:
                if key.strip() == name.strip():
                    return dict_obj[key]
        else:
            return default_value

    @classmethod
    def list_count(cls, list_obj: list, name: str, ignore_case=True) -> int:
        if not ignore_case:
            return list_obj.count(name)
        else:
            result_int = 0
            for list_item in list_obj:
                if cls.equal_ignore_case(cls.any_2_str(list_item), name):
                    result_int = result_int + 1
            return result_int

    @classmethod
    def any_2_str(cls, obj) -> str:
        if obj is None:
            return ''
        else:
            return str(obj)

    @classmethod
    def int_2_format_str(cls, int_value: int, length: int) -> str:
        rt_int_value = int_value
        if rt_int_value is None:
            rt_int_value = 1

        str_value = cls.any_2_str(rt_int_value)
        if len(str_value) >= length:
            return str(str_value)
        else:
            count_zero = length - len(str_value)
            str_zero = '0'*count_zero
            return '{0}{1}'.format(str_zero, str_value)

    @classmethod
    def text_match_re(cls, text, regex) -> bool:
        return re.search(regex, text) is not None

    @classmethod
    def text_is_numeric(cls, check_text: str) -> bool:
        """
        判断是否为数字
        :param check_text:
        :return:
        """
        return check_text.isdigit()

    @classmethod
    def text_is_alpha(cls, check_text: str) -> bool:
        """
        判断是否字母
        :param check_text:
        :return:
        """
        return check_text.isalpha()

    @classmethod
    def split(cls, split_text: str, split_sep_list: list) -> list:
        """
        根据指定的分隔符数组, 对指定文本进行分割
        :param split_text:
        :param split_sep_list:
        :return:
        """
        text_part_list = split_text.split(split_sep_list[0])
        for index in range(len(split_sep_list)):
            if index == 0:
                continue
            result_list = cls.__split_list(text_part_list, split_sep_list[index])
            text_part_list = result_list
        # for item in text_part_list:
        #     print(item)
        return text_part_list

    @classmethod
    def __split_list(cls, text_part_list: list, split_sep: str) -> list:
        """
        私有方法：根据分割的文本段数组、分隔符获取分割后的结果集合
        @param text_part_list:
        @param split_sep:
        @return:
        """
        result_list = []
        for text_item in text_part_list:
            text_part_list2 = text_item.split(split_sep)
            for item in text_part_list2:
                result_list.append(item)
        return result_list

    @classmethod
    def alpha_text(cls, src_text) -> str:
        """
        获取中文字符串的拼音首字母
        :param src_text:
        :return:
        """
        rt_src_text = cls.any_2_str(src_text)
        if cls.equal_ignore_case(rt_src_text, ''):
            return ''
        else:
            return pinyin.get_initial(src_text, delimiter="").lower().strip().replace(' ', '')


if __name__ == '__main__':
    # text_alpha = r'你/好 A\B\B C/中_国'
    # print(CUtils.split(text_alpha, ['/', '\\', ' ', '_', '-']))
    # check_text = '-12'
    # print(CUtils.text_is_numeric(check_text))
    print(CUtils.int_2_format_str(None, 2))
