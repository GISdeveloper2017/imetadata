# -*- coding: utf-8 -*- 
# @Time : 2020/9/1 18:01 
# @Author : 王西亚 
# @File : test_c_process.py

import pytest
import os
import random
import allure
from imetadata.base.c_processUtils import CProcessUtils


class Test_C_Process:
    @allure.step("测试的随机进程为：{1}")
    def show_process_id(self, process_id):
        return process_id

    @allure.title('测试自己的进程是否存在')
    def test_process_id_exist(self):
        if CProcessUtils.process_id_exist(os.getpid()):
            assert True
        else:
            assert False

    # @allure.title('测试一个随机进程是否存在')
    # def test_random_process_id_exist(self):
    #     process_id = random.randint(40000, 60000)
    #     if CProcessUtils.process_id_exist(self.show_process_id(process_id)):
    #         assert False
    #     else:
    #         assert True
    #
    # @allure.title('测试一个指定的进程是否存在')
    # def test_main_process_id_exist(self):
    #     process_id = 46137
    #     if CProcessUtils.process_id_exist(process_id):
    #         assert True
    #     else:
    #         assert False
