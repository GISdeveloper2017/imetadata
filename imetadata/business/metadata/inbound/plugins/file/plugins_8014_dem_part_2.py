# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:23
# @Author : 赵宇飞
# @File : plugins_8014_dem_part_2.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dem import CFilePlugins_GUOTU_DEM


class plugins_8014_dem_part_2(CFilePlugins_GUOTU_DEM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DEM数据'
        information[self.Plugins_Info_Name] = 'dem_part_2'

        return information

    def classified(self):
        """
        设计国土行业数据的dem_part_2验证规则
        完成 负责人 李宪 在这里检验dem_part_2的识别规则
        :return:
        """
        super().classified()
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        check_file_main_name_exist_tif = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))
        check_file_main_name_exist_bil = CFile.file_or_path_exist(
            '{0}.{1}'.format(file_main_name_with_path, self.Name_Bil))
        if (not check_file_main_name_exist_tif) and (not check_file_main_name_exist_bil):
            return self.Object_Confirm_IUnKnown, self._object_name

        # 判断是否有‘-’，并且为一个
        if not self.file_info.file_main_name.count('-') == 1:
            return self.Object_Confirm_IUnKnown, self._object_name

        char_1 = self.file_info.file_main_name.split('-')[0]
        char_2 = self.file_info.file_main_name.split('-')[1]
        # char_1,char_2是否小数
        if CUtils.text_is_decimal(char_1) is False \
                or CUtils.text_is_decimal(char_2) is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        if CUtils.equal_ignore_case(self.file_info.file_ext, self.Name_Tif) \
                or CUtils.equal_ignore_case(self.file_info.file_ext, self.Name_Bil):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_main_name
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        return self._object_confirm, self._object_name


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_8014_dem_part_2.FileType_File,
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\6369.0-796.0\6369.0-796.0.tif',
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\6369.0-796.0\tif', '<root><type>dem</type></root>')
    plugins = plugins_8014_dem_part_2(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_8014_dem_part_2.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_8014_dem_part_2.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_8014_dem_part_2.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_8014_dem_part_2.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
