# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_filePlugins_guotu.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
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
        information[self.Plugins_Info_Group] = None
        information[self.Plugins_Info_Group_Title] = None
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
        file_object_name = file_main_name[:]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母等字符的名
        object_flag = True
        keyword_list = self.get_classified_character_of_keyword()
        if len(keyword_list) == 0:
            object_flag = False
        for keyword_info in keyword_list:
            keyword_id = CUtils.dict_value_by_name(keyword_info, self.Name_ID, None)
            common_match = CUtils.dict_value_by_name(keyword_info, self.TextMatchType_Common, None)
            regex_match = CUtils.dict_value_by_name(keyword_info, self.TextMatchType_Regex, None)
            if CUtils.equal_ignore_case(keyword_id, 'file_name'):
                if common_match is not None:
                    if not CFile.file_match(file_main_name, common_match):
                        object_flag = False
                if regex_match is not None:
                    if not CUtils.text_match_re(file_main_name, regex_match):
                        object_flag = False
            elif CUtils.equal_ignore_case(keyword_id, 'file_path'):
                if common_match is not None:
                    if not CFile.file_match(file_main_name, common_match):
                        object_flag = False
                if regex_match is not None:
                    if not CUtils.text_match_re(file_main_name, regex_match):
                        object_flag = False

        if object_flag:
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_name_without_path

    @abstractmethod
    def get_classified_character_of_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: 'file_name',  # 左下角经度 必填
                self.TextMatchType_Common: None,
                self.TextMatchType_Regex: None
            },
            {
                self.Name_ID: 'file_path',  # 左下角经度 必填
                self.TextMatchType_Common: None,
                self.TextMatchType_Regex: None
            }
        ]
