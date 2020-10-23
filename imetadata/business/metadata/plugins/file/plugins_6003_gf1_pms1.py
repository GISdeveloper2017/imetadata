# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 09:54 
# @Author : 王西亚 
# @File : plugins_6003_gf1_pms1.py.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf1_pms1 import CSatFilePlugins_gf1_pms1


class plugins_6003_gf1_pms1(CSatFilePlugins_gf1_pms1):
    pass


if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_6003_gf1_pms1.FileType_File,
                            '/Users/wangxiya/Documents/交换/1.给我的/GF1/GF1_PMS1_E85.9_N44.1_20140821_L1A0000311315.tar.gz',
                            '/Users/wangxiya/Documents/交换', '')
    plugins = plugins_6003_gf1_pms1(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_6003_gf1_pms1.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_6003_gf1_pms1.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_6003_gf1_pms1.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_6003_gf1_pms1.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
