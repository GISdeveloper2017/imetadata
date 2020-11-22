# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:18
# @Author : 赵宇飞
# @File : plugins_8040_third_survey_block.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_third_survey import \
    CFilePlugins_GUOTU_Third_Survey


class plugins_8040_third_survey_block(CFilePlugins_GUOTU_Third_Survey):
    """
    完成 负责人 王学谦
    数据内容	            命名标准	                                            举例
    影像文件
    （二者任一均可）	分块影像：
                        行政区划代码+采用星源+DOM+2位数分块编号.img               632701ZY3DOM15.img
                        说明：采用多种星源时，星源间以“+”连接                     632701BJ2+GF1+GJ1+ZY3DOM02.img
                    非分块影像：
                        行政区划代码+采用星源+DOM.img
                        说明：当星源为多个时，各星源间用“+”连接表示，例GF1+GF2+BJ2	632701ZY3DOM.img
                                                                            632701BJ2+GF1+GJ1+ZY3DOM.img
    元数据文件	    6位行政区划代码+县（旗、县级市）名称.mdb	                    632701玉树市.mdb
    关于正则表达式     https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '三调影像'
        information[self.Plugins_Info_Name] = 'third_survey_block'

        return information

    def classified(self):
        """
        设计国土行业数据third_survey_block的验证规则（三调影像—分块）
        完成 负责人 王学谦 在这里检验third_survey_block的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_path = self.file_info.file_path
        if len(file_main_name) > 6:
            file_name_before_six = file_main_name[0:6]  # 截取前六位行政区划代码
        else:
            return self.Object_Confirm_IUnKnown, self._object_name  # 主名必然大于6

        if not CUtils.text_is_numeric(CUtils.any_2_str(file_name_before_six)):
            return self.Object_Confirm_IUnKnown, self._object_name  # 前六位必然为数字

        # 正则表达式，(?i)代表大小写不敏感，^代表字符串开头，$代表字符串结尾
        # \S用于匹配所有非空字符，+代表匹配前面字符的数量为至少一个，即\S+匹配一个或多个非空字符
        # \d匹配数字，即[0-9]，即\d+匹配一个或多个非空字符
        match_str = '(?i)^'+file_name_before_six+r'\S+dom\d+.img$'
        check_file_main_name_exist = CFile.find_file_or_subpath_of_path(file_path, match_str, CFile.MatchType_Regex)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        # file_name_before_six_name = ''
        # file_metadata_name = '{0}{1}'.format(file_name_before_six, file_name_before_six_name)
        # file_metadata_name_with_path = CFile.join_file(file_path, file_metadata_name)
        # check_file_mdb_exist = CFile.file_or_path_exist('{0}.mdb'.format(file_metadata_name_with_path))
        # if not check_file_mdb_exist:  # 检查mdb文件存在性
        #     return self.Object_Confirm_IUnKnown, self._object_name
        if len(file_main_name) >= 14:
            name_sub_7_to_8 = file_main_name[6:8]
            name_sub_backwards_6_to_3 = file_main_name[-5:-2]
            name_sub_backwards_2_to_1 = file_main_name[-2:]
            if CUtils.text_is_alpha(name_sub_7_to_8) \
                    and CUtils.equal_ignore_case(CUtils.any_2_str(name_sub_backwards_6_to_3).lower(),
                                                 'dom') \
                    and CUtils.text_is_numeric(CUtils.any_2_str(name_sub_backwards_2_to_1)):
                if CUtils.equal_ignore_case(file_ext, 'img'):
                    self._object_confirm = self.Object_Confirm_IKnown
                    self._object_name = file_main_name
                    self.add_file_to_detail_list(file_name_before_six)
                else:
                    self._object_confirm = self.Object_Confirm_IKnown_Not
                    self._object_name = None
            else:
                # 运行到此的文件，如果格式为以下，则默认为附属文件
                affiliated_ext_list = ['mdb', 'shp', 'shx', 'dbf', 'sbx', 'prj', 'sbn']
                if file_ext.lower() in affiliated_ext_list:
                    self._object_confirm = self.Object_Confirm_IKnown_Not
                    self._object_name = None
                else:
                    return self.Object_Confirm_IUnKnown, self._object_name
        else:
            # 运行到此的文件，如果格式为以下，则默认为附属文件
            affiliated_ext_list = ['mdb', 'shp', 'shx', 'dbf', 'sbx', 'prj', 'sbn']
            if file_ext.lower() in affiliated_ext_list:
                self._object_confirm = self.Object_Confirm_IKnown_Not
                self._object_name = None
            else:
                return self.Object_Confirm_IUnKnown, self._object_name

        return self._object_confirm, self._object_name


if __name__ == '__main__':
    pass
