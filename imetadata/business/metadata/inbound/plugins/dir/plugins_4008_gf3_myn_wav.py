# -*- coding: utf-8 -*-
# @Time : 2020/11/13 18:08
# @Author : 张源博
# @File : plugins_4008_gf3_myn_wav.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf3_myn_wav import \
    CSatFilePlugins_gf3_myn_wav


class plugins_4008_gf3_myn_wav(CSatFilePlugins_gf3_myn_wav):
    pass


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_4008_gf3_myn_wav.FileType_File,
    #                         r'E:\测试数据\GF3_MYN_WAV_001009_E107.9_N39.6_20161018_L1A_HH_L10001906059.tiff',
    #                         r'E:\测试数据', '')
    file_info = CFileInfoEx(plugins_4008_gf3_myn_wav.FileType_Dir,
                            r'E:\测试数据\GF3_MYN_WAV_001009_E107.9_N39.6_20161018_L1A_AHV_L10001906059',
                            r'E:\测试数据', '')

    plugins = plugins_4008_gf3_myn_wav(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_4008_gf3_myn_wav.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_4008_gf3_myn_wav.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_4008_gf3_myn_wav.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_4008_gf3_myn_wav.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
