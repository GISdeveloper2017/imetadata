from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_gf1_B_C_D import CSatFilePlugins_gf1_B_C_D


class plugins_2005_gf1_B_C_D(CSatFilePlugins_gf1_B_C_D):
    pass

if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_2005_gf1_B_C_D.FileType_Dir,
                            '/Users/wangxiya/Documents/交换/1.给我的/GF1/GF1B_PMS_E85.9_N44.1_20140821_L1A0000311315',
                            '/Users/wangxiya/Documents/交换', '')
    plugins = plugins_2005_gf1_B_C_D(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_2005_gf1_B_C_D.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_2005_gf1_B_C_D.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_2005_gf1_B_C_D.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_2005_gf1_B_C_D.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))