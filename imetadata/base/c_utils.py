#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
import re
import uuid
import pinyin
from imetadata.base.c_resource import CResource
from imetadata.base.c_time import CTime
from osgeo import gdal, ogr, osr
from string import Template


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
    def replace_placeholder(cls, text: str, dict_obj: dict, safe: bool = True, **kwargs) -> str:
        if safe:
            return Template(text).safe_substitute(dict_obj, kwargs)
        else:
            return Template(text).substitute(dict_obj, kwargs)

    @classmethod
    def equal_ignore_case(cls, str1: str, str2: str) -> bool:
        return cls.any_2_str(str1).strip().lower() == cls.any_2_str(str2).strip().lower()

    @classmethod
    def quote(cls, str1: str) -> str:
        return "'{0}'".format(str1.strip())

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
        TODO 赵宇飞 判断是否为年月日,或年月（不包含时间），如202010,2020/10,2020-10 或20201022,2020/10/22,2020-10-22
        @param check_text:
        @return:
        """
        if cls.text_is_date_day(check_text):
            return True
        elif cls.text_is_date_month(check_text):
            return True
        return False

    @classmethod
    def text_is_date_day(cls, check_text: str) -> bool:
        """
        TODO 张源博 判断是否为年月日（不包含时间），如20201022,2020/10/22,2020-10-22
        @param check_text:
        @return:
        """
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
        try:
            value = float(obj)
            return value
        except:
            return default_value

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

    @classmethod
    def is_vector_file_can_read(cls, vector_file_with_path: str) -> bool:
        """
        todo 张源博 判断矢量文件的可读性，采用进程读取
        @param vector_file_with_path:
        @return:
        """
        vector_ds = ogr.Open(vector_file_with_path)
        if vector_ds is not None:
            return True
        return False

    @classmethod
    def is_vector_dataset_can_read(cls, vector_dataset_with_path: str) -> bool:
        """
        todo 判断矢量数据集的可读性（mdb中的矢量图层，gdb中的矢量图层），注意函数的参数可能不够，先预留
              采用进程读取
        @param vector_file_with_path:
        @return:
        """
        return False

    @classmethod
    def is_raster_file_can_read(cls, raster_file_with_path: str) -> bool:
        """
        todo 张源博 判断影像文件的可读性,除了能正常打开外，还需要获取块的大小，并且读取第1个块和最后一个块有值，才能确定影像正常可以读取
          采用进程读取
        @param raster_file_with_path:
        @return:
        """
        raster_ds = gdal.Open(raster_file_with_path, gdal.GA_ReadOnly)
        if raster_ds is None:
            return False
        else:
            """
              在这里获取块的大小，并且读取第1个块和最后一个块有值，才能确定影像正常可以读取
            """
            pass
        return True


if __name__ == '__main__':
    # text_alpha = r'你/好 A\B\B C/中_国'
    # print(CUtils.split(text_alpha, ['/', '\\', ' ', '_', '-']))
    check_text = '-125.02'
    check_text = '12'
    check_text = '2001-01'
    print('check_text: ' + CUtils.any_2_str(check_text))
    print('numeric: ' + CUtils.any_2_str(CUtils.text_is_numeric(check_text)))
    print('decimal: ' + CUtils.any_2_str(CUtils.text_is_decimal(check_text)))
    print('integer: ' + CUtils.any_2_str(CUtils.text_is_integer(check_text)))
    print('date: ' + CUtils.any_2_str(CUtils.text_is_date(check_text)))
    print(CUtils.int_2_format_str(None, 2))

    name = '中国'
    str_show = f'{name} is my country'
    print(str_show)
    print(len(name))
    print(len('12'))
