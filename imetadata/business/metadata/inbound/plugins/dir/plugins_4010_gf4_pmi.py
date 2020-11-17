# -*- coding: utf-8 -*-
# @Time : 2020/11/10 13:10
# @Author : 张源博
# @File : plugins_4010_gf4_pmi.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf4_pmi import CSatFilePlugins_gf4_pmi


class plugins_4010_gf4_pmi(CSatFilePlugins_gf4_pmi):
    pass


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_4010_gf4_pmi.FileType_File,
    #                         r'E:\测试数据\GF4_PMS_E115.0_N36.6_20160803_L1A0000125813.tiff',
    #                         r'E:\测试数据', '')
    file_info = CFileInfoEx(plugins_4010_gf4_pmi.FileType_Dir,
                            r'E:\测试数据\GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VV_L10002039504',
                            r'E:\测试数据', '')

    plugins = plugins_4010_gf4_pmi(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_4010_gf4_pmi.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_4010_gf4_pmi.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_4010_gf4_pmi.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_4010_gf4_pmi.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
