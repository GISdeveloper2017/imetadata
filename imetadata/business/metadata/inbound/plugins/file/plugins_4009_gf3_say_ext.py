# -*- coding: utf-8 -*-
# @Time : 2020/11/13 18:10
# @Author : 张源博
# @File : plugins_4009_gf3_say_ext.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf3_say_ext import \
    CSatFilePlugins_gf3_say_ext


class plugins_4009_gf3_say_ext(CSatFilePlugins_gf3_say_ext):
    pass


if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_4009_gf3_say_ext.FileType_File,
                            r'E:\测试数据\GF3_SAY_EXT_000230_E118.8_N38.7_20160825_L1A_HH_L10002015644.tiff',
                            r'E:\测试数据', '')
    # file_info = CFileInfoEx(plugins_4009_gf3_say_ext.FileType_Dir,
    #                         r'E:\测试数据\GF3_SAY_EXT_000230_E118.8_N38.7_20160825_L1A_HH_L10002015644',
    #                         r'E:\测试数据', '')

    plugins = plugins_4009_gf3_say_ext(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_4009_gf3_say_ext.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_4009_gf3_say_ext.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_4009_gf3_say_ext.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_4009_gf3_say_ext.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
