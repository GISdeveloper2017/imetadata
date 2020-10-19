# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:31 
# @Author : 王西亚 
# @File : c_mdTransformerDOM.py

from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer
import pypyodbc


class CMDTransformerDOM(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()

        xml_obj = CXml()
        root_element = xml_obj.new_xml('root')
        xml_obj.set_attr(root_element, self.Name_Type, self.transformer_type)
        try:
            if CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MDB):
                self.mdb_to_xml(self.object_name, self.file_info.__file_name_with_full_path__, root_element)
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MAT):
                pass
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_XLS):
                pass
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_XLSX):
                pass

            super().metadata.set_metadata_bus(
                self.Success,
                '元数据文件[{0}]成功加载! '.format(self.file_info.__file_name_with_full_path__),
                self.MetaDataFormat_XML,
                xml_obj.to_xml()
            )

            return CResult.merge_result(
                self.Success,
                '元数据文件[{0}]成功加载! '.format(self.file_info.__file_name_with_full_path__)
            )
        except:
            super().metadata.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(self.file_info.__file_name_with_full_path__),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(self.file_info.__file_name_with_full_path__)
            )

    def mdb_to_xml(self, file_main_name, file_with_path, parent_element):
        """
         TODO 王学谦 mdb文件转xml文件 by王学谦 初版，需要改进与调试
        :param file_main_name:文件主名，不带后缀名，同时也是mdb的表名
        :param file_with_path:文件全名，带路径
        :param parent_element:进行转换的xml对象，一半在函数外提前定义
        :return: xml_obj:转换好的xml对象
        """
        tablename = file_main_name  # 暂时 表名为与文件名一样 by王学谦

        # conn = pypyodbc.connect('DSN=mdb'); #linux配置，需要配置mdbtools, unixODBC, libmdbodbc
        mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};' + 'DBQ={0}'.format(file_with_path)  # win的驱动，需要安装
        conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
        cur = conn.cursor()
        sql = "SELECT * FROM " + tablename
        cur.execute(sql)
        alldata = cur.fetchall()
        # total_rows = len(alldata)  # 行
        # total_cols = len(alldata[0])  # 列
        node_property = CXml.create_element(parent_element, 'property')
        CXml.set_attr(node_property, 'tablename', tablename)
        for field_index, row_obj in enumerate(cur.description):
            if CUtils.equal_ignore_case(row_obj[0], 'shape'):  # 跳过shape字段
                continue
            node_item = parent_element.create_element(node_property, 'item')
            parent_element.set_attr(node_item, 'name', row_obj[0])
            parent_element.set_element_text(node_item, alldata[0][field_index])
        cur.close()
        conn.close()
