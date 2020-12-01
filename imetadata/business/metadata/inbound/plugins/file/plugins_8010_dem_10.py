# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 16:45 
# @Author : 王西亚 
# @File : plugins_8010_dem_10.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dem import CFilePlugins_GUOTU_DEM


class plugins_8010_dem_10(CFilePlugins_GUOTU_DEM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DEM_分幅'
        # information[self.Plugins_Info_Name] = 'dem_10'
        return information

    def classified(self):
        """
        设计国土行业数据的dom-10验证规则
        完成 负责人 李宪 在这里检验dem-10的元数据文件格式时, 应该一个一个类型的对比, 找到文件时, 将该文件的格式和文件名存储到类的私有属性中, 以便在元数据处理时直接使用
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext

        check_file_main_name_length = len(file_main_name) == 10
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self._object_name

        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_main_name)
        check_file_main_name_exist_tif = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))
        check_file_main_name_exist_bil = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Bil))
        if (not check_file_main_name_exist_tif) and (not check_file_main_name_exist_bil):
            return self.Object_Confirm_IUnKnown, self._object_name
        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第8910位是数字
        """
        char_1 = file_main_name[0:1]
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_10 = file_main_name[7:10]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_7) is False \
                or CUtils.text_is_numeric(char_8_to_10) is False:
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
    file_info = CFileInfoEx(plugins_8010_dem_10.FileType_File,
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\G49G001031\G49G001031.bil',
                            r'D:\迅雷下载\数据入库3\DEM\造的数据TIF\G49G001031\bil', '<root><type>dem</type></root>')
    plugins = plugins_8010_dem_10(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_8010_dem_10.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_8010_dem_10.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_8010_dem_10.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_8010_dem_10.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
