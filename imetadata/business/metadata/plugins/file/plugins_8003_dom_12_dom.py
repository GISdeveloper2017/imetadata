# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:06
# @Author : 赵宇飞
# @File : plugins_8003_dom_12_dom.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dom import CFilePlugins_GUOTU_DOM


class plugins_8003_dom_12_dom(CFilePlugins_GUOTU_DOM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_12_dom'

        return information

    def classified(self):
        """
        设计国土行业数据的dom-12_dom验证规则
        todo 负责人 李宪 在这里检验dom-12_dom的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__

        check_file_main_name_length = len(file_main_name) == 15
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self._object_name

        file_main_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif))

        if not check_file_main_name_exist:
            return self.Object_Confirm_IUnKnown, self._object_name

        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第8910位是数字
        下面判别第111213位是DOM
        """
        char_1 = file_main_name[0:1]
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_12 = file_main_name[7:12]
        char_13_to_15 = file_main_name[12:15]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_7) is False \
                or CUtils.text_is_numeric(char_8_to_12) is False \
                or CUtils.equal_ignore_case(char_13_to_15, "DOM") is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        if CUtils.equal_ignore_case(file_ext, self.Name_Tif):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name