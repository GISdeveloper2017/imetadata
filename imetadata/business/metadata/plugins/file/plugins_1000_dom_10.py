# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 16:45 
# @Author : 王西亚 
# @File : plugins_1000_dom_10.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu_bus import CFilePlugins_GUOTU_BUS


class plugins_1000_dom_10(CFilePlugins_GUOTU_BUS):
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
        # check_file_metadata_name_exist = \
        #     CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xls')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'xlsx')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mat')) \
        #     or CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'mdb'))

        # 记录业务元数据文件全文件名及后缀名
        # check_file_metadata_name_exist = False
        # ext_list = ['xls', 'xlsx', 'mat', 'mdb']
        # for ext in ext_list:
        #     temp_metadata_bus_file = '{0}.{1}'.format(file_metadata_name_with_path, ext)
        #     if CFile.file_or_path_exist(temp_metadata_bus_file):
        #         check_file_metadata_name_exist = True
        #         self._metadata_bus_file_ext = ext
        #         self._metadata_bus_file_with_path = temp_metadata_bus_file
        #         break
        #
        # if not check_file_metadata_name_exist:
        #     return self.Object_Confirm_IUnKnown, self.__object_name__

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
        if not self.identify_dom_or_dem_metadata_bus_file():
            return CResult.merge_result(self.Failure, '元数据文件不存在, 无法解析! ')

        # metadata_xml_file_name = CFile.join_file(self.file_content.content_root_dir,
        #                                         '{0}.xml'.format(self.classified_object_name()))
        # 获取业务元数据文件文件主名，全名与类型
        metadata_bus_file_main_name = self.file_info.__file_main_name__
        metadata_bus_file_name = self._metadata_bus_file_with_path
        metadata_bus_file_ext = self._metadata_bus_file_ext
        # 构建虚拟xml文件
        metadata_xml_file_name = CFile.join_file(self.file_content.work_root_dir, self.FileName_MetaData)
        try:
            # 构建用于转换格式的xml对象，并建立根节点
            xml_obj = CXml()
            xml_obj.new_xml('root')
            if CUtils.equal_ignore_case(metadata_bus_file_ext, 'mdb'):
                xml_obj.set_attr(xml_obj.xpath_one('/root'), 'type', 'dom_mdb')
                xml_obj = self.mdb_to_xml(metadata_bus_file_main_name, metadata_bus_file_name, xml_obj)
            elif CUtils.equal_ignore_case(metadata_bus_file_ext, 'mat'):
                pass
            elif CUtils.equal_ignore_case(metadata_bus_file_ext, 'xls'):
                pass
            elif CUtils.equal_ignore_case(metadata_bus_file_ext, 'xlsx'):
                pass
            xml_obj.save_file(metadata_xml_file_name)
        except:
            return CResult.merge_result(self.Failure, '元数据文件[{0}]解析异常! '.format(metadata_bus_file_name))

        # if not CFile.file_or_path_exist(metadata_xml_file_name):
        #     return CResult.merge_result(self.Failure, '元数据文件[{0}]不存在, 无法解析! '.format(metadata_xml_file_name))
        try:
            parser.metadata.set_metadata_bus_file(self.Success,
                                                  '元数据文件[{0}]成功加载! '.format(metadata_bus_file_name),
                                                  self.MetaDataFormat_XML,
                                                  metadata_xml_file_name)
            return CResult.merge_result(self.Success,
                                        '元数据文件[{0}]成功加载! '.format(metadata_bus_file_name))
        except:
            parser.metadata.set_metadata_bus(self.Exception,
                                             '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(metadata_bus_file_name),
                                             self.MetaDataFormat_Text,
                                             '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(metadata_bus_file_name))




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
    xml_obj = CXml()
    xml_obj.new_xml('root')
    xml_obj.set_attr(xml_obj.xpath_one('/root'), 'type', 'dom_mdb')
    xml_obj = plugins.mdb_to_xml('G49G001030', 'D:\\work\\测试数据\\数据入库3\\DOM\\湖南标准分幅成果数据\\G49G001030\\G49G001030.mdb',
                                 xml_obj)
    xml_obj.save_file('D:\\work\\资料\\调试日志.xml')
    print('结束')
