# -*- coding: utf-8 -*-
# @Time : 2020/03/04
# @Author : 李兵洋
# @File : traverse_plugins_names.py.py


from imetadata.base.c_resource import CResource
from imetadata.base.c_file import CFile
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from imetadata.base.zip.c_zip_zipfile import CZip_ZipFile
from imetadata.base.c_utils import CUtils
import argparse

class Compress(CResource):
    """
    分类压缩插件
    """
    def search_type(self):
        """
        检索插件类型
        :return:
        """
        listplugin = []
        plugins_root_dir = CSys.get_plugins_root_dir()
        plugins_type_list = CFile.file_or_subpath_of_path(plugins_root_dir)
        for plugins_type in plugins_type_list:
            if CFile.is_dir(CFile.join_file(plugins_root_dir, plugins_type)) and (
                    not (str(plugins_type)).startswith('_')):
                plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), plugins_type)
                path = CFile.join_file(CSys.get_plugins_root_dir(), plugins_type)
                plugins_file_list = CFile.file_or_subpath_of_path(path, '{0}_*.{1}'.format(self.Name_Plugins,
                                                                                           self.FileExt_Py))
                for file_name_without_path in plugins_file_list:
                    file_main_name = CFile.file_main_name(file_name_without_path)
                    class_classified_obj = CObject.create_plugins_instance(
                        plugins_root_package_name,
                        file_main_name,
                        None
                    )
                    plugins_info = class_classified_obj.get_information()
                    # 获取插件的类型和名字
                    plugins_info["dsodid"] = '{0}'.format(plugins_type) + CFile.unify_seperator + '{0}'.format(file_main_name)
                    listplugin.append(plugins_info)
        plugin_path = []
        # 遍历listplugin
        for i in listplugin:
            file_dict = {}
            # 获取当前文件工作目录
            work_path = CFile.file_abs_path('.')
            # 拼接通用路径
            main_path = work_path + "/imetadata/business/metadata/inbound/plugins/"
            # 分割插件类型和名字
            list = CUtils.dict_value_by_name(i, "dsodid",'').split(CFile.unify_seperator)
            # 拼接插件所在路径
            file_path = main_path + CUtils.dict_value_by_name(i, "dsodid",'') + "." + self.FileExt_Py
            # 格式化文件路径
            sorted_file_path = CFile.unify(file_path)
            """
            type: dir/file/layer
            source: 待压缩的文件路径
            target: 压缩后路径和名字(根据用户输入的压缩地址,然后拼接出完整的压缩文件)
            """
            file_dict[CResource.Name_Type] = list[0]
            file_dict.setdefault(CResource.Name_Source, [ ]).append(sorted_file_path)
            file_dict[CResource.Name_Target] = str(CUtils.dict_value_by_name(i, "dsodtype",'')) + ".zip"
            print(file_dict)
            plugin_path.append(file_dict)
        return plugin_path

    def begin_compress(self):
        """
        开始压缩
        -p后面接的是压缩到那个地方的路径,默认是压缩到当前工作的目录
        -m后面接的是一个数字0或者1表示压缩方式,默认是0   1 =  zipfile.ZIP_STORED , 0 = zipfile.ZIP_DEFLATED
        :return:
        """
        parser = argparse.ArgumentParser(description='add zip path, eg:"/user/bin/src/"')
        parser.add_argument("-p",
                            help='path no name, eg:"/user/bin/src/"',
                            default=CFile.file_abs_path('.') + CFile.unify_seperator +"zip" + CFile.unify_seperator)
        parser.add_argument("-m",
                            help='zip methods, use int, eg: 1 =  zipfile.ZIP_STORED and 0 = zipfile.ZIP_DEFLATED',
                            type=int,
                            default=0)
        args = parser.parse_args()
        path = args.p
        zip_way = args.m
        plugin_path = self.search_type()
        print("开始创建目录.........")
        print("创建目录成功")
        for plugin_name in plugin_path:
            path_with_name = path + CUtils.dict_value_by_name(plugin_name, 'type', '') + CFile.unify_seperator + CUtils.dict_value_by_name(plugin_name, 'target', '')
            print("压缩路径是%s" %path_with_name)
            test = CZip_ZipFile(path_with_name)
            test.new(zip_way)
            test.add_file_or_path(plugin_name)
            test.close()
        print("所有插件压缩完成")

if __name__ == '__main__':
    Compress().begin_compress()