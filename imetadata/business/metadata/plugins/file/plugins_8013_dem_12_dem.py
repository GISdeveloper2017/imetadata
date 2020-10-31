# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:18
# @Author : 赵宇飞
# @File : plugins_8013_dem_12_dem.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dem import CFilePlugins_GUOTU_DEM


class plugins_8013_dem_12_dem(CFilePlugins_GUOTU_DEM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DEM数据'
        information[self.Plugins_Info_Name] = 'dem_12_dem'

        return information

    def classified(self):
        """
        设计国土行业数据的dem_12_dem验证规则
        todo 负责人 李宪 在这里检验dem_12_dem的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__

        check_file_main_name_length = len(file_main_name) == 15
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self._object_name

        file_main_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
        check_file_main_name_exist_tif = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))
        check_file_main_name_exist_bil = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Bil))
        if (not check_file_main_name_exist_tif) and (not check_file_main_name_exist_bil):
            return self.Object_Confirm_IUnKnown, self._object_name
        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第89101112位是数字
        下面判别第131415位是DOM
        """
        char_1 = file_main_name[0:1]
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_12 = file_main_name[7:12]
        char_13_to_15 = file_main_name[12:15]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_7) is False \
                or CUtils.text_is_numeric(char_8_to_12) is False \
                or CUtils.equal_ignore_case(char_13_to_15, "DEM") is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) \
                or CUtils.equal_ignore_case(file_ext, self.Name_Bil):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_8013_dem_12_dem.FileType_File,
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\G49G00103121DEM\G49G00103121DEM.tif',
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\G49G00103121DEM\tif', '<root><type>dem</type></root>')
    plugins = plugins_8013_dem_12_dem(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_8013_dem_12_dem.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_8013_dem_12_dem.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_8013_dem_12_dem.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_8013_dem_12_dem.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))