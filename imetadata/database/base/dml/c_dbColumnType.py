# -*- coding: utf-8 -*- 
# @Time : 2020/11/23 21:16 
# @Author : 王西亚 
# @File : c_dbColumnType.py

class CDBColumnType:
    def __init__(self, db_column_type_filter: str, inner_type: str, set_value_method: str, set_value_template=None,
                 function_param_quoted=False, function_param_max_size=-1):
        self._db_column_type_filter = db_column_type_filter
        self._inner_type = inner_type
        self._set_value_method = set_value_method
        self._set_value_template = set_value_template
        self._function_param_quoted = function_param_quoted
        self._function_param_max_size = function_param_max_size

    @property
    def function_param_quoted(self):
        return self._function_param_quoted

    @property
    def function_param_max_size(self):
        return self._function_param_max_size

    @property
    def db_column_type_filter(self):
        return self._db_column_type_filter

    @property
    def inner_type(self):
        return self._inner_type

    @property
    def set_value_method(self):
        return self._set_value_method

    @property
    def set_value_template(self):
        return self._set_value_template
