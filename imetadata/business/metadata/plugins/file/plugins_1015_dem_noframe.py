# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:24
# @Author : 赵宇飞
# @File : plugins_1015_dem_noframe.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dem import CFilePlugins_GUOTU_DEM


class plugins_1015_dem_noframe(CFilePlugins_GUOTU_21AT):
    """
    todo 负责人 李宪
    数据内容	    文件格式	    是否有坐标系	内容样例	            说明
    影像文件	    img/IMG
                tif/TIF	    有	    XXXX区域5米DEM.img	    以影像文件为单位
    元数据文件 	xml/XML	    无	    XXXX区域5米DEM_21at.xml	元数据生产工具生成
    """

    def classified(self):
        """
        设计国土行业数据的dem_noframe非分幅数据的验证规则
        todo 负责人 李宪 在这里检验dem_noframe的识别规则
        :return:
        """
        pass