# -*- coding: utf-8 -*-
# @Time : 2020/10/17 13:31
# @Author : 王西亚
# @File : c_mdTransformerDOM.py

import re
import pypyodbc
import xlrd
# import jaydebeapi
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerDOM(CMDTransformer):
    def process(self) -> str:
        """
        :return:
        """
        super().process()

        file_metadata_name_with_path = self.transformer_src_filename

        try:
            xml_obj = None
            if CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MDB):
                xml_obj = self.mdb_to_xml(file_metadata_name_with_path)
            elif CUtils.equal_ignore_case(self.transformer_type, self.Transformer_DOM_MAT):
                xml_obj = self.mat_to_xml(file_metadata_name_with_path)
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
        except Exception as error:
            super().metadata.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! 错误原因为{1}'
                    .format(file_metadata_name_with_path, error.__str__()),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! 错误原因为{1}'
                    .format(file_metadata_name_with_path, error.__str__())
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
            if CUtils.equal_ignore_case(CSys.get_os_name(), self.OS_Windows):
                mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};' + 'DBQ={0}'.format(
                    file_metadata_name_with_path)  # win驱动，安装AccessDatabaseEngine_X64.exe驱动
                conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
            elif CUtils.equal_ignore_case(CSys.get_os_name(), self.OS_Linux):
                pass
                # 安装jaydebeapi3包，使用UCanAccess.jar
                # ucanaccess_jars = [
                #     "/UCanAccess-4.0.4-bin/ucanaccess-4.0.4.jar",
                #     "/UCanAccess-4.0.4-bin/lib/commons-lang-2.6.jar",
                #     "/UCanAccess-4.0.4-bin/lib/commons-logging-1.1.3.jar",
                #     "/UCanAccess-4.0.4-bin/lib/hsqldb.jar",
                #     "/UCanAccess-4.0.4-bin/lib/jackcess-2.1.11.jar",
                # ]
                # classpath = ":".join(ucanaccess_jars)
                # conn = jaydebeapi.connect(
                #     "net.ucanaccess.jdbc.UcanaccessDriver",
                #     ["jdbc:ucanaccess://{0}".format(file_metadata_name_with_path), "", ""],
                #     classpath
                # )
            else:
                raise Exception('操作系统识别发生错误')

            cur = conn.cursor()  # 游标
            sql = "SELECT * FROM " + self.object_name
            cur.execute(sql)
            table_data = cur.fetchall()
            # total_rows = len(alldata)  # 行
            # total_cols = len(alldata[0])  # 列
            xml_obj = CXml()  # 建立xml对象
            node_root = xml_obj.new_xml('root')
            xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)  # 设置root节点与属性
            for field_index, row_obj in enumerate(cur.description):
                row_name = row_obj[0]  # 字段名称
                row_type = row_obj[1]  # 字段类型
                if row_type is bytearray:  # 跳过长二进制数组
                    continue
                node_item = xml_obj.create_element(node_root, 'item')
                xml_obj.set_attr(node_item, self.Name_Name, CUtils.any_2_str(row_name).lower())
                xml_obj.set_element_text(node_item, table_data[0][field_index])  # 设置item节点与属性与内容
        except Exception as error:
            raise Exception(error.__str__())
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return xml_obj

    def mat_to_xml(self, file_metadata_name_with_path: str):
        """
        完成 王学谦 mat文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的mat文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        text_list = CFile.file_2_list(file_metadata_name_with_path)  # 获取mat文件作为列表
        if (text_list is None) or CUtils.equal_ignore_case(CUtils.any_2_str(text_list), ''):
            raise  # 如果获取的文件内容为空，则抛出异常
        flag = False  # 设置标志

        xml_obj = CXml()  # 建立xml对象
        node_root = xml_obj.new_xml('root')
        xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)  # 设置root节点与属性
        for index, row_text in enumerate(text_list):
            if row_text.startswith('1\t'):  # 从开头为1+tab键的行开始录入
                flag = True
            row_list = re.split('\t+', row_text)  # 利用正则表达式，根据一个或多个tab剪切字符
            if flag:
                node_item = xml_obj.create_element(node_root, 'item')
                xml_obj.set_attr(node_item, self.Name_Name, CUtils.any_2_str(row_list[1]).lower())
                xml_obj.set_element_text(node_item, CUtils.any_2_str(row_list[2].strip()))  # 设置item节点与属性与内容
        if not flag:
            raise Exception('文件内容异常，无法正常识别文件开头')  # 如果未找到1+tab键开头，则抛出异常
        return xml_obj

    def xls_to_xml(self, file_metadata_name_with_path: str):
        """
         完成 王学谦 xls/xlsx文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象 by王学谦
        :param file_metadata_name_with_path:查询的xls/xlsx文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        all_data = xlrd.open_workbook(file_metadata_name_with_path)  # 获取表格所有内容
        table_data = all_data.sheets()[0]  # 默认获取第一个表格

        cols_num = table_data.ncols  # 获取列数
        rows_num = table_data.nrows  # 获取行数
        cols_index = 0  # 预定义列的index
        if CUtils.equal_ignore_case(CUtils.any_2_str(cols_num), CUtils.any_2_str(2)):
            pass  # 无序号列从1列开始
        elif CUtils.equal_ignore_case(CUtils.any_2_str(cols_num), CUtils.any_2_str(3)):
            cols_index = 1  # 有序号列从2列开始
        else:
            raise Exception('xls格式异常，无法正常解析')

        xml_obj = CXml()  # 建立xml对象
        node_root = xml_obj.new_xml('root')
        xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)  # 设置root节点与属性
        for row in range(0, rows_num):
            node_item = xml_obj.create_element(node_root, 'item')
            xml_obj.set_attr(node_item, self.Name_Name,
                             CUtils.any_2_str(table_data.cell(row, cols_index).value).lower())
            xml_obj.set_element_text(node_item, table_data.cell(row, cols_index + 1).value)  # 设置item节点与属性与内容
        return xml_obj


if __name__ == '__main__':
    pass
    # file_metadata_name_with_path = r'D:\wor\测试数据\数据入库3\DOM\湖北单个成果数据\H49G001026\H49G001026.mat'
