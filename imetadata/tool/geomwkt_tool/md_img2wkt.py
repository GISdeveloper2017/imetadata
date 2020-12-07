# -*- coding: utf-8 -*-

import os
import subprocess
import argparse
from osgeo import ogr
from osgeo import gdal


# 判断文件夹是否存在，若不存在则创建
def check_and_create_dir(file_name) -> bool:
    if os.path.exists(file_name):
        os.remove(file_name)
    (input_file_path, input_file_main_name) = os.path.split(file_name)

    try:
        if not os.path.exists(input_file_path):
            os.makedirs(input_file_path)
        return True
    except OSError as error:
        return False


# 将text写入文件
def write_output_file(text, file_name):
    if file_name is not None:
        if check_and_create_dir(file_name):
            f = open(file_name, 'w')
            f.write(text)
            f.close()


def process_bus(input_filename, output_filename, result_filename):
    try:
        # 检查输入文件
        if not os.path.exists(input_filename):
            write_output_file(u"{'result': 0, 'message': '输入文件不存在'}", result_filename)
            return False

        # 检查输出文件
        if not check_and_create_dir(output_filename):
            write_output_file(u"{'result': 0, 'message': '目标子目录[{0}]无法创建！'}".format(output_filename), result_filename)
            return False

        basedir = os.path.abspath(os.path.dirname(__file__))
        exe_path = os.path.join(basedir, "binX64\\BPDS_CutImageOutline.exe")
        shp_path = output_filename.replace('.wkt', '.shp')
        for ext in ['.shp', '.dbf', '.shx', '.prj']:
            tmp_path = shp_path.replace('.shp', ext)
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        cmd = '"{0}" -src "{1}" -dst "{2}" -mode 0 -level 7 -WGS84'.format(exe_path, input_filename, shp_path)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

        # 检查shp文件
        if not os.path.exists(shp_path):
            write_output_file(u"{'result': 0, 'message': 'shapefile:[{0}]出错！'}".format(shp_path), result_filename)
            return False

        # 注册所有驱动
        ogr.RegisterAll()
        # 支持中文路径
        gdal.SetConfigOption('GDAL_FILENAME_IS_UTF8', 'YES')
        # 属性表支持中文
        gdal.SetConfigOption('SHAPE_ENCODING', 'gbk')

        # 打开shp文件
        shpds = ogr.Open(shp_path, 0)
        if shpds is None:
            write_output_file(u"{'result': 0, 'message': '打开shp文件失败！'}", result_filename)
            return False

        # 获取该数据源的图层（shp文件只有一个图层）
        layer = shpds.GetLayer(0)
        if layer.GetFeatureCount() < 1:
            write_output_file(u"{'result': 0, 'message': '该图层不存在！'}", result_filename)
            return False

        # 获取图层要素
        fea = layer.GetFeature(0)
        if fea is None:
            write_output_file(u"{'result': 0, 'message': '获取要素失败！'}", result_filename)
            return False

        # 获取几何多边形
        geo = fea.GetGeometryRef()
        if geo is None:
            write_output_file(u"{'result': 0, 'message': '获取多边形失败！'}", result_filename)
            return False

        # 抽希
        geo = geo.Simplify(0.0001)
        if geo is None:
            write_output_file(u"{'result': 0, 'message': '多边形抽希失败！'}", result_filename)
            return False

        # wkt转化
        wkt = geo.ExportToWkt()
        if wkt is None:
            write_output_file(u"{'result': 0, 'message': '转化wkt失败！'}", result_filename)
            return False

        dstfp = open(output_filename, 'w')
        dstfp.write(wkt)
        dstfp.close()
        write_output_file(u"{'result': -1, 'message': '数据处理成功！'}", result_filename)
        return True
    except Exception as error:
        write_output_file(u"{'result': 0, 'message': '算法计算过程出现错误！'}", result_filename)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
将指定的影像提取边界矢量，并转换为wkt
作者：张源博
日期：2020/9/3

命令:
D:/App/QGIS/bin/python-qgis.bat  D:/PycharmWork/project1/get_Luotu/md_img2wkt.py
-i D:/test/test-img2wkt/xiandata80.img -o D:/test/test-img2wkt/wkt/xiandata80.wkt -rf D:/test/test-img2wkt/error/xiandata80.json

说明：
1.input_filename: 待转换的img文件
2.output_filename: 转换的目标文件名，扩展名为wkt，同时生成的临时文件shp，放在与wkt相同的目录下
3.result_filename: 转换的成功或失败信息, json格式

依赖

    """)
    parser.add_argument('-i', '--input_filename', required=True, help='输入文件', dest='input_filename')
    parser.add_argument('-rf', '--result_filename', required=True, help='输出文件', dest='result_filename')
    parser.add_argument('-o', '--output_filename', required=True, help='输出文件', dest='output_filename')

    args = parser.parse_args()

    process_bus(args.input_filename, args.output_filename, args.result_filename)
