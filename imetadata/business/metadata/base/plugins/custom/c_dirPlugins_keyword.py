# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_filePlugins_guotu.py
from abc import abstractmethod
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class CDirPlugins_keyword(CDirPlugins):
    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        information[self.Plugins_Info_Title] = information[self.Plugins_Info_ID]
        information[self.Plugins_Info_ViewEngine] = None
        information[self.Plugins_Info_SpatialEngine] = None
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_TagsEngine] = None
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Module_Distribute_Engine] = None  # 同步的引擎，值是发布同步用的类的名字
        return information

    def classified(self):
        """
        关键字识别
        """
        super().classified()
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        Confirm_IUnKnown_flag = False
        Confirm_IKnown_Not_flag = False
        keyword_list = self.get_classified_character_of_keyword()
        if len(keyword_list) > 0:
            file_name_flag = False
            file_path_flag = False
            file_ext_flag = False
            for keyword_info in keyword_list:
                keyword_id = CUtils.dict_value_by_name(keyword_info, self.Name_ID, None)
                regex_match = CUtils.dict_value_by_name(keyword_info, self.TextMatchType_Regex, '.*')
                if CUtils.equal_ignore_case(keyword_id, 'file_name'):
                    if CUtils.text_match_re(file_main_name, regex_match):
                        file_name_flag = True
                elif CUtils.equal_ignore_case(keyword_id, 'file_path'):
                    if CUtils.text_match_re(file_path, regex_match):
                        file_path_flag = True
                elif CUtils.equal_ignore_case(keyword_id, 'file_ext'):
                    if CUtils.text_match_re(file_ext, regex_match):
                        file_ext_flag = True

            if file_name_flag and file_path_flag and file_ext_flag:
                Confirm_IUnKnown_flag = True
            elif file_name_flag and file_path_flag and (not file_ext_flag):
                Confirm_IKnown_Not_flag = True
        else:
            Confirm_IUnKnown_flag = False
            Confirm_IKnown_Not_flag = False

        if Confirm_IUnKnown_flag:
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.get_classified_object_name_of_keyword(file_main_name)
        elif Confirm_IKnown_Not_flag:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        else:
            self._object_confirm = self.Object_Confirm_IUnKnown
            self._object_name = None

        return self._object_confirm, self._object_name

    @abstractmethod
    def get_classified_character_of_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: 'file_name',
                self.TextMatchType_Regex: None
            },
            {
                self.Name_ID: 'file_path',
                self.TextMatchType_Regex: None
            },
            {
                self.Name_ID: 'file_ext',
                self.TextMatchType_Regex: None
            }
        ]

    @abstractmethod
    def get_classified_object_name_of_keyword(self, file_main_name) -> str:
        return file_main_name
