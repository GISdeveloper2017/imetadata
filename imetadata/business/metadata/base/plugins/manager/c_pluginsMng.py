# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 20:56 
# @Author : 王西亚 
# @File : c_pluginsMng.py
from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CPluginsMng(CResource):
    @classmethod
    def plugins_classified(cls, file_info: CDMFilePathInfoEx) -> CPlugins:
        """
        插件识别
        1. 首先检查file_info的__rule_content__中, 有无优先识别插件列表, 有则使用该列表按顺序进行识别
        1. 其次, 检查file_info的__rule_content__是否为空, 如果不为空, 则获取其类型, 如果类型不为空, 则按类型, 匹配系统配置
        1. 其次, 检查应用系统配置中, 有无对目录识别插件的特殊设置, 有则按设置中的列表进行识别
        1. 最后按系统插件目录下的顺序, 对数据进行识别
        :param file_info:
        :return:
        """
        class_classified_obj = None

        if file_info.file_type == cls.FileType_Dir:
            plugin_node_list = CXml.xml_xpath(file_info.rule_content, cls.Path_MD_Rule_Plugins_Dir)
        else:
            plugin_node_list = CXml.xml_xpath(file_info.rule_content, cls.Path_MD_Rule_Plugins_File)

        if len(plugin_node_list) > 0:
            class_classified_obj = cls.__plugins_classified_by_plugin_node_list__(file_info, plugin_node_list)

            if class_classified_obj is not None:
                return class_classified_obj

        rule_type = CXml.get_element_text(CXml.xml_xpath_one(file_info.rule_content, cls.Path_MD_Rule_Type))
        if not CUtils.equal_ignore_case(rule_type, ''):
            plugins_json_array = settings.application.xpath_one(cls.Path_Setting_MetaData_Plugins_Dir, None)
            if plugins_json_array is not None:
                for plugins_define in plugins_json_array:
                    key_word = CUtils.any_2_str(CUtils.dict_value_by_name(plugins_define, cls.Name_Keyword, None))
                    plugin_list = CUtils.dict_value_by_name(plugins_define, cls.Name_Plugin, None)
                    if plugin_list is None:
                        continue

                    if CUtils.equal_ignore_case(key_word, rule_type):
                        class_classified_obj = cls.__plugins_classified_by_plugin_list__(file_info, plugin_list)
        else:
            file_path = file_info.file_path_with_rel_path
            plugins_json_array = settings.application.xpath_one(cls.Path_Setting_MetaData_Plugins_Dir, None)
            if plugins_json_array is not None:
                for plugins_define in plugins_json_array:
                    key_word = CUtils.any_2_str(CUtils.dict_value_by_name(plugins_define, cls.Name_Keyword, None))
                    plugin_list = CUtils.dict_value_by_name(plugins_define, cls.Name_Plugin, None)
                    if plugin_list is None:
                        continue

                    # todo(注意) 如果关键字为空, 则表明所有子目录都优先使用设置的插件列表进行识别!!!
                    if CUtils.equal_ignore_case(key_word, ''):
                        class_classified_obj = cls.__plugins_classified_by_plugin_list__(file_info, plugin_list)
                    else:
                        if CFile.subpath_in_path(CUtils.any_2_str(key_word), file_path):
                            class_classified_obj = cls.__plugins_classified_by_plugin_list__(file_info, plugin_list)

        if class_classified_obj is not None:
            return class_classified_obj
        else:
            return cls.__plugins_classified_of_directory__(file_info)

    @classmethod
    def plugins(cls, file_info: CDMFilePathInfoEx, plugins_id: str) -> CPlugins:
        """
        根据给定的文件信息和插件名称, 直接创建插件对象
        如果插件文件不存在, 则返回None
        :param file_info:
        :param plugins_id:
        :return:
        """
        target_type = file_info.file_type
        target_path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_name = CFile.join_file(target_path, '{0}.{1}'.format(plugins_id, cls.FileExt_Py))
        if not CFile.file_or_path_exist(plugins_file_name):
            return None

        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, plugins_id, file_info)
        return class_classified_obj

    @classmethod
    def __plugins_classified_of_directory__(cls, file_info: CDMFilePathInfoEx) -> CPlugins:
        """
        使用系统目录下的所有插件进行识别
        :param file_info:
        :return:
        """
        target = file_info.file_main_name
        target_type = file_info.file_type
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.file_or_subpath_of_path(path, '{0}_*.{1}'.format(cls.Name_Plugins, cls.FileExt_Py))
        for file_name_without_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_without_path)
            try:
                class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                       file_info)
                object_confirm, object_name = class_classified_obj.classified()
                if object_confirm != cls.Object_Confirm_IUnKnown:
                    obj_info = class_classified_obj.get_information()
                    obj_id = class_classified_obj.get_id()
                    CLogger().debug(
                        '{0} is classified as {1}.{2}'.format(
                            target,
                            obj_info,
                            obj_id
                        )
                    )
                    return class_classified_obj
            except Exception as error:
                CLogger().debug('插件[{0}]解析出现异常, 错误信息为: [{1}], 请检查!'.format(file_main_name, error.__str__()))
                if settings.application.xpath_one('{0}.{1}'.format(cls.Name_Application, cls.Name_Debug),
                                                  cls.DB_False) == cls.DB_True:
                    raise
                else:
                    continue
        else:
            return None

    @classmethod
    def __plugins_classified_by_plugin_node_list__(cls, file_info: CDMFilePathInfoEx,
                                                   plugin_node_list: list) -> CPlugins:
        """
        根据外部给定的插件xml节点数组, 顺序进行识别, 返回第一个识别出文件的插件对象
        :param file_info:
        :param plugin_node_list:
        :return:
        """
        for plugin_node in plugin_node_list:
            plugin_id = CXml.get_element_text(plugin_node)
            class_classified_obj = cls.plugins(file_info, plugin_id)

            if class_classified_obj is None:
                continue

            try:
                object_confirm, object_name = class_classified_obj.classified()
                if object_confirm != cls.Object_Confirm_IUnKnown:
                    CLogger().debug(
                        '{0} is classified as {1}.{2}'.format(file_info.file_main_name,
                                                              class_classified_obj.get_information(),
                                                              class_classified_obj.get_id()))
                    return class_classified_obj
            except:
                CLogger().debug('插件[{0}]解析出现异常, 请检查!'.format(plugin_id))
                continue
        else:
            return None

    @classmethod
    def __plugins_classified_by_plugin_list__(cls, file_info: CDMFilePathInfoEx, plugin_list: list) -> CPlugins:
        """
        根据给定的插件列表, 顺序进行识别, 返回第一个识别出文件的插件对象
        :param file_info:
        :param plugin_list:
        :return:
        """
        for plugin_id in plugin_list:
            class_classified_obj = cls.plugins(file_info, plugin_id)

            if class_classified_obj is None:
                continue

            try:
                object_confirm, object_name = class_classified_obj.classified()
                if object_confirm != cls.Object_Confirm_IUnKnown:
                    CLogger().debug(
                        '{0} is classified as {1}.{2}'.format(file_info.file_main_name,
                                                              class_classified_obj.get_information(),
                                                              class_classified_obj.get_id()))
                    return class_classified_obj
            except:
                CLogger().debug('插件[{0}]解析出现异常, 请检查!'.format(plugin_id))
                continue
        else:
            return None
