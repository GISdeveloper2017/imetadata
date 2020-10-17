# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:31 
# @Author : 王西亚 
# @File : c_mdTransformerDOM.py
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer
import pypyodbc


class CMDTransformerDOM(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()

        if CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MDB):
            return self.__process_file_format__(self.MetaDataFormat_XML)

    def mdb_to_xml(self, file_main_name, file_with_path, xml_obj):
        """
         TODO 王学谦 mdb文件转xml文件 by王学谦 初版，需要改进与调试
        :param file_main_name:文件主名，不带后缀名，同时也是mdb的表名
        :param file_with_path:文件全名，带路径
        :param xml_obj:进行转换的xml对象，一半在函数外提前定义
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
        node_property = xml_obj.create_element(xml_obj.xpath_one('/root'), 'property')
        xml_obj.set_attr(node_property, 'tablename', tablename)
        for field_index, row_obj in enumerate(cur.description):
            if CUtils.equal_ignore_case(row_obj[0], 'shape'):  # 跳过shape字段
                continue
            node_item = xml_obj.create_element(node_property, 'item')
            xml_obj.set_attr(node_item, 'name', row_obj[0])
            xml_obj.set_element_text(node_item, alldata[0][field_index])
        cur.close()
        conn.close()
        return xml_obj