# -*- coding: utf-8 -*- 
# @Time : 2020/10/5 10:03 
# @Author : 王西亚 
# @File : c_mdSpatial.py

class CMDSpatial:
    def __init__(self):
        self.__native_bbox__ = None
        self.__native_geom__ = None
        self.__native_center__ = None
        self.__wgs84_bbox__ = None
        self.__wgs84_geom__ = None
        self.__wgs84_center__ = None

    @property
    def native_box(self):
        return self.__native_bbox__

    @native_box.setter
    def native_box(self, value):
        self.__native_bbox__ = value

    @property
    def native_geom(self):
        return self.__native_geom__

    @native_geom.setter
    def native_geom(self, value):
        self.__native_geom__ = value

    @property
    def native_center(self):
        return self.__native_center__

    @native_center.setter
    def native_center(self, value):
        self.__native_center__ = value

    @property
    def wgs84_bbox(self):
        return self.__wgs84_bbox__

    @wgs84_bbox.setter
    def wgs84_bbox(self, value):
        self.__wgs84_bbox__ = value

    @property
    def wgs84_geom(self):
        return self.__wgs84_geom__

    @wgs84_geom.setter
    def wgs84_geom(self, value):
        self.__wgs84_geom__ = value

    @property
    def wgs84_center(self):
        return self.__wgs84_center__

    @wgs84_center.setter
    def wgs84_center(self, value):
        self.__wgs84_center__ = value
