#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import datetime
from osgeo import ogr, gdal, osr
import copy
import uuid
import codecs
from imetadata.settings import application
from imetadata.base.c_json import CJson
from imetadata.business.data2service.service import c_geo_util as geoUtils
from imetadata.business.data2service.service import c_mapfileHelper as mapfileHelper
from imetadata.base.c_logger import CLogger

basedir = os.path.abspath(os.path.dirname(__file__))


def clear_failure(service_name):
    service_files = []
    for ext in ['.shp', '.dbf', '.shx', 'prj']:
        service_files.append(os.path.join(application.xpath_one('data2service.tindex_dir', None), service_name + ext))

    service_files.append(os.path.join(application.xpath_one('data2service.map_dir', None), 'service_' + service_name + '.map'))
    service_files.append(os.path.join(application.xpath_one('data2service.yaml_dir', None), 'service_' + service_name + '.yaml'))
    service_files.append(os.path.join(application.xpath_one('data2service.seed_dir', None), 'service_seed_' + service_name + '.yaml'))
    service_files.append(os.path.join(application.xpath_one('data2service.wsgi_dir', None), 'service_' + service_name + '.wsgi'))

    service_files.append(os.path.join(application.xpath_one('data2service.map_dir', None), service_name + '.map'))
    service_files.append(os.path.join(application.xpath_one('data2service.yaml_dir', None), service_name + '.yaml'))
    service_files.append(os.path.join(application.xpath_one('data2service.wsgi_dir', None), service_name + '.wsgi'))

    for ser_file in service_files:
        if os.path.exists(ser_file):
            os.remove(ser_file)


def CreateTIndex(shpname, imgpaths):
    print('img files count:' + str(len(imgpaths)))
    CLogger().info('img files count:' + str(len(imgpaths)))

    raster_file = ' '.join(imgpaths)
    proj4 = geoUtils.GetProj4(imgpaths[0])

    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")

    options = ["ENCODING=UTF-8"]
    srs = osr.SpatialReference()
    srs.ImportFromProj4(proj4)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    tindex_ds = driver.CreateDataSource(shpname)
    lyr = tindex_ds.CreateLayer(str(os.path.split(shpname)[-1]), srs, ogr.wkbPolygon, options=options)

    # add field
    n_max_field_size = 254
    tile_index_field = ogr.FieldDefn("location", ogr.OFTString)
    tile_index_field.SetWidth(n_max_field_size)
    lyr.CreateField(tile_index_field)

    srs_field = ogr.FieldDefn("src_srs", ogr.OFTString)
    srs_field.SetWidth(n_max_field_size)
    lyr.CreateField(srs_field)

    del lyr
    tindex_ds.Destroy()
    del driver

    cmd = r'gdaltindex -src_srs_name src_srs -write_absolute_path {0} {1}'
    if len(imgpaths) > 500:
        cnt = int(len(imgpaths) / 500)
        for kk in range(cnt):
            raster_file = ' '.join(imgpaths[kk * 500: (kk + 1) * 500 - 1])
            os.system(cmd.format(shpname, raster_file))
        raster_file = ' '.join(imgpaths[cnt * 500:])
        os.system(cmd.format(shpname, raster_file))
    else:
        os.system(cmd.format(shpname, raster_file))

    CLogger().info('created tileIndex: ' + shpname)


def RepFile(srcfile, dstfile, kvs):
    srcfp = codecs.open(srcfile, 'r', encoding='utf-8')
    srccontent = srcfp.read()
    for k in kvs:
        srccontent = srccontent.replace(k, kvs[k])
    dstfp = codecs.open(dstfile, 'w', encoding='utf-8')
    dstfp.write(srccontent)
    srcfp.close()
    dstfp.close()


def RepTemp(srccontent, dstfile, kvs):
    for k in kvs:
        srccontent = srccontent.replace(k, kvs[k])
    dstfp = open(dstfile, 'w')
    dstfp.write(srccontent)
    dstfp.close()


def RepString(src_string, kvs):
    dst_string = src_string
    for k in kvs:
        dst_string = dst_string.replace(k, kvs[k])

    return dst_string


def ExtendEnvlope(geoextent):
    hor_delta = (geoextent[1] - geoextent[0]) * 0.05
    ver_delta = (geoextent[3] - geoextent[2]) * 0.05

    return (geoextent[0] - hor_delta, geoextent[1] + hor_delta, geoextent[2] - ver_delta, geoextent[3] + ver_delta)


def Link254Limit(service_define, src_path) -> str:
    '''解决shp文件字段长度只能到254的问题
    '''
    if len(src_path.encode('utf-8')) < 255:
        return src_path

    path_parts = src_path.split('/')

    if len(path_parts) < 5:
        raise Exception("the file path is too long " + src_path)
    else:
        link_src = '/'.join(path_parts[:-2])
        link_path = os.path.join(application.xpath_one('data2service.tindex_dir', None), service_define.id)
        if not os.path.exists(link_path):
            os.mkdir(link_path)

        for subs in os.listdir(link_path):
            if os.path.islink(os.path.join(link_path, subs)):
                if os.readlink(os.path.join(link_path, subs)) == link_src:
                    return os.path.join(os.path.join(link_path, subs), '/'.join(path_parts[-2:]))

        link_dst_name = str(uuid.uuid1())
        link_dst_path = os.path.join(link_path, link_dst_name, '/'.join(path_parts[-2:]))
        if len(link_dst_path) > 254:
            raise Exception("the file path is too long " + src_path)
        os.symlink(link_src, os.path.join(link_path, link_dst_name))
        return link_dst_path


def ToLinuxPath(src_path) -> str:
    linux_path = src_path

    linux_path = linux_path.replace('\\', '/').replace('//', '/')
    return linux_path


def GetAllSources(service_define, lyr_define, tindex) -> list:
    ''' get all source of a layer, if layer type is raster, tindex is true, return tileIndex, false, return rasters
    :param tindex 布尔值，是否返回tileIndex矢量
    '''
    shp_path_list = []
    tindex_dir = application.xpath_one('data2service.tindex_dir', None)
    if lyr_define.type.lower() == 'vector':
        if lyr_define.sourcetype.lower() == 'folder':
            for src_key in lyr_define.sourcepath:
                for folder in lyr_define.sourcepath[src_key]:
                    linux_folder = ToLinuxPath(folder)
                    shp_path_list.extend(geoUtils.GetShpPaths(linux_folder))
        elif lyr_define.sourcetype.lower() == 'file':
            for src_key in lyr_define.sourcepath:
                for shp_path in lyr_define.sourcepath[src_key]:
                    linux_path = ToLinuxPath(shp_path)
                    shp_path_list.append(linux_path)
        else:
            for src_key in lyr_define.sourcepath:
                for gdb in lyr_define.sourcepath[src_key]:
                    # print(gdb)
                    linux_gdb = ToLinuxPath(gdb)
                    shp_path_list.append(linux_gdb)
        return shp_path_list
    else:
        raster_files = []
        group_files = []
        for src_key in lyr_define.sourcepath:
            group_files.clear()
            if lyr_define.sourcetype.lower() == 'folder':
                for folder in lyr_define.sourcepath[src_key]:
                    linux_folder = ToLinuxPath(folder)
                    group_files = geoUtils.GetImgPaths(linux_folder)
                    raster_files.extend(group_files)
            else:
                for raster_path in lyr_define.sourcepath[src_key]:
                    linux_path = ToLinuxPath(raster_path)
                    linux_path = Link254Limit(service_define, linux_path)
                    group_files.append(linux_path)
                    raster_files.append(linux_path)

            if tindex:
                lyr_tIndex = os.path.join(tindex_dir, service_define.id + '_' + lyr_define.id + '_' + src_key + '.shp')
                CreateTIndex(lyr_tIndex, group_files)
                shp_path_list.append(lyr_tIndex)

        if tindex:
            return shp_path_list
        else:
            return raster_files


def ReplaceSameTemplate(service_def) -> tuple:
    '''创建服务配置文件，包括 mapfile,mapproxy yaml file 和 wsgi file
    :return service extent of geography, all mapproxy cache name, wsgi file path
    '''
    # 比较坐标系，如果同一图层下的坐标系不同，返回错误
    '''
    for lyr_def in service_def.layers:
        geo_data_paths = GetAllSources(service_def, lyr_def, False)

        if not geoUtils.CompareCoords(geo_data_paths):
            CLogger().info("geo datas in layer {0} have different spatialreference".format(lyr_def.id))
            raise Exception("geo datas in layer {0} have different spatialreference".format(lyr_def.id))

        del geo_data_paths
    '''

    # 配置文件路径
    yamlfile = os.path.join(application.xpath_one('data2service.yaml_dir', None), service_def.id + '.yaml')
    wsgifile = os.path.join(application.xpath_one('data2service.wsgi_dir', None), service_def.id + '.wsgi')

    temp_dir = os.path.join(basedir, 'template')
    with open(os.path.join(temp_dir, 'service_yaml_layer.txt'), 'r') as fp:
        service_yaml_lyr = fp.read()
    with open(os.path.join(temp_dir, 'service_yaml_cache.txt'), 'r') as fp:
        service_yaml_cache = fp.read()
    with open(os.path.join(temp_dir, 'service_yaml_source.txt'), 'r') as fp:
        service_yaml_source = fp.read()

    all_prjextent = []
    all_geoextent = []
    all_map_lyr_name = ''
    all_service_yaml_lyr = ''
    all_service_yaml_cache = ''
    all_service_yaml_source = ''
    all_service_yaml_cache_name = ''
    # 逐个图层处理
    for lyr_def in service_def.layers:
        cur_index = 0
        shp_path_list = GetAllSources(service_def, lyr_def, True)
        lyr_geoextent = []

        if len(shp_path_list) < 1:
            CLogger().info("no vector/raster in layer " + lyr_def.id)
            continue

        mapHelper = mapfileHelper.MapfileHelper()
        mapHelper.loads(os.path.join(basedir, "template/service_id.map"))
        mapHelper.setvalue("MAP.NAME", '"map_' + service_def.id + '_' + lyr_def.id + '"')

        # proj4 = geoUtils.GetProj4(shp_path_list[0])
        proj4 = "+proj=longlat +datum=WGS84 +no_defs"
        CLogger().info(proj4)
        proj4 = proj4.replace('+', '')
        map_prj = '\r\n'
        map_unit = 'dd'
        for defs in proj4.split():
            map_prj += '"' + defs + '"\n'
            if defs.startswith('unit') and defs.split('=')[-1] == 'm':
                map_unit = 'meters'
        map_prj += '\r\n'

        mapHelper.setvalue("MAP.UNITS", map_unit)
        mapHelper.setvalue("MAP.PROJECTION", map_prj)
        mapHelper.setvalue("MAP.WEB.METADATA.'WMS_TITLE'", 'map_' + service_def.id)

        ori_lyr = mapHelper.getvalue("MAP.LAYER.0")
        copy_lyr = copy.deepcopy(ori_lyr)

        for shp in shp_path_list:
            shp_prj = '\r\n'
            shp_proj4 = geoUtils.GetProj4(shp)
            shp_proj4 = shp_proj4.replace('+', '')
            for defs in shp_proj4.split():
                shp_prj += '"' + defs + '"\n'
            shp_prj += '\r\n'

            geoextent, prjextent = geoUtils.GetVectorExtent(shp)
            if prjextent == (0, 0, 0, 0):
                CLogger().info(shp + 'is null')
                continue

            geoextent = ExtendEnvlope(geoextent)
            all_prjextent.append(prjextent)
            all_geoextent.append(geoextent)
            lyr_geoextent.append(geoextent)

            # map layer
            if cur_index > 0:
                cur_lyr = copy.deepcopy(copy_lyr)
                mapHelper.setvalue("MAP.LAYER.{0}".format(cur_index), cur_lyr)

            base_name = lyr_def.id + str(cur_index)
            print(base_name)
            mapHelper.setvalue("MAP.LAYER.{0}.NAME".format(cur_index), u"'{0}'".format(base_name))
            mapHelper.setvalue("MAP.LAYER.{0}.METADATA.'WMS_TITLE'".format(cur_index), u"'{0}'".format(base_name))
            mapHelper.setvalue("MAP.LAYER.{0}.PROJECTION", shp_prj)
            # print(lyr_def.classidetify)
            if len(lyr_def.classidetify) > 10:
                json = CJson()
                json.load_json_text(lyr_def.classidetify)
                mapHelper.setvalue("MAP.LAYER.{0}.CLASS.0".format(cur_index), json.json_obj)

            if lyr_def.type.lower() == "vector":
                mapHelper.setvalue("MAP.LAYER.{0}.CONNECTION".format(cur_index), u"'{0}'".format(shp))
                mapHelper.setvalue("MAP.LAYER.{0}.CONNECTIONTYPE".format(cur_index), "OGR")
                mapHelper.setvalue("MAP.LAYER.{0}.TYPE".format(cur_index), "POLYGON")
                if lyr_def.sourcetype.lower() not in ["file", "folder"]:
                    mapHelper.setvalue("MAP.LAYER.{0}.DATA".format(cur_index), u"'{0}'".format(os.path.split(shp)[-1]))
            else:
                mapHelper.setvalue("MAP.LAYER.{0}.TILEINDEX".format(cur_index), u"'{0}'".format(shp))
                mapHelper.setvalue("MAP.LAYER.{0}.TYPE".format(cur_index), "RASTER")

            all_map_lyr_name = all_map_lyr_name + base_name + ','
            cur_index += 1

        if len(all_prjextent) < 1:
            continue

        # one layer one mapfile
        mapfile = os.path.join(application.xpath_one('data2service.map_dir', None), service_def.id + '_' + lyr_def.id + '.map')

        res_prjextent = geoUtils.UnionExt(all_prjextent)
        all_ext_prj = "{0} {1} {2} {3}".format(res_prjextent[0], res_prjextent[2], res_prjextent[1], res_prjextent[3])
        mapHelper.setvalue("MAP.EXTENT", all_ext_prj)
        mapHelper.dumps(mapfile)
        all_prjextent = []

        # yaml values
        if len(lyr_geoextent) < 1:
            continue
        lyr_cache_name = 'cache_' + lyr_def.id
        cache_source_name = 'source_' + lyr_def.id
        res_geoextent = geoUtils.UnionExt(lyr_geoextent)
        ext_yaml_lyr = "{0},{1},{2},{3}".format(res_geoextent[0], res_geoextent[2], res_geoextent[1], res_geoextent[3])
        all_service_yaml_cache_name = all_service_yaml_cache_name + lyr_cache_name + ','

        # yaml layer values
        yaml_lyr_values = dict({'$lyr_name$': lyr_def.id, '$lyr_cache$': lyr_cache_name})
        all_service_yaml_lyr = all_service_yaml_lyr + '\r\n' + RepString(service_yaml_lyr, yaml_lyr_values)

        # yaml cache values
        yaml_cache_values = dict({'$cache_source$': cache_source_name, '$lyr_cache$': lyr_cache_name,
                                  '$grids$': service_def.getGrids()})
        CLogger().info("the service grids are: " + service_def.getGrids())
        all_service_yaml_cache = all_service_yaml_cache + '\r\n' + RepString(service_yaml_cache, yaml_cache_values)

        # yaml source values
        all_map_lyr_name = all_map_lyr_name.rstrip(',')
        yaml_source_values = dict(
            {'$cache_source$': cache_source_name, '$map_file$': mapfile, '$lyr_name$': all_map_lyr_name,
             '$coverage_bbox$': ext_yaml_lyr})
        all_map_lyr_name = ''
        yaml_source_values['$server_bin$'] = application.xpath_one('data2service.service_yaml.server_bin', None)
        yaml_source_values['$server_dir$'] = application.xpath_one('data2service.service_yaml.server_dir', None)
        all_service_yaml_source = all_service_yaml_source + '\r\n' + RepString(service_yaml_source,
                                                                               yaml_source_values)

    # yaml
    yaml_cache_dir = application.xpath_one('data2service.service_yaml.cache_dir', None).replace('$orderid$', service_def.id)
    if not os.path.exists(yaml_cache_dir):
        os.makedirs(yaml_cache_dir)

    # yaml values
    yaml_values = dict({'$cache_dir$': yaml_cache_dir, '$yaml_layer$': all_service_yaml_lyr,
                        '$yaml_cache$': all_service_yaml_cache, '$yaml_source$': all_service_yaml_source})
    RepFile(os.path.join(basedir, "template/service_id.yaml"), yamlfile, yaml_values)

    # wsgi
    logfile = os.path.join(application.xpath_one('data2service.wsgi_dir', None), 'service_' + service_def.id + '.log')
    wsgivalues = dict({'$log_file$': logfile, '$yaml_file$': yamlfile})
    RepFile(os.path.join(sys.path[0], "template/service_id.wsgi"), wsgifile, wsgivalues)

    res_all_geoextent = geoUtils.UnionExt(all_geoextent)
    ext_yaml_lyr = "{0},{1},{2},{3}".format(res_all_geoextent[0], res_all_geoextent[2], res_all_geoextent[1],
                                            res_all_geoextent[3])
    return ext_yaml_lyr, all_service_yaml_cache_name.rstrip(','), wsgifile


def ProcessService(service_def):
    try:
        CLogger().info("start a service: " + service_def.id)

        repres = ReplaceSameTemplate(service_def)

        cache_area = application.xpath_one('data2service.seed_yaml.coverages', None).replace('$kid$', 'kall').replace('$seed_bbox$', repres[0])
        seedvalues = dict({'$refresh_time$': datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
                           '$cache_area$': cache_area, '$kn$': 'kall', '$all_cache$': repres[1],
                           '$grids$': service_def.getGrids()})
        seedfile = os.path.join(application.xpath_one('data2service.seed_dir', None), 'service_seed_' + service_def.id + '.yaml')
        RepFile(os.path.join(sys.path[0], "template/service_seed_id.yaml"), seedfile, seedvalues)

        qldfp = open(application.xpath_one('data2service.qld_conf.conf_path', None), 'r')
        qldcontent = qldfp.read()
        qldfp.close()

        wsgi_index = qldcontent.index('WSGIScriptAlias')
        wsgiscript = application.xpath_one('data2service.qld_conf.wsgi_script',
                                           None).replace("$aliasname$", service_def.id).replace('$wsgi_file$', repres[2])

        if "multiapp" not in application.xpath_one('data2service', None) \
                or application.xpath_one('data2service.multiapp', None) == "false":
            if wsgiscript not in qldcontent:
                resqld = qldcontent[0:wsgi_index] + wsgiscript + '\n' + qldcontent[wsgi_index:]
                qldfp = open(application.xpath_one('data2service.qld_conf.conf_path', None), 'w')
                qldfp.write(resqld)
                qldfp.close()
                CLogger().info("WSGIScriptAlias added")
                os.system("apachectl restart")

        CLogger().info(service_def.id + ' published\n')
    except Exception as ex:
        CLogger().info(str(ex))

