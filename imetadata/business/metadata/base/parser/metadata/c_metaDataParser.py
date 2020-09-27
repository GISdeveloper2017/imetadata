# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 09:08 
# @Author : 王西亚 
# @File : c_metaDataParser.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.metadata.quality.c_quality import CQuality
from imetadata.database.c_factory import CFactory


class CMetaDataParser(CParser):
    """
    对象元数据处理类
    在本对象中, 要处理如下内容:
    . 对象的质检
    . 对象的业务元数据
    . 对象的基础元数据
    . 对象的可视元数据
    . 对象的元数据优化
    """
    __information__: dict
    __file_content__: CVirtualContent = None
    __file_quality__: CQuality = None

    def __init__(self, db_server_id: str, object_id: str, object_name: str, file_info: CFileInfoEx, file_content: CVirtualContent, information: dict):
        self.__file_quality__ = CQuality()
        self.__information__ = information
        self.__file_content__ = file_content
        super().__init__(db_server_id, object_id, object_name, file_info)

    @property
    def file_quality(self):
        return self.__file_quality__

    @property
    def file_content(self):
        return self.__file_content__

    def process(self) -> str:
        """
        完成元数据的所有处理操作
        1. 数据解析处理
        1. 文件命名检查
        1. 文件完整性检查
        1. 文件元数据提取并分析
        1. 业务元数据提取并分析
        :return:
        """
        file_quality_text = self.__file_quality__.to_xml()
        quality_result = self.__file_quality__.quality_result()

        CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_object
                    set dso_quality = :dso_quality, dso_quality_result = :dso_quality_result
                    where dsoid = :dsoid
                    ''', {'dso_quality': file_quality_text, 'dsoid': self.__object_id__, 'dso_quality_result': quality_result}
                                                               )
        return CUtils.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        pass
