# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:14 
# @Author : 王西亚 
# @File : c_mdTransformer.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData


class CMDTransformer(CParser):
    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx, file_content: CVirtualContent,
                 metadata: CMetaData, transformer_type: str, transformer_src_filename: str):
        self.__file_content = file_content
        self.__transformer_type__ = transformer_type
        self.__transformer_src_filename__ = transformer_src_filename
        self.__metadata__ = metadata
        super().__init__(object_id, object_name, file_info)

    @property
    def file_content(self):
        return self.__file_content

    @property
    def transformer_type(self):
        return self.__transformer_type__

    @property
    def metadata(self):
        return self.__metadata__

    @property
    def transformer_src_filename(self):
        return self.__transformer_src_filename__

    def process(self) -> str:
        """
        :return:
        """
        return CResult.merge_result(
            self.Success,
            '文件[{0}]成功加载! '.format(self.transformer_src_filename)
        )
