# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 17:52 
# @Author : 王西亚 
# @File : test_c_vectorDataSets.py
from imetadata.tool.datasets.c_vectorDataSets import CVectorDataSets


class Test_CVectorDataSets:
    def test_parser_vector_file(self):
        file_name = '/Users/wangxiya/Documents/我的测试数据/31.混合存储/测试数据/通用数据/矢量数据集/生态治理和水土保持监测数据库_黑岱沟露天煤矿_10017699_2020d1_2020-01-01.mdb'
        vector_datasets = CVectorDataSets(file_name)
        vector_datasets.open()
        try:
            assert vector_datasets.active
        finally:
            vector_datasets.close()
