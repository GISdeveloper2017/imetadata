# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 12:03 
# @Author : 王西亚 
# @File : c_viewCreatorRaster.py

from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreator import CViewCreator


class CViewCreatorDocument(CViewCreator):
    def process(self) -> str:
        """
        todo 负责人 赵宇飞 在这里提取文档数据的快视图, 将元数据文件存储在self.file_content.view_root_dir下
            注意返回的串中有快视图和拇指图的文件名
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        result = CResult.merge_result(self.Success, '处理完毕!')
        result = CResult.merge_result_info(result, self.Name_Browse, '/aa/bb_browse.png')
        result = CResult.merge_result_info(result, self.Name_Thumb, '/aa/bb_thumb.png')
        return result
