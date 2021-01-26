# -*- coding: utf-8 -*-
# @Time : 2020/10/17 13:31
# @Author : 王西亚
# @File : c_mdTransformerDOM.py

import re
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerSat_k2(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()

        file_metadata_name_with_path = self.transformer_src_filename
        try:
            xml_obj = self.txt_to_xml(file_metadata_name_with_path)

            if xml_obj is not None:
                super().metadata.set_metadata_bus(
                    self.Success,
                    '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path),
                    self.MetaDataFormat_XML,
                    xml_obj.to_xml()
                )

                return CResult.merge_result(
                    self.Success,
                    '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path)
                )
            else:
                raise
        except Exception as error:
            super().metadata.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法, 无法处理! 错误原因为{1}'
                    .format(file_metadata_name_with_path, error.__str__()),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法, 无法处理! 错误原因为{1}'
                    .format(file_metadata_name_with_path, error.__str__())
            )

    def txt_to_xml(self, file_metadata_name_with_path: str):
        """
        完成 王学谦 txt文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的mat文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        text_list = CFile.file_2_list(file_metadata_name_with_path)  # 获取mat文件作为列表
        if (text_list is None) or len(text_list) == 0:
            raise  # 如果获取的文件内容为空，则抛出异常

        xml_obj = CXml()  # 建立xml对象
        node_root = xml_obj.new_xml('root')
        xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)  # 设置root节点与属性
        for row_text in text_list:
            row_list = re.split(r'\s+', row_text.strip())  # 利用正则表达式，根据一个或多个tab剪切字符
            # item节点
            node_item = xml_obj.create_element(node_root, 'item')
            xml_obj.set_attr(node_item, self.Name_Name, CUtils.any_2_str(row_list[0]))
            del row_list[0]
            # value节点
            for row in row_list:
                node_value = xml_obj.create_element(node_item, 'value')
                xml_obj.set_element_text(node_value, CUtils.any_2_str(row.strip()))  # 设置item节点与属性与内容
        return xml_obj


if __name__ == '__main__':
    pass
    # file_metadata_name_with_path = r'D:\work\测试数据\原始数据\未整理\卫星测试数据\卫星样例数据' \
    #                                r'\样例一\MSC_120327020449_30221_09881221\MSC_120327020449_30221_09881221PP02_1R.txt'
