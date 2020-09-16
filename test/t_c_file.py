# -*- coding: utf-8 -*- 
# @Time : 2020/9/7 11:00 
# @Author : 王西亚 
# @File : t_c_file.py

import pytest
from imetadata.base.c_file import CFile
import allure


class Test_C_File:

    @allure.title('测试文件名是否获取完整')
    def test_file_main_name(self):
        assert CFile.file_main_name(r'/Users/Clare/gf1.tar.gz') == r'gf1'
