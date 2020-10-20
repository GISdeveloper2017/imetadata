# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:00
# @Author : 赵宇飞
# @File : plugins_1020_ortho.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class plugins_1020_ortho(CFilePlugins_GUOTU):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '单景正射'
        information[self.Plugins_Info_Name] = 'ortho'

        return information

    def classified(self):
        """
        设计国土行业数据ortho的验证规则（单景正射）
        todo 负责人 王学谦 在这里检验ortho的识别规则
        :return:
        """
        pass