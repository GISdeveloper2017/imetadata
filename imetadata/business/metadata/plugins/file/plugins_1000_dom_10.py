# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 16:45 
# @Author : 王西亚 
# @File : plugins_1000_dom_10.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class plugins_1000_dom_10(CFilePlugins_GUOTU):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_10'

        return information

    def get_classified_metadata_rule_type(self):
        """
        设置需要提前验证的元数据规则类型
        :return:
        """
        return self.MetaData_Rule_Type_DOM

    def classified_by_character_guotu(self):
        file_main_name = self.__file_info__.__file_main_name__
        file_ext = self.__file_info__.__file_ext__

        check_file_main_name_length = len(file_main_name) == 10
        if not check_file_main_name_length:
            return self.__object_confirm__, self.Object_Confirm_IUnKnown

        file_metadata_name_with_path = CFile.join_file(self.__file_info__.__file_path__, file_main_name)
        check_file_metadata_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xls')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xlsx')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mat')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mdb'))

        if not check_file_metadata_name_exist:
            return self.__object_confirm__, self.Object_Confirm_IUnKnown

        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'tif'))

        if not check_file_main_name_exist:
            return self.__object_confirm__, self.Object_Confirm_IUnKnown

        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第8910位是数字
        """

        if CUtils.equal_ignore_case(file_ext, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__


if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
                            '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
                            '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    plugins = plugins_1000_dom_10(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_1000_dom_10.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_1000_dom_10.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_1000_dom_10.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_1000_dom_10.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
