# -*- coding: utf-8 -*-
# @Time : 2020/10/17 13:31
# @Author : 王西亚
# @File : c_mdTransformerDOM.py

import re
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerSat import CMDTransformerSat


class CMDTransformerSat_LandSat(CMDTransformerSat):
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
        xml_obj.set_attr(node_root, self.Name_Type, self.Transformer_TXT)  # 设置root节点与属性
        # 设置操作的节点
        current_node = node_root
        for row_text in text_list:
            if CUtils.equal_ignore_case('row_text', 'END'):
                break
            # 分割字符
            row_list = re.split(r'=', row_text.strip())
            if len(row_list) >= 2:
                # 为GROUP建立新节点
                if CUtils.equal_ignore_case(row_list[0], 'GROUP'):
                    node_item = xml_obj.create_element(current_node, 'item')
                    # 值设为属性
                    item_value = CUtils.any_2_str(row_list[1].strip())
                    if item_value.startswith('"') and item_value.endswith('"'):
                        item_value = item_value[1:-1]
                    xml_obj.set_attr(node_item, self.Name_Name, item_value)

                    current_node = node_item
                elif CUtils.equal_ignore_case(row_list[0], 'END_GROUP'):
                    current_node = xml_obj.node_xpath_one(current_node, '..')
                else:
                    node_item = xml_obj.create_element(current_node, 'item')
                    xml_obj.set_attr(node_item, self.Name_Name, row_list[0].strip())
                    item_value = CUtils.any_2_str(row_list[1].strip())
                    if item_value.startswith('"') and item_value.endswith('"'):
                        item_value = item_value[1:-1]
                    xml_obj.set_element_text(node_item, item_value)

        return xml_obj


if __name__ == '__main__':
    pass
