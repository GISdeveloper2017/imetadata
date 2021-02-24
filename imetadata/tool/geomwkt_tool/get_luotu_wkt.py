# coding:utf-8
import os
import sys
import time
import subprocess
from osgeo import ogr

def CreateLuotu(imgpath, wktpath):
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        exepath = os.path.join(basedir,"binX64\\BPDS_CutImageOutline.exe")
        
        shppath = wktpath.replace('.txt', '.shp')

        cmd = "{0} -src {1} -dst {2} -mode 0 -level 20 -WGS84".format(exepath, imgpath, shppath)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        # os.system(cmd)
        print('create luotu shapefile success')
        
        time.sleep(1)


        driver = ogr.GetDriverByName("ESRI Shapefile")
        shpds = driver.Open(shppath, 0)
        layer = shpds.GetLayer(0)

        if layer.GetFeatureCount() < 1:
            return False

        geo = layer.GetFeature(0).GetGeometryRef()
        geo = geo.Simplify(0.0001)
        wkt = geo.ExportToWkt()

        dstfp = open(wktpath, 'w')
        dstfp.write(wkt)
        dstfp.close()
        print('write luotu wkt success')
        return True
    except Exception as ex:
        print(ex.message)
        return False
    
    
if __name__ == "__main__":
    issuccess = CreateLuotu(sys.argv[1], sys.argv[2])
    if issuccess:
        sys.exit(0)
    else:
        sys.exit(1)