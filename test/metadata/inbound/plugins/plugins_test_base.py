# -*- coding: utf-8 -*- 
# @Time : 2020/12/4 08:55 
# @Author : 王西亚 
# @File : test_plugins_base.py

from abc import abstractmethod

import allure

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class Plugins_Test_Base(CResource):
    _test_file_root_path = ''
    _test_file_parent_path = ''

    @abstractmethod
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return None

    @abstractmethod
    def test_file_info_list(self) -> list:
        return []

    def get_test_file_info(self, test_file_info: dict):
        file_type = CUtils.dict_value_by_name(test_file_info, self.Name_Test_File_Type, None)
        test_file_with_rel_path = CUtils.dict_value_by_name(test_file_info, self.Name_Test_file_path, None)
        correct_object_confirm = CUtils.dict_value_by_name(test_file_info, self.Name_Test_object_confirm, None)
        correct_object_name = CUtils.dict_value_by_name(test_file_info, self.Name_Test_object_name, None)
        return file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        plugins_group = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Group_Title, '')
        plugins_type = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Type, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog,
            plugins_group,
            plugins_type
        )

    def get_test_obj(self, file_type, test_file_with_full_path):
        file_info = CDMFilePathInfoEx(
            file_type,
            test_file_with_full_path,
            None,  # storage_id
            None,  # file_id
            None,  # file_parent_id
            None,  # owner_id
            self.DB_Server_ID_Default,
            None
        )
        plugins_obj = self.create_plugins(file_info)
        plugins_obj.classified()
        plugins_obj.create_virtual_content()
        metadata_parser = CMetaDataParser(
            CUtils.one_id(),
            test_file_with_full_path.replace(self._test_file_parent_path, ''),
            file_info, plugins_obj.file_content, plugins_obj.get_information()
        )
        return file_info, plugins_obj, metadata_parser

    @allure.story("文件识别")  # 二级标题
    @allure.title("文件识别")  # 方法名称
    @allure.description("测试classified方法")  # 描述
    def test_classified(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
            # 获取插件对象
            file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
            # 执行测试
            object_confirm, object_name = plugins_obj.classified()
            # 检查结果
            if object_confirm == self.Object_Confirm_IKnown:
                flag = (object_confirm == correct_object_confirm) and (object_name == correct_object_name)
            else:
                flag = (object_confirm == correct_object_confirm)
            # 录入测试信息
            allure.attach(
                '应该的可能性为{0}，识别出的可能性为{1}。'
                '应该的对象名为{2}，识别出的对象名为{3}'.format(
                    correct_object_confirm, object_confirm, correct_object_name, object_name
                ),
                '{0}'.format(test_file_with_rel_path),
                allure.attachment_type.TEXT
            )
            assert flag

    @allure.story("影像元数据")  # 三级标题
    @allure.title("影像元数据")  # 方法标题
    @allure.description("测试metadata方法")  # 描述
    def test_metadata(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            if correct_object_confirm == self.Object_Confirm_IKnown:
                test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
                # 获取插件对象
                file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
                # 执行测试
                plugins_obj.parser_metadata_with_qa(metadata_parser)
                # 获取结果
                result_with_qa, message_with_qa, metadata_type, metadata \
                    = metadata_parser.metadata.metadata()
                # 录入测试信息
                allure.attach('元数据处理信息为{0},元数据类型为{1},元数据内容为{2},'
                              .format(message_with_qa, metadata_type, metadata),
                              '{0}'.format(test_file_with_rel_path),
                              allure.attachment_type.TEXT)
                assert result_with_qa

    @allure.story("业务元数据")  # 三级标题
    @allure.title("业务元数据")  # 方法标题
    @allure.description("测试metadata_bus方法")  # 描述
    def test_metadata_bus(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            if correct_object_confirm == self.Object_Confirm_IKnown:
                test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
                # 获取插件对象
                file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
                # 执行测试
                plugins_obj.parser_metadata_with_qa(metadata_parser)
                # 获取结果
                result_with_bus_qa, message_with_bus_qa, metadata_bus_type, metadata_bus \
                    = metadata_parser.metadata.metadata_bus()
                # 录入测试信息
                allure.attach('业务元数据处理信息为{0},业务元数据类型为{1},业务元数据内容为{2}'
                              .format(message_with_bus_qa, metadata_bus_type, metadata_bus),
                              '{0}'.format(test_file_with_rel_path),
                              allure.attachment_type.TEXT)
                assert result_with_bus_qa

    @allure.story("时间元数据")  # 三级标题
    @allure.title("时间元数据")  # 方法标题
    @allure.description("测试metadata_time方法")  # 描述
    def test_metadata_time(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            if correct_object_confirm == self.Object_Confirm_IKnown:
                test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
                # 获取插件对象
                file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
                # 执行测试
                plugins_obj.parser_metadata_with_qa(metadata_parser)
                plugins_obj.parser_metadata_time_after_qa(metadata_parser)
                # 获取结果
                result_with_time, message_with_time, time_information = metadata_parser.metadata.metadata_time()
                # 录入测试信息
                allure.attach('处理信息为{0},时间元数据内容为{1}'
                              .format(message_with_time, time_information),
                              '{0}'.format(test_file_with_rel_path),
                              allure.attachment_type.TEXT)
                assert result_with_time

    @allure.story("空间元数据")  # 三级标题
    @allure.title("空间元数据")  # 方法标题
    @allure.description("测试metadata_spatial方法")  # 描述
    def test_metadata_spatial(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            if correct_object_confirm == self.Object_Confirm_IKnown:
                test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
                # 获取插件对象
                file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
                # 执行测试
                plugins_obj.parser_metadata_with_qa(metadata_parser)
                plugins_obj.parser_metadata_spatial_after_qa(metadata_parser)
                # 获取结果
                result_with_spatial, message_with_spatial, metadata_spatial \
                    = metadata_parser.metadata.metadata_spatial()
                # 录入测试信息
                allure.attach('处理信息为{0},空间元数据内容为{1}'
                              .format(message_with_spatial, metadata_spatial),
                              '{0}'.format(test_file_with_rel_path),
                              allure.attachment_type.TEXT)
                assert result_with_spatial

    @allure.story("视图元数据")  # 三级标题
    @allure.title("视图元数据")  # 方法标题
    @allure.description("测试metadata_view方法")  # 描述
    def test_metadata_view(self):
        self.init_before_test()  # 初始化路径

        for test_file_info in self.test_file_info_list():
            file_type, test_file_with_rel_path, correct_object_confirm, correct_object_name = \
                self.get_test_file_info(test_file_info)
            if correct_object_confirm == self.Object_Confirm_IKnown:
                test_file_with_full_path = CFile.join_file(self._test_file_parent_path, test_file_with_rel_path)
                # 获取插件对象
                file_info, plugins_obj, metadata_parser = self.get_test_obj(file_type, test_file_with_full_path)
                # 执行测试
                plugins_obj.parser_metadata_with_qa(metadata_parser)
                plugins_obj.parser_metadata_view_after_qa(metadata_parser)
                # 获取结果
                result_with_view, message_with_view, thumb_img_file_name, browse_img_file_name \
                    = metadata_parser.metadata.metadata_view()
                # 录入测试信息
                allure.attach('处理信息为{0}'.format(message_with_view),
                              '{0}'.format(test_file_with_rel_path),
                              allure.attachment_type.TEXT)
                # 因为快视图拇指图的路径生成依赖数据库object表，所以测试中暂时无法生成文件
                # allure.attach.file(thumb_img_file_name, attachment_type=allure.attachment_type.JPG)
                # allure.attach.file(browse_img_file_name, attachment_type=allure.attachment_type.PNG)
                assert result_with_view
