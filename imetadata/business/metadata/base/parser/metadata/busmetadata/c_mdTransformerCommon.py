# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:31 
# @Author : 王西亚 
# @File : c_mdTransformerDOM.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerCommon(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()
        if CUtils.equal_ignore_case(self.transformer_type, self.Transformer_XML):
            return self.__process_file_format__(self.MetaDataFormat_XML)
        elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_Json):
            return self.__process_file_format__(self.MetaDataFormat_Json)
        elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_TXT):
            return self.__process_file_format__(self.MetaDataFormat_Text)

    def __process_file_format__(self, metadata_format: str):
        if not CFile.file_or_path_exist(self.transformer_src_filename):
            return CResult.merge_result(
                self.Failure,
                '文件[{0}]不存在, 无法解析! '.format(self.transformer_src_filename)
            )

        try:
            self.__metadata__.set_metadata_bus_file(
                self.Success,
                '文件[{0}]成功加载! '.format(self.transformer_src_filename),
                metadata_format,
                self.transformer_src_filename
            )
            return CResult.merge_result(
                self.Success,
                '文件[{0}]成功加载! '.format(self.transformer_src_filename)
            )
        except:
            self.__metadata__.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法, 无法处理! '.format(self.transformer_src_filename),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法, 无法处理! '.format(self.transformer_src_filename)
            )
