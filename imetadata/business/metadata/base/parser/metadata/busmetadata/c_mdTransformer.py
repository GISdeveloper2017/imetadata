# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:14 
# @Author : 王西亚 
# @File : c_mdTransformer.py
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData
import pypyodbc


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

    def get_mdb_connect(self, file_metadata_name_with_path):
        """
        :return:
        """
        try:
            # win下需要安装AccessDatabaseEngine_X64.exe驱动
            # linux下需要安装mdbtools与unixODBC-2.3.9.tar与gdal，gdal拥有pgeo驱动
            # 并将odbcinst.ini文件的设置一个连接名为Driver=Microsoft Access Driver (*.mdb)的项目
            mdb = 'Driver=Microsoft Access Driver (*.mdb);' + 'DBQ={0}'.format(
                file_metadata_name_with_path)  # win驱动，安装AccessDatabaseEngine_X64.exe驱动
            #  get_os_name方法返回值, posix, nt, java对应linux / windows / java虚拟机
            if CUtils.equal_ignore_case(CSys.get_os_name(), 'nt'):  # win下返回nt
                conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
            else:
                conn = pypyodbc.connect(mdb)
        except Exception as error:
            raise Exception('mdb解析驱动异常:' + error.__str__())
        return conn


if __name__ == '__main__':
    #  get_os_name方法返回值, posix, nt, java对应linux / windows / java虚拟机
    print(CSys.get_os_name())
