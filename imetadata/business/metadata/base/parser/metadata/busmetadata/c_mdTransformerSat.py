# -*- coding: utf-8 -*-
# @Time : 2020/10/17 13:31
# @Author : 王西亚
# @File : c_mdTransformerDOM.py
from imetadata.base.c_result import CResult
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerSat(CMDTransformer):
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
        return CXml()
