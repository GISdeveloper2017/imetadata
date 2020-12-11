# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 10:25 
# @Author : 王西亚 
# @File : c_doc.py

from tikapp import TikaApp

tika_client = TikaApp(file_jar="/usr/local/Cellar/tika/1.24.1_1/libexec/tika-app-1.24.1.jar")
metadata = tika_client.extract_only_metadata("/Users/wangxiya/Downloads/000101020062805119-00.pdf")
print(type(metadata))
print(metadata)

# from tika import parser

# parsed = parser.from_file('/path/to/file')
# print(parsed["metadata"])
# print(parsed["content"])

# parsed = parser.from_file('/Users/wangxiya/Downloads/000101020062805119-00.pdf', 'http://localhost:9998/tika')
# metadata = parsed["metadata"]
# print(type(metadata))
# print(metadata)
