# coding:utf-8
'''
@Author: zhangxx
@Date: 2020-02-19 14:14:42
@LastEditors: zhangxx
@LastEditTime: 2020-07-29 17:33:45
@Description: a python class to handle geo datasets
'''
import os

from osgeo import ogr, osr, gdal


# 获取shp文件四至，包括地理四至和投影四至
def GetShpExtent(shpname):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shpds = driver.Open(shpname, 0)
    layer = shpds.GetLayer(0)
    geoextent, prjextent = GetLayerExtent(layer)

    shpds.Destroy()
    del layer
    del driver
    return geoextent, prjextent


def GetVectorExtent(vector_path):
    if vector_path.endswith('.shp'):
        return GetShpExtent(vector_path)
    else:
        gdb_paths = os.path.split(vector_path)
        gdbds = ogr.Open(gdb_paths[0], 0)
        lyr = gdbds.GetLayerByName(str(gdb_paths[-1]))
        return GetLayerExtent(lyr)


def GetLayerExtent(layer):
    extent = layer.GetExtent()
    prj_wkt = layer.GetSpatialRef().ExportToWkt()

    rb = (0, 0)
    lu = (0, 0)
    if prj_wkt.strip() != "":
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(prj_wkt)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(prosrs, geosrs)
        rb = ct.TransformPoint(extent[1], extent[2])
        lu = ct.TransformPoint(extent[0], extent[3])
    else:
        rb = (extent[1], extent[2])
        lu = (extent[0], extent[3])

    return (lu[0], rb[0], rb[1], lu[1]), extent


def GetProj4(data_path):
    '''get geodata's SpatialReference, export to proj4 format
    '''
    # print(data_path)
    proj4_res = ''
    if str(data_path).endswith('.shp'):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        shpds = driver.Open(data_path, 0)
        layer = shpds.GetLayer(0)

        proj4_res = layer.GetSpatialRef().ExportToProj4()

        del layer
        shpds.Destroy()
        del driver
    elif ".gdb\\" in data_path or ".gdb/" in data_path:
        gdb_paths = os.path.split(data_path)
        gdbds = ogr.Open(gdb_paths[0], 0)
        layer = gdbds.GetLayerByName(str(gdb_paths[-1]))

        proj4_res = layer.GetSpatialRef().ExportToProj4()

        del layer
        gdbds.Destroy()
    else:
        imgds = gdal.Open(data_path, gdal.GA_ReadOnly)
        imgsrs = imgds.GetProjection()
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(imgsrs)
        proj4_res = prosrs.ExportToProj4()

        del imgds
    return proj4_res


def GetAllLocation(shp_path):
    raster_paths = []
    # 支持中文路径
    gdal.SetConfigOption('GDAL_FILENAME_IS_UTF8', 'YES')
    # 属性表支持中文
    gdal.SetConfigOption('SHAPE_ENCODING', 'UTF-8')

    shpds = ogr.Open(shp_path, 0)
    layer = shpds.GetLayerByIndex(0)
    total = layer.GetFeatureCount()

    for i in range(total):
        fea = layer.GetFeature(i)
        raster_paths.append(fea.GetFieldAsString('location'))

    shpds.Destroy()
    del layer
    return raster_paths


def GetPrjWkt(imgname):
    imgds = gdal.Open(imgname, gdal.GA_ReadOnly)
    imgsrs = imgds.GetProjection()

    del imgds
    return imgsrs


# 获取影像的分辨率、波段数和文件体积（以G为单位）
def GetImageResCountSize(imgname):
    filesize = os.path.getsize(imgname)/1024.0/1024.0/1024

    imgds = gdal.Open(imgname, gdal.GA_ReadOnly)
    bdcount = imgds.RasterCount
    geoTransform = imgds.GetGeoTransform(can_return_null=False)
    reso = geoTransform[1]

    prj_wkt = imgds.GetProjection()
    if prj_wkt.startswith('GEO'):
        reso = reso * 111.11 * 1000

    del imgds
    return reso, bdcount, filesize


def CompareCoords(src_array):
    '''param src_array: the array of geodatas, like shp, tif, gdb or other 
    Compare coordinates of the date source in src_array, if not same, return false
    '''
    if len(src_array) < 2:
        return True

    first_coor = GetProj4(src_array[0])
    cur_coor = ""
    for path in src_array:
        cur_coor = GetProj4(path)
        if cur_coor != first_coor:
            return False
    return True


def GetImageExtent(imgname):
    '''get geoextent,prjextent of image
    '''
    imgds = gdal.Open(imgname, gdal.GA_ReadOnly)
    geoTransform = imgds.GetGeoTransform(can_return_null = False)
    right=geoTransform[0] + imgds.RasterXSize*geoTransform[1] + imgds.RasterYSize*geoTransform[2]
    bottom=geoTransform[3] + imgds.RasterXSize*geoTransform[4] + imgds.RasterYSize*geoTransform[5]
    
    prj_wkt=imgds.GetProjection()
    
    rb=(0,0)
    lu=(0,0)
    if prj_wkt.strip() != "":
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(prj_wkt)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(prosrs, geosrs)
        rb = ct.TransformPoint(right, bottom)
        lu = ct.TransformPoint(geoTransform[0],geoTransform[3])
    else:
        rb=(right,bottom)
        lu=(geoTransform[0],geoTransform[3])
    
    del imgds
    return (lu[0],rb[0],rb[1],lu[1]),(geoTransform[0],right,bottom,geoTransform[3])


def IsExtIntersect(ext1,ext2):
    if (ext2[0]<ext1[0]<ext2[1] or ext2[0]<ext1[1]<ext2[1]) and (ext2[2]<ext1[2]<ext2[3] or ext2[2]<ext1[3]<ext2[3]):
        return True
    return False


def ExtUnion(ext1,ext2):
    xcoor=[ext1[0],ext1[1],ext2[0],ext2[1]]
    ycoor=[ext1[2],ext1[3],ext2[2],ext2[3]]
    
    return (min(xcoor),max(xcoor),min(ycoor),max(ycoor))


def UnionExt(allextent):
    unioned_ext=allextent[0]
    for ext in allextent:
        unioned_ext=ExtUnion(unioned_ext,ext)
        
    return unioned_ext


def UnionIntersectExt(allextent):
    refresh_geoms=[]
    for geom in allextent:
        unioned_index=[]
        if len(refresh_geoms)<1:
            refresh_geoms.append(geom)
        else:
            while(1):
                unioned=False
                for k,now_geom in enumerate(refresh_geoms):
                    if IsExtIntersect(now_geom,geom) or IsExtIntersect(geom,now_geom):
                        geom=ExtUnion(now_geom,geom)
                        unioned_index.append(k)
                        unioned=True
                for j in unioned_index:
                    refresh_geoms[j]=(0,0,0,0)
                if not unioned:
                    break
                
            refresh_geoms.append(geom)
    
    nnn=refresh_geoms.count((0,0,0,0))
    for i in range(nnn):
        refresh_geoms.remove((0,0,0,0))
    return refresh_geoms


# 获取一个文件夹下的所有img、tif影像
def GetImgPaths(input_dir):
    imgpaths=[]
    input_dir = input_dir.strip(';')

    if input_dir.lower().endswith('tif') or input_dir.lower().endswith('tiff') or input_dir.lower().endswith('img'):
        imgpaths.append(input_dir.split(';'))
        return imgpaths

    allsubs=os.listdir(input_dir)
    for sub in allsubs:
        if sub.lower().endswith(".img") or sub.lower().endswith(".tif") or sub.lower().endswith(".tiff"):
            imgpaths.append(os.path.join(input_dir,sub))
        elif os.path.isdir(os.path.join(input_dir,sub)):
            imgpaths.extend(GetImgPaths(os.path.join(input_dir,sub)))
    return imgpaths


def GetEncryImgPaths(dir):
    imgpaths=[]
    crypt="/vsicrypt/key_b64=oVzVUc4hGTF81fJPSsZy43j3dk7UYo8m2iskYOJGTDw=,file="
    allsubs=os.listdir(dir)
    for sub in allsubs:
        if sub.lower().endswith(".img") or sub.lower().endswith(".tif") or sub.lower().endswith(".tiff"):
            imgpaths.append(crypt + os.path.join(dir,sub))
        elif os.path.isdir(os.path.join(dir,sub)):
            imgpaths.extend(GetEncryImgPaths(os.path.join(dir,sub)))
    return imgpaths


def GetShpPaths(input_dir):
    shppaths=[]
    input_dir = input_dir.strip(';')

    if input_dir.endswith('.shp') :
        shppaths.extend(input_dir.split(';'))
        return shppaths

    allsubs=os.listdir(input_dir)
    for sub in allsubs:
        if sub.endswith(".shp") :
            shppaths.append(os.path.join(input_dir,sub))
        elif os.path.isdir(os.path.join(input_dir,sub)):
            shppaths.extend(GetShpPaths(os.path.join(input_dir,sub)))
    return shppaths