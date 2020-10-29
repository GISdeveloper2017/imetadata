# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:26
# @Author : 赵宇飞
# @File : plugins_8051_guoqing_scene_block.py

from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing


class plugins_8051_guoqing_scene_block(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	    文件格式	是否有坐标系	内容样例	                    说明
    影像文件
    （影像分块）	img/IMG	有	    GF2398924020190510F-1.img	分块影像文件，全色、多光谱、融合至少包含一种类型IMG，支持多块分割
                                GF2398924020190510F-2.img   优先顺序: F、P、M
                                GF2398924020190510M-1.img
                                GF2398924020190510M-2.img
                                GF2398924020190510P-1.img
                                GF2398924020190510P-2.img
    元数据文件	xml/XML	无	    GF2398924020190510M.XML	    元数据文件优先顺序: Y、P、M
                                GF2398924020190510P.XML
                                GF2398924020190510Y.XML
    """
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-整景纠正'
        information[self.Plugins_Info_Name] = 'guoqing_scene_block'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_block的验证规则（国情影像—分块）,带数字 F-1/F-2
        todo 负责人 王学谦 在这里检验guoqing_scene_block的识别规则
        :return:
        """
        pass