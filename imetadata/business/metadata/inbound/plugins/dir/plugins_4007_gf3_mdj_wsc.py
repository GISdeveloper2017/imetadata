# -*- coding: utf-8 -*- 
# @Time : 2020/11/6 10:46 
# @Author : 邢凯凯
# @File : plugins_4007_gf3_mdj_wsc.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf3_mdj_wsc import \
    CSatFilePlugins_gf3_mdj_wsc


class plugins_4007_gf3_mdj_wsc(CSatFilePlugins_gf3_mdj_wsc):
    pass


if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_4007_gf3_mdj_wsc.FileType_File,
                            'E:\测试数据\GF3_mdj_WSC_000823_E122.8_N39.8_20161005_L1A_hh_L10002039504_strip_0.tiff',
                            'E:\测试数据', '')

    #    file_info = CFileInfoEx(plugins_6006_gf3_kas_wsc.FileType_Dir,
    #                            'E:\测试数据\GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VV_L10002039504',
    #                            'E:\测试数据', '')
    plugins = plugins_4007_gf3_mdj_wsc(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_4007_gf3_mdj_wsc.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_4007_gf3_mdj_wsc.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_4007_gf3_mdj_wsc.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_4007_gf3_mdj_wsc.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
