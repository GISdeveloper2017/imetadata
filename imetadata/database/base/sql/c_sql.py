# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 15:03 
# @Author : 王西亚 
# @File : c_sql.py


class CSql:
    def __init__(self, database_type, database_version):
        self.__database_type__ = database_type
        self.__database_version__ = database_version

    @property
    def database_type(self):
        return self.__database_type__

    @property
    def database_version(self):
        return self.__database_version__

    def func_wkt2geometry(self, wkt: str, srid: int):
        return ''

    def func_geometry2wkt(self, wkt: str):
        return ''
