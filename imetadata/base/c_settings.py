# -*- coding: utf-8 -*- 
# @Time : 2020/10/24 10:16 
# @Author : 王西亚 
# @File : c_settings.py
import sys

from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource


class CSettings(CJson):
    def __init__(self, obj):
        super().__init__()
        self.load_obj(obj)

    def set_app_information(self, app_dir, app_name):
        json_app = self.xpath_one(CResource.Path_Setting_Application, None)
        if json_app is None:
            self.set_value_of_name(
                CResource.Name_Application,
                {
                    CResource.Name_Name: app_name,
                    CResource.Name_Directory: app_dir
                }
            )
        else:
            json_app[CResource.Name_Name] = app_name
            json_app[CResource.Name_Directory] = app_dir
            self.set_value_of_name(CResource.Name_Application, json_app)

        self.init_sys_path()

    def init_sys_path(self):
        app_dir = self.xpath_one(CResource.Path_Setting_Application_Dir, None)
        if app_dir is not None:
            sys.path.append(app_dir)
