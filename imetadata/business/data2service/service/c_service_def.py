#!/usr/bin/python3
# -*- coding:utf-8 -*-
from imetadata import settings

class LayerDef(object):
    def __init__(self):
        self.id = ""
        self.name = ''
        self.type = ''
        self.classidetify = ''
        self.sourcetype = ''
        self.sourcepath = []

class ServiceDef(object):
    def __init__(self, sid, sname):
        self.id = sid
        self.name = sname
        self.cache = False
        self.cachelevel = 16
        self.coordinates = []
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
