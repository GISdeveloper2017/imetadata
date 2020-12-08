# -*- coding: utf-8 -*- 
# @Time : 2020/10/27 14:39
# @Author : 赵宇飞
# @File : c_mdTransformerThirdSurvey.py
import pypyodbc

from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerThirdSurvey(CMDTransformer):
    """
    完成 王学谦  三调mdb里多表 转 业务元数据xml文件
    """

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

    def mdb_to_xml(self, file_metadata_name_with_path: str):
        """
         TODO 王学谦 mdb文件转xml,在函数外提前定义xml对象并获取父节点传入，函数会将通过父节点构造xml对象
        :param file_metadata_name_with_path:查询的mdb文件全名，带路径
        :return xml_obj:将文件内容存储好的项目对象
        """
        conn = None  # 预定义连接与游标，方便释放
        cur = None
        try:
            try:
                if CUtils.equal_ignore_case(CSys.get_os_name(), self.OS_Windows):
                    mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};' + 'DBQ={0}'.format(
                        file_metadata_name_with_path)  # win驱动，安装AccessDatabaseEngine_X64.exe驱动
                    conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
                elif CUtils.equal_ignore_case(CSys.get_os_name(), self.OS_Linux):
                    conn = pypyodbc.connect('DSN=mymdb')  # linux配置，需要配置mdbtools, unixODBC, libmdbodbc
                else:
                    raise Exception('操作系统识别发生错误')
            except Exception as error:
                raise Exception('mdb解析驱动异常:'+error.__str__())

            cur = conn.cursor()  # 游标

            xml_obj = CXml()  # 建立xml对象
            node_root = xml_obj.new_xml('root')
            xml_obj.set_attr(node_root, self.Name_Type, self.transformer_type)  # 设置root节点与属性

            table_name_list = ['mbii', 'mpid', 'mppi', 'mqc1', 'mqc2', 'mdac']
            for table_name in table_name_list:
                try:
                    sql = "SELECT * FROM " + table_name
                    cur.execute(sql)
                    table_data = cur.fetchall()
                    # total_rows = len(alldata)  # 行
                    # total_cols = len(alldata[0])  # 列

                    node_property = xml_obj.create_element(node_root, 'property')
                    xml_obj.set_attr(node_property, 'tablename', table_name)  # 设置property节点与属性与内容
                    for field_index, row_obj in enumerate(cur.description):
                        row_name = row_obj[0]  # 字段名称
                        row_type = row_obj[1]  # 字段类型
                        if row_type is bytearray:  # 跳过长二进制数组
                            continue
                        node_item = xml_obj.create_element(node_property, 'item')
                        xml_obj.set_attr(node_item, self.Name_Name, CUtils.any_2_str(row_name).lower())
                        xml_obj.set_element_text(node_item, table_data[0][field_index])  # 设置item节点与属性与内容
                except:
                    continue
        except Exception as error:
            raise Exception(error.__str__())
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return xml_obj
