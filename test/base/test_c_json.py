# -*- coding: utf-8 -*- 
# @Time : 2020/9/4 17:12 
# @Author : 王西亚 
# @File : test_c_json.py 

from imetadata.base.c_json import CJson


class Test_C_Json:
    test_filename: str = r"C:\Users\Clare\PycharmProjects\pythonProject\test1.xml"
    test_text: str = '{"a":1,"b":2,"c":3,"d":4,"中文属性":5, "student": [{"name":"小明", "birthday": "2020-1-1"}, {"name":"小王", "birthday": "2020-2-1"}]}'

    def test_load_text(self):
        json = CJson()
        json.load_json_text(self.test_text)
        assert True

    def test_get_attr(self):
        json = CJson()
        json.load_json_text(self.test_text)
        assert json.xpath_one('a', -1) == 1
        assert json.xpath_one('aa', -1) == -1
        assert json.xpath_one('student[0].name', '') == '小明'
        assert json.xpath_one('student[1].name', '') == '小王'

    def test_get_attr_by_class_method(self):
        value = CJson.json_attr_value(self.test_text, 'b', 1)
        assert value == 2

    def test_get_chn_attr_by_class_method(self):
        value = CJson.json_attr_value(self.test_text, '中文属性', 1)
        assert value == 5

    def test_load_obj(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        json_obj = CJson()
        json_obj.load_obj(data)
        assert json_obj.xpath_one('a', -1) == 1


if __name__ == '__main__':
    file_name = '/Users/wangxiya/Downloads/gdb.json'
    json = CJson()
    json.load_file(file_name)
    data_source = json.xpath_one('datasource', None)
    layers = json.xpath_one('layers', None)
    target_json = CJson()
    target_json.set_value_of_name('datasource', data_source)
    target_json.set_value_of_name('layer_count', 1)
    target_json.set_value_of_name('layers', [layers[0]])
    print(target_json.to_json())
