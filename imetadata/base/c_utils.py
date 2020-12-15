#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import re
import uuid
from datetime import datetime
from string import Template

import pinyin

from imetadata.base.c_resource import CResource
from imetadata.base.c_time import CTime


class CUtils(CResource):
    @classmethod
    def str_append(cls, src_str: str, second_str: str, seperator_str: str = '\n') -> str:
        result = src_str
        if second_str == '':
            return result

        if result != '':
            result = '{0}{1}'.format(result, seperator_str)

        return '{0}{1}'.format(result, second_str)

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
    def replace_placeholder(cls, text: str, dict_obj: dict, safe: bool = True) -> str:
        """
        按照Python的Template规范进行占位符的替换
        占位符格式如下:
        . $name
        . ${$name}
        具体百度python template
        如果字符串里需要$, 则使用$$消除占位语法

        :param text:
        :param dict_obj:
        :param safe:
        :return:
        """
        if dict_obj is None:
            return text

        if safe:
            return Template(text).safe_substitute(dict_obj)
        else:
            return Template(text).substitute(dict_obj)

    @classmethod
    def equal_ignore_case(cls, str1: str, str2: str) -> bool:
        return cls.any_2_str(str1).strip().lower() == cls.any_2_str(str2).strip().lower()

    @classmethod
    def quote(cls, str1: str) -> str:
        return "'{0}'".format(cls.any_2_str(str1))

    @classmethod
    def dict_value_by_name(cls, dict_obj: dict, name: str, default_value, ignore_case=True) -> any:
        if dict_obj is None:
            return default_value

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
        if list_obj is None:
            return 0
        elif not ignore_case:
            return list_obj.count(name)
        else:
            result_int = 0
            for list_item in list_obj:
                if cls.equal_ignore_case(cls.any_2_str(list_item), name):
                    result_int = result_int + 1
            return result_int

    @classmethod
    def list_2_str(cls, list_obj: list, prefix: str, separator: str, suffix: str, ignore_empty: bool = False) -> str:
        if list_obj is None:
            return ''
        elif len(list_obj) == 0:
            return ''
        else:
            result = ''
            for list_item in list_obj:
                list_text = cls.any_2_str(list_item)
                if ignore_empty:
                    if cls.equal_ignore_case(list_text, ''):
                        continue

                result = cls.str_append(
                    result,
                    '{0}{1}{2}'.format(prefix, list_text, suffix),
                    separator
                )
            return result

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
            str_zero = '0' * count_zero
            return '{0}{1}'.format(str_zero, str_value)

    @classmethod
    def text_match_re(cls, text, regex) -> bool:
        return re.search(regex, text) is not None

    @classmethod
    def text_is_numeric(cls, check_text: str) -> bool:
        """
        判断是否为纯数字（不带负号，不带.符号）
        :param check_text:
        :return:
        """
        return check_text.isdigit()

    @classmethod
    def text_is_date(cls, check_text: str) -> bool:
        """
        TODO 赵宇飞 判断是否为年月日,或年月,或年（不包含时间），如2020,202010,2020/10,2020-10 或20201022,2020/10/22,2020-10-22
        @param check_text:
        @return:
        """
        if cls.text_is_date_day(check_text):
            return True
        elif cls.text_is_date_month(check_text):
            return True
        elif cls.text_is_date_year(check_text):
            return True
        return False

    @classmethod
    def text_is_date_day(cls, check_text: str) -> bool:
        """
        TODO 张源博 判断是否为年月日（不包含时间），如20201022,2020/10/22,2020-10-22,2020.10.22,2020年10月22日
        @param check_text:
        @return:
        """
        # 日期格式最低8位
        if CUtils.len_of_text(check_text) < 8:
            return False
        time_format = "%Y{0}%m{0}%d"
        sep_real = ""
        sep_list = ['-', '/']
        for sep in sep_list:
            if sep in check_text:
                sep_real = sep
                break
        time_format_real = time_format.format(sep_real)
        default_date = CTime.now()
        date_value = CTime.from_datetime_str(check_text, default_date, time_format_real)
        if CUtils.equal_ignore_case(date_value, default_date):
            return False
        return True

    @classmethod
    def text_is_date_month(cls, check_text: str) -> bool:
        """
        TODO 赵宇飞 判断是否为年月（不包含日），如202010,2020/10,2020-10
        @param check_text:
        @return:
        """
        time_format = "%Y{0}%m"
        sep_real = ""
        sep_list = ['-', '/']
        for sep in sep_list:
            if sep in check_text:
                sep_real = sep
                break
        time_format_real = time_format.format(sep_real)
        default_date = CTime.now()
        date_value = CTime.from_datetime_str(check_text, default_date, time_format_real)
        if CUtils.equal_ignore_case(date_value, default_date):
            return False
        return True

    @classmethod
    def text_is_date_year(cls, check_text: str) -> bool:
        """
        TODO 赵宇飞 判断是否为年（不包含月日），如2020
        @param check_text:
        @return:
        """
        time_format = "%Y"
        default_date = CTime.now()
        date_value = CTime.from_datetime_str(check_text, default_date, time_format)
        if CUtils.equal_ignore_case(date_value, default_date):
            return False
        return True

    @classmethod
    def text_is_datetime(cls, check_text: str) -> bool:
        """
        TODO 张源博 判断是否为日期时间（包含时间），如20201022 22:22:22.345,
        2020/10/22 22:22:22.345, 2020-10-22 22:22:22.345, 2020-10-22T22:22:22.000007
        @param check_text:
        @return:
        """
        time_format = "%Y{0}%m{0}%d{1}%H:%M:%S{2}"
        sep_real = ""
        sep_list = ['-', '/']
        for sep in sep_list:
            if sep in check_text:
                sep_real = sep
                break
        # 判断是否带T，GMT
        sign_real = " "
        sign_list = ['T', 'CST']
        for sign in sign_list:
            if sign in check_text:
                sign_real = sign
                break
        second_real = ""
        if "." in check_text:
            second_real = ".%f"
        time_format_real = time_format.format(sep_real, sign_real, second_real)
        default_date = CTime.now()
        date_value = CTime.from_datetime_str(check_text, default_date, time_format_real)
        if CUtils.equal_ignore_case(date_value, default_date):
            return False
        return True

    @classmethod
    def text_is_date_or_datetime(cls, check_text: str) -> bool:
        """
        判断是否为日期或日期时间），如20201022,2020/10/22,2020-10-22，
            20201022 22:22:22.345,2020/10/22 22:22:22.345,2020-10-22 22:22:22.345, 2020-10-22T22:22:22.000007
        @param check_text:
        @return:
        """
        if cls.text_is_date(check_text):
            return True
        elif cls.text_is_datetime(check_text):
            return True
        return False

    def standard_datetime_format(date_text: str, default_date) -> datetime:
        """
        将日期或日期时间格式化为YYYY-MM-DD HH:MM:SS格式，如20201022,2020/10/22格式化为2020-10-22，
            20201022 22:22:22.345,2020/10/22 22:22:22.345格式化为2020-10-22 22:22:22.345, 2020-10-22T22:22:22.000007
        @param date_text:
        @param default_date:  CTime.now()
        @return:
        """
        # default_date = CTime.now()
        try:
            time_format_real = '%Y-%m-%d %H:%M:%S'
            time_format = ["%Y{0}", "%Y{0}%m{1}", "%Y{0}%m{1}%d{2}{3}%H:%M:%S{4}", "%Y{0}%m{1}%d{2}", "%Y",
                           "%Y{0}%m", "%Y{0}%m{0}%d{1}%H:%M:%S{2}", "%Y{0}%m{0}%d"]

            str_len = len(date_text)

            # 汉字标记
            ch_flag = 0
            if ('年' in date_text) or ('月' in date_text) or ('日' in date_text):
                ch_flag = 1

            # 日期时间标记
            sign_flag = 0
            sign_list = ['T', 'CST', ' ']
            for sign in sign_list:
                if sign in date_text:
                    sign_flag = 1
                    break

            if ch_flag:
                if str_len == 5:
                    time_format_real = time_format[0].format('年')
                    date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                    if CUtils.equal_ignore_case(date_value, default_date):
                        return default_date
                    return CTime.format_str(date_value, '%Y')
                elif (str_len == 7) or (str_len == 8):
                    time_format_real = time_format[1].format('年', '月')
                    date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                    if CUtils.equal_ignore_case(date_value, default_date):
                        return default_date
                    return CTime.format_str(date_value, '%Y-%m')
                elif str_len >= 9:
                    if sign_flag:
                        sign_real = " "
                        sign_list = ['CST', 'T']
                        for sign in sign_list:
                            if sign in date_text:
                                sign_real = sign
                                break
                        sec_real = ""
                        if "." in date_text:
                            sec_real = ".%f"
                        time_format_real = time_format[2].format('年', '月', '日', sign_real, sec_real)
                        date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                        if CUtils.equal_ignore_case(date_value, default_date):
                            return default_date
                        return CTime.format_str(date_value, '%Y-%m-%d %H:%M:%S')
                    else:
                        time_format_real = time_format[3].format('年', '月', '日')
                    date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                    if CUtils.equal_ignore_case(date_value, default_date):
                        return default_date
                    return CTime.format_str(date_value, '%Y-%m-%d')
            else:
                if str_len == 4:
                    time_format_real = time_format[4]
                    date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                    if CUtils.equal_ignore_case(date_value, default_date):
                        return default_date
                    return CTime.format_str(date_value, '%Y')
                elif (str_len == 6) or (str_len == 7):
                    sep_real = ""
                    sep_list = ['-', '/', '.']
                    for sep in sep_list:
                        if sep in date_text:
                            sep_real = sep
                            break
                    time_format_real = time_format[5].format(sep_real)
                    date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                    if CUtils.equal_ignore_case(date_value, default_date):
                        return default_date
                    return CTime.format_str(date_value, '%Y-%m')
                elif str_len >= 8:
                    if sign_flag:
                        sign_real = " "
                        sign_list = ['CST', 'T']
                        for sign in sign_list:
                            if sign in date_text:
                                sign_real = sign
                                break
                        date, time = date_text.split(sign_real)
                        sep_real = ""
                        sep_list = ['-', '/', '.']
                        for sep in sep_list:
                            if sep in date:
                                sep_real = sep
                                break
                        sec_real = ""
                        if "." in time:
                            sec_real = ".%f"
                        time_format_real = time_format[6].format(sep_real, sign_real, sec_real)
                        date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                        if CUtils.equal_ignore_case(date_value, default_date):
                            return default_date
                        return CTime.format_str(date_value, '%Y-%m-%d %H:%M:%S')
                    else:
                        sep_real = ""
                        sep_list = ['-', '/', '.']
                        for sep in sep_list:
                            if sep in date_text:
                                sep_real = sep
                                break
                        time_format_real = time_format[7].format(sep_real)
                        date_value = CTime.from_datetime_str(date_text, default_date, time_format_real)
                        if CUtils.equal_ignore_case(date_value, default_date):
                            return default_date
                        return CTime.format_str(date_value, '%Y-%m-%d')

        except:
            return default_date

    @classmethod
    def text_is_decimal(cls, check_text: str) -> bool:
        """
        判断是否为小数，（必须有小数点，包含正小数，负小数，不包含整数）
            1.小数点个数可以使用.count()方法
            2.按照小数点进行分割 例如： 1.98 [1,98]
            3.正小数：小数点左边是整数，右边也是整数 可以使用.isdigits()方法
            4.负小数：小数点左边是是负号开头，但是只有一个负号，右边也是整数
        :param check_text:
        :return:
        """
        check_text = cls.any_2_str(check_text)
        check_text_list = None
        if check_text.count(".") == 1:  # 小数点个数
            check_text_list = check_text.split(".")
        if check_text_list is None:
            return False
        left = check_text_list[0]  # 小数点左边
        right = check_text_list[1]  # 小数点右边
        if left.isdigit() and right.isdigit():
            return True
        elif left.startswith('-') and left.count('-') == 1 and left.split('-')[1].isdigit() and right.isdigit():
            return True
        return False

    @classmethod
    def text_is_integer(cls, check_text: str) -> bool:
        """
        判断是否为整数（包含正负整数，不带.符号）
        :param check_text:
        :return:
        """
        try:
            temp_value = int(check_text)
            return isinstance(temp_value, int)
        except ValueError:
            return False

    @classmethod
    def text_is_decimal_or_integer(cls, check_text: str) -> bool:
        """
        判断是否为小数或整数（包含负数）
        :param check_text:
        :return:
        """
        if cls.text_is_decimal(check_text):
            return True
        elif cls.text_is_integer(check_text):
            return True
        return False

    @classmethod
    def text_is_decimal_or_integer_positive(cls, check_text: str) -> bool:
        """
        判断是否为正小数或整数（不包含负数）
        :param check_text:
        :return:
        """
        if cls.text_is_decimal_or_integer(check_text):
            value_num = float(check_text)
            if value_num > 0:
                return True
        return False

    @classmethod
    def text_is_alpha(cls, check_text: str) -> bool:
        """
        判断是否字母
        :param check_text:
        :return:
        """
        return check_text.isalpha()

    @classmethod
    def text_is_string(cls, obj):
        """
        判断是否是字符串文本
        @param obj:
        @return:
        """
        return isinstance(obj, str)

    @classmethod
    def len_of_text(cls, text_obj):
        """
        获取文本或数字类型的长度
        @param text_obj:
        @return:
        """
        value_str = CUtils.any_2_str(text_obj)
        len_text = len(value_str)
        return len_text

    @classmethod
    def to_decimal(cls, obj, default_value=-1):
        """
        文本转小数
        @param obj:
        @param default_value:
        @return:
        """
        if CUtils.equal_ignore_case(obj, ''):
            return default_value
        try:
            value = float(obj)
            return value
        except:
            return default_value

    @classmethod
    def to_integer(cls, obj, default_value=-1):
        """
        文本转整数
        @param obj:
        @param default_value:
        @return:
        """
        if CUtils.equal_ignore_case(obj, ''):
            return default_value
        try:
            value_decimal = cls.to_decimal(obj, default_value)
            value = int(value_decimal)
            return value
        except:
            return default_value

    @classmethod
    def text_to_lower(cls, text):
        """
        文本转小写
        @param text:
        @return:
        """
        if text is not None:
            return text.lower()
        return text

    @classmethod
    def to_day_format(cls, text, default_value):
        """
        文本转日（只对年、月转换），日不用转，只会格式化,
            2020  2020年  转为 20200101
            202009 2020-09 2020/09  2020年9月   转为20200901
        @param text:
        @param default_value:
        @return:
        """
        # default_date = CTime.now()
        date_value = cls.standard_datetime_format(text, default_value)
        if CUtils.equal_ignore_case(date_value, default_value):
            return default_value
        date_value = date_value.replace('-', '')
        day_format = ''
        if CUtils.len_of_text(date_value) == 4:
            day_format = '{0}0101'.format(date_value)
        elif CUtils.len_of_text(date_value) == 6:
            day_format = '{0}01'.format(date_value)
        else:
            day_format = date_value
        return day_format

    @classmethod
    def split(cls, split_text: str, split_sep_list: list) -> list:
        """
        根据指定的分隔符数组, 对指定文本进行分割
        :param split_text:
        :param split_sep_list:
        :return:
        """
        if split_sep_list is None:
            return [split_text]

        text_part_list = split_text.split(split_sep_list[0])
        for index in range(len(split_sep_list)):
            if index == 0:
                continue
            result_list = cls.__split_list(text_part_list, split_sep_list[index])
            text_part_list = result_list
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
    text = "to_jsonb(${value})"
    print(CUtils.replace_placeholder(text, {'value': 'my_value'}))

    # str22 = '30'
    # sa = CUtils.to_integer(str22, -1)
    # print(sa)
