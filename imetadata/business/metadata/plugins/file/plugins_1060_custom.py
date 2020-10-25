# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:39
# @Author : 赵宇飞
# @File : plugins_1060_custom.py

from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_1060_custom(CFilePlugins_GUOTU_21AT):
    """
     todo 李宪
     注意5.9 自定义影像包含2中模式（***_21at.xml/无xml文件）
    数据内容	    文件格式	是否有坐标系	内容样例	        说明
    影像文件	    img/IMG
                tif/TIF	    有	    XXXXXX.img	    以影像文件为单位
    元数据文件 	xml/XML	    无	    XXXXXX_21at.xml	元数据生产工具生成
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