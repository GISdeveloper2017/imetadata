# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 15:06 
# @Author : 王西亚 
# @File : c_sqlPostgresql.py
from imetadata.database.base.sql.c_sql import CSql


class CSqlPostgresql(CSql):
    def func_wkt2geometry(self, wkt: str, srid: int):
        return "st_geomfromtext({0}, {1})".format(wkt, srid)

    def func_geometry2wkt(self, wkt: str):
        return "st_astext({0})".format(wkt)
