# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 16:45 
# @Author : 王西亚 
# @File : plugins_1000_dom_10.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerDOM import CMDTransformerDOM
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dom import CFilePlugins_GUOTU_DOM


class plugins_1000_dom_10(CFilePlugins_GUOTU_DOM):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_10'

        return information

    def classified(self):
        """
        设计国土行业数据的dom-10验证规则
        todo 负责人 赵宇飞 在这里检验dom-10的元数据文件格式时, 应该一个一个类型的对比, 找到文件时, 将该文件的格式和文件名存储到类的私有属性中, 以便在元数据处理时直接使用
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__

        check_file_main_name_length = len(file_main_name) == 10
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        file_metadata_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
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
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_10 = file_main_name[7:10]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_7) is False \
                or CUtils.text_is_numeric(char_8_to_10) is False:
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
        todo 负责人 王学谦 在这里将dom-10的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        transformer = CMDTransformerDOM(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return []


if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
                            r'D:\data\tif\wsiearth_H49G001026\H49G001026.tif',
                            r'D:\data\tif', '<root><type>dom</type></root>')
    plugins = plugins_1000_dom_10(file_info)
    # object_confirm, object_name = plugins.classified()
    # if object_confirm == plugins_1000_dom_10.Object_Confirm_IUnKnown:
    #     print('对不起, 您给你的文件, 我不认识')
    # elif object_confirm == plugins_1000_dom_10.Object_Confirm_IKnown_Not:
    #     print('您给你的文件, 我确认它不是对象')
    # elif object_confirm == plugins_1000_dom_10.Object_Confirm_IKnown:
    #     print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    # elif object_confirm == plugins_1000_dom_10.Object_Confirm_Maybe:
    #     print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
