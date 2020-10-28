# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:20
# @Author : 赵宇飞
# @File : plugins_1041_third_survey_noblock.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_third_survey import \
    CFilePlugins_GUOTU_Third_Survey
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils


class plugins_1041_third_survey_noblock(CFilePlugins_GUOTU_Third_Survey):
    """
    todo 负责人 王学谦
    数据内容	            命名标准	                                            举例
    影像文件
    （二者任一均可）	分块影像：
                        行政区划代码+采用星源+DOM+2位数分块编号.img               632701ZY3DOM15.img
                        说明：采用多种星源时，星源间以“+”连接                     632701BJ2+GF1+GJ1+ZY302.img
                    非分块影像：
                        行政区划代码+采用星源+DOM.img
                        说明：当星源为多个时，各星源间用“+”连接表示，例GF1+GF2+BJ2	632701ZY3DOM.img
                                                                            632701BJ2+GF1+GJ1+ZY3.img
    元数据文件	    6位行政区划代码+县（旗、县级市）名称.mdb	                    632701玉树市.mdb
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '三调影像'
        information[self.Plugins_Info_Name] = 'third_survey_noblock'

        return information

    def classified(self):
        """
        设计国土行业数据third_survey_noblock的验证规则（三调影像—非分块）
        todo 负责人 王学谦 在这里检验third_survey_noblock的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数
        file_path = self.file_info.__file_path__

        if len(file_main_name) > 6:
            file_name_before_six = file_main_name[0:6]  # 截取前六位行政区划代码
        else:
            return self.Object_Confirm_IUnKnown, self.__object_name__  # 主名必然大于6

        if CUtils.text_is_numeric(CUtils.any_2_str(file_name_before_six)):
            return self.Object_Confirm_IUnKnown, self.__object_name__  # 前六位必然为数字

        match_str = '{0}*dom??.img'.format(file_name_before_six)
        check_file_main_name_exist = CFile.find_file_or_subpath_of_path(file_path, match_str)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        # file_name_before_six_name = ''
        # file_metadata_name = '{0}{1}'.format(file_name_before_six, file_name_before_six_name)
        # file_metadata_name_with_path = CFile.join_file(file_path, file_metadata_name)
        # check_file_mdb_exist = CFile.file_or_path_exist('{0}.mdb'.format(file_metadata_name_with_path))
        # if not check_file_mdb_exist:  # 检查mdb文件存在性
        #     return self.Object_Confirm_IUnKnown, self.__object_name__

        name_sub_7_to_8 = file_main_name[6:8]
        name_sub_backwards_3_to_1 = file_main_name[-3:]
        if len(file_main_name) >= 12 and \
                CUtils.text_is_alpha(name_sub_7_to_8) and \
                CUtils.equal_ignore_case(
                    CUtils.any_2_str(name_sub_backwards_3_to_1).lower(), 'dom'
                ) and \
                CUtils.equal_ignore_case(file_ext, 'img'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__
