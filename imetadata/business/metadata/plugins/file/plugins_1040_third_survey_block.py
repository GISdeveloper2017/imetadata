# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:18
# @Author : 赵宇飞
# @File : plugins_1040_third_survey_block.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_third_survey import \
    CFilePlugins_GUOTU_Third_Survey


class plugins_1040_third_survey_block(CFilePlugins_GUOTU_Third_Survey):
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
        information[self.Plugins_Info_Name] = 'third_survey_block'

        return information

    def classified(self):
        """
        设计国土行业数据third_survey_block的验证规则（三调影像—分块）
        todo 负责人 王学谦 在这里检验third_survey_block的识别规则
        :return:
        """
        pass