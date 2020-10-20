# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 13:31 
# @Author : 王西亚 
# @File : c_mdTransformerDOM.py

from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer
import pypyodbc
import xlrd
import re


class CMDTransformerDOM(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()

        file_metadata_name_with_path = '{0}.{1}'.format(
            CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__),
            self.transformer_type
        )

        try:
            xml_obj = None
            if CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MDB):
                xml_obj = self.mdb_to_xml(file_metadata_name_with_path)
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MAT):
                pass
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_XLS):
                xml_obj = self.xls_to_xml(file_metadata_name_with_path)
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_XLSX):
                xml_obj = self.xls_to_xml(file_metadata_name_with_path)
            else:
                raise

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
        except:
            super().metadata.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(file_metadata_name_with_path),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(file_metadata_name_with_path)
            )

    def mdb_to_xml(self, file_metadata_name_with_path: str):
        """
         TODO 王学谦 mdb文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的mdb文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        conn = None  # 预定义连接与游标，方便释放
        cur = None
        try:
            # conn = pypyodbc.connect('DSN=mymdb'); #linux配置，需要配置mdbtools, unixODBC, libmdbodbc
            mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};' + 'DBQ={0}'.format(file_metadata_name_with_path)
            conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
            cur = conn.cursor()

            sql = "SELECT * FROM " + self.object_name
            cur.execute(sql)
            table_data = cur.fetchall()
            # total_rows = len(alldata)  # 行
            # total_cols = len(alldata[0])  # 列
            xml_obj = CXml()
            node_root = xml_obj.new_xml('root')
            xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)
            for field_index, row_obj in enumerate(cur.description):
                row_name = row_obj[0]  # 字段名称
                row_type = row_obj[1]  # 字段类型
                if row_type is bytearray:  # 跳过长二进制数组
                    continue
                node_item = xml_obj.create_element(node_root, 'item')
                xml_obj.set_attr(node_item, self.Name_Name, row_name)
                xml_obj.set_element_text(node_item, table_data[0][field_index])
        except:
            raise
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return xml_obj

    def mat_to_xml(self, file_metadata_name_with_path: str):
        """
         TODO 王学谦 mat文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的mdb文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        pass

    def xls_to_xml(self, file_metadata_name_with_path: str):
        """
         TODO 王学谦 xls/xlsx文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的mdb文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        all_data = xlrd.open_workbook(file_metadata_name_with_path)
        table_data = all_data.sheets()[0]

        cols_num = table_data.ncols
        rows_num = table_data.nrows
        cols_index = 0
        if CUtils.equal_ignore_case(str(cols_num), str(2)):
            pass
        elif CUtils.equal_ignore_case(str(cols_num), str(3)):
            cols_index = 1
        else:
            raise

        xml_obj = CXml()
        node_root = xml_obj.new_xml('root')
        xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)
        for row in range(0, rows_num):
            node_item = xml_obj.create_element(node_root, 'item')
            xml_obj.set_attr(node_item, self.Name_Name, table_data.cell(row, cols_index).value)
            xml_obj.set_element_text(node_item, table_data.cell(row, cols_index + 1).value)
        return xml_obj


if __name__ == '__main__':
    pass
    # file_metadata_name_with_path = r'D:\work\测试数据\数据入库3\DOM\湖北单个成果数据\H49G001026\H49G001026.mat'
    # text_list = CFile.file_2_list(file_metadata_name_with_path)
    # text_secondary_array = None
    # for index, row_text in enumerate(text_list):
    #     text_first_array = re.split('\t+', row_text)
    #     print(text_first_array)
    #     text_secondary_array[index] = text_first_array
    #
    # print(text_secondary_array)
