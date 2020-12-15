# -*- coding: utf-8 -*- 
# @Time : 2020/9/30 10:43 
# @Author : 王西亚 
# @File : test_c_utils.py

from imetadata.base.c_utils import CUtils


class Test_CUtils:

    def test_split(self):
        text_split = 'aa/bb\\cc_dd-ee ff'
        text_list = CUtils.split(text_split, ['\\', '/', '-', '_', ' '])
        assert len(text_list) == 6
        assert text_list.count('ff') == 1
        assert text_list
        print(text_list)

    def test_alpha_text(self):
        text_alpha = r'你好 abc中国'
        print(text_alpha)
        result_alpha = CUtils.alpha_text(text_alpha)
        print(result_alpha)
        assert result_alpha == 'nhabczg'

    def test_dict_value_by_name(self):
        dict_value = {
            'name': 'test',
            'srid': None,
            'value': 5
        }
        srid = CUtils.dict_value_by_name(dict_value, 'srid', 4326)
        assert srid == 4326

    def test_replace_placeholder(self):
        holder_text = '${0}'.format('value')
        holder_text = CUtils.replace_placeholder(holder_text, {'value': 'wangxiya'})
        assert holder_text == 'wangxiya'
