# -*- coding: utf-8 -*-

import argparse
import os
import sys
import urllib

PY3 = sys.version_info[0] >= 3
if PY3:
    import urllib.request

# 判断文件夹是否存在，若不存在则创建
def check_and_create_dir(file_name):
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
    if check_and_create_dir(file_name):
        f = open(file_name, 'w')
        f.write(text)
        f.close()
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''根据影像ID或数据集ID生成快视图，
    命令：python make_browser.py -i v14d12c8c656f47c1b1cc6d89e4ec1eb4 -t data -rf D:/test/test-img2wkt/error/xiandata80.json
    说明：
    data_id 数据或数据集的 object id
    type 可以是 data或dataset
    ''')
    parser.add_argument('-i', '--data_id', required=True, help='数据ID', dest='data_id')
    parser.add_argument('-rf', '--result_filename', required=True, help='输出文件', dest='result_filename')
    parser.add_argument('-t', '--type', required=True, help='数据类型', dest='type')

    args = parser.parse_args()
    
    
    make_url = "http://172.172.5.102:8082/service_api/MakeThumb?id={0}&type={1}"
    try:
        if PY3:
            res = urllib.request.urlopen(make_url.format(args.data_id, args.type))
        else:
            res = urllib.urlopen(make_url.format(args.data_id, args.type))
        res_content = res.read()
        res_content = str(res_content)
        res_code = res.getcode()
        
        if res_code == 200:
            print('success')
            write_output_file("{'result': -1, 'message': 'success'}", args.result_filename)
        else:
            print('error,{0}'.format(res_content))
            write_output_file("{'result': 0, 'message': 'error," + res_content + "'}", args.result_filename)
            
    except Exception as ex:
        write_output_file("{'result': 0, 'message': 'error," + str(ex) + "'}", args.result_filename)
        print('error,{0}'.format(ex))