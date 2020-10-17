# -*- coding: utf-8 -*- 
# @Time : 2020/10/13 17:02
# @Author : 赵宇飞
# @File : plugins_1012_dem_12.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu_bus import CFilePlugins_GUOTU_BUS


class plugins_1012_dem_12(CFilePlugins_GUOTU_BUS):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DEM数据'
        information[self.Plugins_Info_Name] = 'dem_12'

        return information

    def classified(self):
        """
        设计国土行业数据的dem_12验证规则
        todo 负责人 邢凯凯 在这里检验dem_12的元数据文件格式时, 应该一个一个类型的对比, 找到文件时, 将该文件的格式和文件名存储到类的私有属性中, 以便在元数据处理时直接使用
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__

        check_file_main_name_length = len(file_main_name) == 12
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        file_metadata_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
        # check_file_metadata_name_exist = \
        #     CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xls')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xlsx')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mat')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mdb'))

        # 记录业务元数据文件全文件名及后缀名
        check_file_metadata_name_exist = False
        ext_list = ['xls', 'xlsx', 'mat', 'mdb']
        for ext in ext_list:
            temp_metadata_bus_file = '{0}.{1}'.format(file_metadata_name_with_path, ext)
            if CFile.file_or_path_exist(temp_metadata_bus_file):
                check_file_metadata_name_exist = True
                self._metadata_bus_file_ext = ext
                self._metadata_bus_file_with_path = temp_metadata_bus_file
                break

        if not check_file_metadata_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'tif'))

        if not check_file_main_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第2、3位是数字
        下面判别第5-8位是数字
        下面判别第9-12位是数字
        """
        char_1 = file_main_name[0:1]
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_8 = file_main_name[4:8]
        char_9_to_12 = file_main_name[8:12]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_8) is False \
                or CUtils.text_is_numeric(char_9_to_12) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        if CUtils.equal_ignore_case(file_ext, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 赵宇飞 在这里将dem_12的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        metadata_xml_file_name = CFile.join_file(self.file_content.content_root_dir,
                                                 '{0}.xml'.format(self.classified_object_name()))
        # if not CFile.file_or_path_exist(metadata_xml_file_name):
        return CResult.merge_result(self.Failure, '元数据文件[{0}]不存在, 无法解析! '.format(metadata_xml_file_name))

        # try:
        #     parser.metadata.set_metadata_bus_file(self.MetaDataFormat_XML, metadata_xml_file_name)
        #     return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(metadata_xml_file_name))
        # except:
        #     parser.metadata.set_metadata_bus(self.MetaDataFormat_Text, '')
        #     return CResult.merge_result(self.Exception,
        #                                        '元数据文件[{0}]格式不合法, 无法处理! '.format(metadata_xml_file_name))


if __name__ == '__main__':
    file_info = CFileInfoEx(plugins_1012_dem_12.FileType_File,
                            r'E:\python数管\数据入库3\dem\G49G00103016\G49G00103016.tif',
                            r'E:\python数管\数据入库3\dem', '<root><type>dem</type></root>')
    plugins = plugins_1012_dem_12(file_info)
    object_confirm, object_name = plugins.classified()
    if object_confirm == plugins_1012_dem_12.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_1012_dem_12.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_1012_dem_12.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_1012_dem_12.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
