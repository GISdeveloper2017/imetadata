# coding:utf-8
import os
import sys
from osgeo import ogr, gdal, osr
import urllib
import logging
import geoUtils
import sqlHelp
import mapfileHelper

PY3 = sys.version_info[0] >= 3
if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')


basedir = os.path.abspath(os.path.dirname(__file__))
dbConfig = {"database":"atplatform3", "user":"postgres", "password":"postgres", "host":"172.172.5.218", "port":"5432"}
png_suffix = "_thumb.png"
mapfile_suffix = "_thumb.map"
tindex_suffix = "_thumb.shp"
map_dir = '/home/geocube/map/mapfile'
tindex_dir = '/home/geocube/map/tileIndex'
png_dir = '/mnt/thumb'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename=os.path.join(basedir, 'makethumb.log'), filemode='a')


def ToLinuxPath(src_path):
    linux_path = src_path
    linux_path = linux_path.replace('\\', '/').replace('//', '/')
    return linux_path


def CreateTIndex(shpname, imgpaths):
    print('img files count:' + str(len(imgpaths)))
    logging.info('img files count:' + str(len(imgpaths)))

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
    nMaxFieldSize = 254
    tile_index_field = ogr.FieldDefn("location", ogr.OFTString)
    tile_index_field.SetWidth(nMaxFieldSize)
    lyr.CreateField(tile_index_field)

    srs_field = ogr.FieldDefn("src_srs", ogr.OFTString)
    srs_field.SetWidth(nMaxFieldSize)
    lyr.CreateField(srs_field)

    del lyr
    tindex_ds.Destroy()
    del driver

    cmd = r'gdaltindex -src_srs_name src_srs -write_absolute_path {0} {1}'
    if len(imgpaths) > 500:
        cnt = len(imgpaths) / 500
        for kk in range(cnt):
            raster_file = ' '.join(imgpaths[kk * 500 : (kk + 1) * 500 -1])
            os.system(cmd.format(shpname, raster_file))
        raster_file = ' '.join(imgpaths[cnt * 500 : ])
        os.system(cmd.format(shpname, raster_file))
    else:
        os.system(cmd.format(shpname, raster_file))

    print('created tileIndex: ' + shpname)
    logging.info('created tileIndex: ' + shpname)


def CreateMapfile(img_paths, name):
    # check exists
    mapfile_path = os.path.join(map_dir, name + mapfile_suffix)
    if len(img_paths) == 1 and os.path.exists(mapfile_path):
        return mapfile_path

    # create tileIndex
    tindex_shp = os.path.join(tindex_dir, name + tindex_suffix)
    CreateTIndex(tindex_shp, img_paths)

    mapHelper = mapfileHelper.MapfileHelper()
    mapHelper.loads(os.path.join(sys.path[0], "template/service_id.map"))
    mapHelper.setvalue("MAP.NAME", '"map_' + name + '"')

    proj4 = geoUtils.GetProj4(img_paths[0])
    print(proj4)
    logging.info(proj4)
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
    mapHelper.setvalue("MAP.WEB.METADATA.'WMS_TITLE'", 'map_' + name)

    mapHelper.setvalue("MAP.LAYER.0.NAME", u"'{0}'".format(name))
    mapHelper.setvalue("MAP.LAYER.0.METADATA.'WMS_TITLE'", u"'{0}'".format(name))
    mapHelper.setvalue("MAP.LAYER.0.TILEINDEX", u"'{0}'".format(tindex_shp))
    mapHelper.setvalue("MAP.LAYER.0.TYPE", "RASTER")

    res_geoextent, res_prjextent = geoUtils.GetShpExtent(tindex_shp)
    all_ext_prj = "{0} {1} {2} {3}".format(res_prjextent[0], res_prjextent[2], res_prjextent[1], res_prjextent[3])
    mapHelper.setvalue("MAP.EXTENT", all_ext_prj)

    # set map png width and height
    width = 1000
    height = width * (res_prjextent[3] - res_prjextent[2]) / (res_prjextent[1] - res_prjextent[0])
    height = int(height)
    mapHelper.setvalue("MAP.SIZE", "{0} {1}".format(width, height))
    mapHelper.dumps(mapfile_path)

    return mapfile_path


def MakeThumb(img_ids, png_name):
    linux_image_path = []
    # connect to database
    print (dbConfig)
    sqlhelper = sqlHelp.SQLHelp(dbConfig["host"], dbConfig["port"],
                                dbConfig["database"], dbConfig["user"],
                                dbConfig["password"])

    # search images with img_ids
    ori_image_paths = []
    sql_img_ids = img_ids.replace(';', ',').rstrip(',')
    sql_img_ids = "'" + sql_img_ids.replace(',',"','") + "'"
    # if sql_img_ids.count(',') <= 1:
    #     png_name = sql_img_ids + '_thumb.png'
    # else:
    #     png_name = png_name + '_thumb.png'

    img_sql = "select dps_object_fullname from view_dm2_object_dirandfile where dps_object_id in ({0})".format(sql_img_ids)
    print(img_sql)
    logging.info(img_sql)
    img_sql_res = sqlhelper.getRows(img_sql)
    for row in img_sql_res:
        ori_image_paths.append(row[0])

    # replace win path with linux path
    path_rep = dict()
    path_pair_sql = "select dstunipath,mounturl1 from dm2_storage where status = '1'"
    path_sql_res = sqlhelper.getRows(path_pair_sql)
    for row in path_sql_res:
        path_rep[row[0]] = row[1]

    for path in ori_image_paths:
        for pk in path_rep:
            if pk in path:
                linux_image_path.append(ToLinuxPath(path.replace(pk, path_rep[pk])))
                logging.info(ToLinuxPath(path.replace(pk, path_rep[pk])))
                break

    # create tileIndex and mapfile
    mapfile = CreateMapfile(linux_image_path, png_name)

    # create png
    thumb_url = "http://172.172.5.102:8082/cgi-bin/mapserv?map={0}&mode=map&layers=all"
    res_png = os.path.join(png_dir, png_name + png_suffix)

    rsp = urllib.urlopen(thumb_url.format(mapfile))
    img = rsp.read()
    with open(res_png, 'wb') as f:
        f.write(img)
    sqlhelper.closeconn()


if __name__ == "__main__":
    logging.info(" ".join(sys.argv))
    if len(sys.argv) < 3:
        print("Error:wrong argv")
        logging.error("Error:wrong argv " + ' '.join(sys.argv))
        sys.exit(1)

    MakeThumb(sys.argv[1], sys.argv[2])
