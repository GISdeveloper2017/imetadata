# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:18
# @Author : 赵宇飞
# @File : plugins_1040_third_survey_block.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_third_survey import \
    c_filePlugins_guoto_third_survey


class plugins_1040_third_survey_block(c_filePlugins_guoto_third_survey):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '三调影像'
        information[self.Plugins_Info_Name] = 'third_survey_block'

        return information

    def classified(self):
        """
        设计国土行业数据third_survey_block的验证规则（三调影像—分块）
        todo 负责人 王学谦 在这里检验third_survey_block的识别规则
        :return:
        """
        pass