#!/usr/bin/python3
# -*- coding:utf-8 -*-
import settings


class LayerDef(object):
    def __init__(self):
        '''
        todo(张雄雄） 添加标注、标注显示比例尺、矢量显示比例尺、查询字段等属性
        '''
        self.id = ""
        self.name = ''
        # Raster/Vector
        self.type = ''
        self.classidetify = ''
        # File/Folder
        self.sourcetype = ''
        # self.sourcepath = []
        self.sourcepath = {}


class ServiceDef(object):
    def __init__(self, sid, sname):
        self.id = sid
        self.name = sname
        self.cache = False
        self.cachelevel = 16
        # 服务坐标系
        self.coordinates = []
        # 服务的图层定义数组
        self.layers = []

    def getGrids(self):
        grids = ''
        epsgname = dict({'EPSG:3857': 'webmercator', 'EPSG:4326': 'wgs84', 'EPSG:4490': 'cgcs2000'})
        for coor in self.coordinates:
            if coor in epsgname.keys():
                grids = grids + epsgname[coor] + ','
            else:
                grids = grids + coor + ','
        return grids.rstrip(',')


if __name__ == '__main__':
    print(settings.application.xpath_one('data2service.tindex_dir', None))
