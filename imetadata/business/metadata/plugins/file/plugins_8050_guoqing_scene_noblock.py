# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:21
# @Author : 赵宇飞
# @File : plugins_8050_guoqing_scene_noblock.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing


class plugins_8050_guoqing_scene_noblock(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	文件格式	是否有坐标系	内容样例	                说明
    影像文件
    （至少有一个img）	img/IMG	有	GF2398924020190510F.img	融合影像文件，xxxF-n、xxxM-n、xxxP-n为一组
                                GF2398924020190510M.img	多光谱影像文件
                                GF2398924020190510P.img	全色波段影像文件
    元数据文件	    xml/XML	无	GF2398924020190510M.XML	多光谱元数据文件
                                GF2398924020190510P.XML	全色元数据文件
                                GF2398924020190510Y.XML	整体元数据文件
    """
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-整景纠正'
        information[self.Plugins_Info_Name] = 'guoqing_scene_noblock'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_noblock的验证规则（国情影像—非分块）,不带数字
        todo 负责人 王学谦 在这里检验guoqing_scene_noblock的识别规则
        :return:
        """
        pass