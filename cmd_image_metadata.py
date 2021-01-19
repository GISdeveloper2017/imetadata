# -*- coding: utf-8 -*- 
# @Time : 2021/1/20 00:17 
# @Author : 王西亚 
# @File : cmd_image_metadata.py
# -*- coding: utf-8 -*-

import os
import argparse
from urllib import parse

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.tool.mdreader.raster.c_rasterMDReader import CRasterMDReader


def escape_arg(value):
    result = '{}'.format(value)
    return parse.unquote(result)


def write_output_file(text, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    (input_file_path, input_file_main_name) = os.path.split(file_name)

    try:
        if not os.path.exists(input_file_path):
            os.makedirs(input_file_path)
    except OSError as error:
        print(u"{'result': 0, 'message': '目录%s无法创建！'}" % input_file_path)
        return

    f = open(file_name, 'w')
    f.write(text)
    f.close()


def process_bus(input_filename, output_filename, result_filename):
    try:
        CResult.to_file(CRasterMDReader(input_filename).get_metadata_2_file(output_filename), result_filename)
    except Exception as error:
        write_output_file(u"{'result': 0, 'message': '算法计算过程出现错误！'}", result_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input_filename', required=True, help='输入文件', dest='input_filename')
    parser.add_argument('-rf', '--result_filename', required=True, help='输入文件', dest='result_filename')

    parser.add_argument('-o', '--output_filename', required=True, help='输出文件', dest='output_filename')

    args = parser.parse_args()

    application_dir = CFile.file_path(CFile.file_abs_path(__file__))
    application_name = CFile.file_main_name(application_dir)
    settings.application.set_app_information(application_dir, application_name)
    process_bus(args.input_filename, args.output_filename, args.result_filename)
