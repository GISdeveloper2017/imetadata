# -*- coding: utf-8 -*- 
# @Time : 2020/10/13 16:22
# @Author : 赵宇飞
# @File : plugins_1001_dom_10_dom.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class plugins_1001_dom_10_DOM(CFilePlugins_GUOTU):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_10_dom'

        return information

    def classified(self):
        """
        设计国土行业数据的dom-10_dom验证规则
        todo 负责人 李宪 在这里检验dom-10_dom的元数据文件格式时, 应该一个一个类型的对比, 找到文件时, 将该文件的格式和文件名存储到类的私有属性中, 以便在元数据处理时直接使用
        :return:
        """
        pass

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 赵宇飞 在这里将dom-10_dom的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
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
    pass
