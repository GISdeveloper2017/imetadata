# -*- coding: utf-8 -*- 
# @Time : 2020/9/7 11:00 
# @Author : 王西亚 
# @File : test_c_file.py
import allure
import pytest

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.inbound.plugins.file.plugins_8020_ortho import plugins_8020_ortho
from imetadata import settings

root_path_total = settings.application.xpath_one('directory.test', '')
root_path_module = CFile.join_file(root_path_total, '\\国土行业\\国土数据\\单景正射')  # 需要配置的地方1，配置相应的文件夹
file_type = 'file'  # 需要配置的地方2，文件对象配置file，数据集像配置dir
object_template = plugins_8020_ortho  # 需要配置的地方3，配置类对象
storage_id = '11'
db_id = 0
# 用于classified的部分
file_name_with_full_path_all_list = CFile.file_or_dir_fullname_of_path(root_path_module, True)
file_name_with_full_path_file_list = list()
for file_name_with_full_path_file in file_name_with_full_path_all_list:
    if CFile.is_file(file_name_with_full_path_file):
        file_name_with_full_path_file_list.append(file_name_with_full_path_file)

# 用于元数据测试的部分
object_name_with_full_path_list = ['单景test\\单景test.tif', '单景test_123\\单景test_123.tif']  # 需要配置的地方4，已知的对象
real_object_name_with_full_path_list = list()
for object_name_with_full_path in object_name_with_full_path_list:
    object_name_with_full_path = CFile.join_file(root_path_module, object_name_with_full_path)
    real_object_name_with_full_path_list.append(object_name_with_full_path)
print('预定义结束')


def get_parameter(real_file_name_with_full_path):
    file_info = CFileInfoEx(file_type, real_file_name_with_full_path, root_path_module, '')
    plugins_obj = object_template(file_info)
    file_info_obj = CDMFilePathInfoEx(
        file_type,  # 目录给dir，文件给file
        real_file_name_with_full_path,
        storage_id,  # storage_id
        '',  # file_id
        '',  # file_parent_id
        '',  # owner_id
        db_id,  # db_id
        ''  # rule_content
    )
    metadata_parser = CMetaDataParser(
        'dso_id', 'dso_object_name', file_info_obj, plugins_obj.file_content, plugins_obj.get_information())
    return plugins_obj, metadata_parser


@allure.feature("单景影像")  # 模块标题
@allure.story("文件识别")  # 模块标题
@allure.title("文件识别")  # 方法标题
@allure.description("测试classified方法")  # 描述
@pytest.mark.parametrize("file_name_with_full_path", file_name_with_full_path_file_list)
def test_classified(file_name_with_full_path):
    file_info = CFileInfoEx(file_type, file_name_with_full_path, root_path_module, '')
    plugins_obj = object_template(file_info)
    object_confirm, object_name = plugins_obj.classified()
    obj_name_with_full_path = plugins_obj.file_info.file_name_with_full_path
    flag = False
    if object_confirm == -1:
        if obj_name_with_full_path in real_object_name_with_full_path_list:
            flag = True
    else:
        if obj_name_with_full_path not in real_object_name_with_full_path_list:
            flag = True
    allure.attach('可能性为{0},识别出的对象名为{1}'.format(object_confirm, object_name),
                  'classified方法信息', allure.attachment_type.TEXT)
    assert flag


@allure.feature("单景影像")  # 模块标题
@allure.story("元数据提取")  # 模块标题
@allure.title("业务元数据")  # 方法标题
@allure.description("测试metadata方法")  # 描述
@pytest.mark.parametrize("real_file_name_with_full_path", real_object_name_with_full_path_list)
def test_metadata(real_file_name_with_full_path):
    plugins_obj, metadata_parser = get_parameter(real_file_name_with_full_path)
    plugins_obj.parser_metadata_with_qa(metadata_parser)
    result_with_qa, message_with_qa, metadata_bus_type, metadata_bus = metadata_parser.metadata.metadata_bus()
    allure.attach('处理信息为{0},业务元数据类型为{1},业务元数据内容为{2}'
                  .format(message_with_qa, metadata_bus_type, metadata_bus),
                  '业务元数据信息', allure.attachment_type.TEXT)
    assert result_with_qa


@allure.feature("单景影像")  # 模块标题
@allure.story("元数据提取")  # 模块标题
@allure.title("时间元数据")  # 方法标题
@allure.description("测试metadata_time方法")  # 描述
@pytest.mark.parametrize("real_file_name_with_full_path", real_object_name_with_full_path_list)
def test_metadata_time(real_file_name_with_full_path):
    plugins_obj, metadata_parser = get_parameter(real_file_name_with_full_path)
    plugins_obj.parser_metadata_with_qa(metadata_parser)
    plugins_obj.parser_metadata_time_after_qa(metadata_parser)
    result_with_time, message_with_time, time_information = metadata_parser.metadata.metadata_time()
    allure.attach('处理信息为{0},时间元数据内容为{1}'
                  .format(message_with_time, time_information),
                  '时间元数据信息', allure.attachment_type.TEXT)
    assert result_with_time


@allure.feature("单景影像")  # 模块标题
@allure.story("元数据提取")  # 模块标题
@allure.title("空间元数据")  # 方法标题
@allure.description("测试metadata_spatial方法")  # 描述
@pytest.mark.parametrize("real_file_name_with_full_path", real_object_name_with_full_path_list)
def test_metadata_spatial(real_file_name_with_full_path):
    plugins_obj, metadata_parser = get_parameter(real_file_name_with_full_path)
    plugins_obj.parser_metadata_spatial_after_qa(metadata_parser)
    result_with_spatial, message_with_spatial, metadata_spatial = metadata_parser.metadata.metadata_spatial()
    allure.attach('处理信息为{0},空间元数据内容为{1}'
                  .format(message_with_spatial, metadata_spatial),
                  '空间元数据信息', allure.attachment_type.TEXT)
    assert result_with_spatial


@allure.feature("单景影像")  # 模块标题
@allure.story("元数据提取")  # 模块标题
@allure.title("视图元数据")  # 方法标题
@allure.description("测试metadata_view方法")  # 描述
@pytest.mark.parametrize("real_file_name_with_full_path", real_object_name_with_full_path_list)
def test_metadata_view(real_file_name_with_full_path):
    plugins_obj, metadata_parser = get_parameter(real_file_name_with_full_path)
    plugins_obj.parser_metadata_view_after_qa(metadata_parser)
    result_with_view, message_with_view, thumb_img_file_name, browse_img_file_name \
        = metadata_parser.metadata.metadata_view()
    allure.attach('处理信息为{0},拇指图为{1}，快视图为{2}'
                  .format(message_with_view, thumb_img_file_name, browse_img_file_name),
                  '视图元数据信息', allure.attachment_type.TEXT)
    assert result_with_view


if __name__ == '__main__':
    pytest.main()
