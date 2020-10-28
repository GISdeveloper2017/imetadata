# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:11
# @Author : 赵宇飞
# @File : plugins_1004_dom_part_2.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dom import CFilePlugins_GUOTU_DOM


class plugins_1004_dom_part_2(CFilePlugins_GUOTU_DOM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_part_2'

        return information

    def classified(self):
        """
        设计国土行业数据的dom_part_2验证规则
        todo 负责人 李宪 在这里检验dom_part_2的识别规则
        :return:
        """
        super().classified()
        file_main_name_with_path = CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__)
        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, 'tif'))
        if not check_file_main_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        if not self.file_info.__file_main_name__.count('-') == 1:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        char_1 = self.file_info.__file_main_name__.split('-')[0]
        char_2 = self.file_info.__file_main_name__.split('-')[1]
        if CUtils.text_is_decimal(char_1) is False \
                or CUtils.text_is_decimal(char_2) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        if CUtils.equal_ignore_case(self.file_info.__file_ext__, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = self.file_info.__file_main_name__
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None
        return self.__object_confirm__, self.__object_name__

if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_1004_dom_part_2.FileType_File,
                            r'D:\迅雷下载\数据入库1\DOM\广西影像数据\2772.0-509.0\2772.0-509.0.tif',
                            r'D:\迅雷下载\数据入库1\DOM\广西影像数据\2772.0-509.0\tif', '<root><type>dom</type></root>')
    plugins = plugins_1004_dom_part_2(file_info)
    object_confirm, object_name = plugins.classified()
    plugins.init_qa_file_list(file_info)
    if object_confirm == plugins_1004_dom_part_2.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
