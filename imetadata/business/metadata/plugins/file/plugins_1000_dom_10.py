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
            return self.Object_Confirm_IUnKnown, self.__object_name__

        file_metadata_name_with_path = CFile.join_file(self.__file_info__.__file_path__, file_main_name)
        check_file_metadata_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xls')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xlsx')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mat')) \
            or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mdb'))

        if not check_file_metadata_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'tif'))

        if not check_file_main_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第8910位是数字
        """
        char_1 = file_main_name[0:1]
        char_4 = file_main_name[3:4]
        char_2_3 = file_main_name[1:3]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_10 = file_main_name[7:10]
        if self.check_is_alapha(char_1) == False \
            or self.check_is_alapha(char_4) == False \
            or self.check_is_numeric(char_2_3) == False \
            or self.check_is_numeric(char_5_to_7) == False \
            or self.check_is_numeric(char_8_to_10) == False:
            return self.Object_Confirm_IUnKnown, self.__object_name__


        if CUtils.equal_ignore_case(file_ext, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def check_is_numeric(self, check_str: str) -> bool:
        '''
            判断是否为数字
        '''
        return check_str.isdigit()

    def check_is_alapha(self, check_str: str) -> bool:
        '''
            判断是否字母
        '''
        return check_str.isalpha()

    '''
        python3判断字符串是字母/数字/大小写的系统函数：
        函数	                含义
        字符串.isalnum()	所有字符都是数字或者字母，为真返回 Ture，否则返回 False。
        字符串.isalpha() 所有字符都是字母，为真返回 Ture，否则返回 False。
        字符串.isdigit() 所有字符都是数字，为真返回 Ture，否则返回 False。
        字符串.islower()	所有字符都是小写，为真返回 Ture，否则返回 False。
        字符串.isupper()	所有字符都是大写，为真返回 Ture，否则返回 False。
        字符串.istitle()	所有单词都是首字母大写，为真返回 Ture，否则返回 False。
        字符串.isspace()	所有字符都是空白字符，为真返回 Ture，否则返回 False。
    '''

if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
                            r'D:\data\tif\wsiearth_H49G001026\H49G001026.tif',
                            r'D:\data\tif', '<root><type>dom</type></root>')
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
