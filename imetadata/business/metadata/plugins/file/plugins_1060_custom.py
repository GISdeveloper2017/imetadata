# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:39
# @Author : 赵宇飞
# @File : plugins_1060_custom.py

from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_1060_custom(CFilePlugins_GUOTU_21AT):
    """
      注意5.9 自定义影像包含2中模式（***_21at.xml/无xml文件）
     todo 李宪
    """
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '自定义影像'
        information[self.Plugins_Info_Name] = 'custom'

        return information

    def classified(self):
        """
        设计国土行业数据custom的验证规则（自定义影像）
        todo 负责人 李宪 在这里检验custom的识别规则
        :return:
        """
        pass