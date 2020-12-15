# -*- coding: utf-8 -*- 
# @Time : 2020/12/15 07:58 
# @Author : 王西亚 
# @File : c_dataTransfer.py

from imetadata.base.c_dataSetSeqReader import CDataSetSeqReader
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.c_dbDataSetSeqReader import CDBDataSetSeqReader
from imetadata.database.tools.c_table import CTable
from imetadata.tool.datasets.c_vectorDataSets import CVectorDataSets


class CDataImport(CResource):
    """
    实现数据的导入
    . 源: 数据序列读取类
    . 目标: 数据表

    初始化配置: 字典
    具体格式如下:
    {
        'source': {
            'type': 'vector',
            'type_comment': 'shapefile-单层shp矢量文件; vector_dataset-多层矢量数据集, 如gdb,mdb; table-数据表; query-数据查询',
            'shapefile': {
                'name': '/aa/bb/cc.shp'
            },
            'vector_dataset': {
                'name': '/aa/bb/cc.gdb',
                'layer': 'ee'
            },
            'table': {
                'database': '0',
                'name': 'dm2_storage'
            },
            'query': {
                'database': '0',
                'sql': 'select * from dm2_storage'
            }
        },
        'target': {
            'database': '0',
            'name': 'dm2_storage'
        },
        'pipe': [
            {
                'field': 'dstid',
                'type': 'common',
                'value': '$(source_field_name)'
            },
            {
                'field': 'geom',
                'type': 'spatial',
                'value': '$(source_field_name)',
                'srid': 4326
            },
            {
                'field': 'tags',
                'type': 'array',
                'value': '$(source_field_name)'
            }
        ],
        'option': {
            'same_field_name_match': True
        }
    }
    """

    def __init__(self, config: dict, params: dict = None):
        super().__init__()
        self.__config = config
        self.__params = params
        self.__source_data = None
        self.__target_table = None

    def config(self):
        return self.__config

    def params(self):
        return self.__params

    def replace_placeholder(self, text: str, safe: bool = True):
        return CUtils.replace_placeholder(text, self.__params, safe)

    def process(self) -> str:
        try:
            data_source = self.open_source()
            data_target = self.open_target()
            return self.import_data(data_source, data_target)
        except Exception as error:
            result_message = '数据导出过程出现错误, 详细错误为: {0}'.format(error.__str__())
            CLogger().debug(result_message)
            return CResult.merge_result(self.Failure, result_message)

    def open_source(self) -> CDataSetSeqReader:
        option_source = CUtils.dict_value_by_name(self.__config, self.Name_Source, None)
        if option_source is None:
            raise Exception('数据源未设置, 请检查修正后重试! ')

        type_source = CUtils.dict_value_by_name(option_source, self.Name_Type, self.Name_Table)
        if CUtils.equal_ignore_case(type_source, self.Name_ShapeFile):
            source_data_option = CUtils.dict_value_by_name(option_source, type_source, None)
            source_data_filename = CUtils.dict_value_by_name(source_data_option, self.Name_Name, None)
            if CUtils.equal_ignore_case(source_data_filename, ''):
                raise Exception('[{0}]类型数据源未设置文件名, 请检查修正后重试! '.format(type_source))
            if not CFile.file_or_path_exist(source_data_filename):
                raise Exception('[{0}]类型数据源设置的文件[{1}]不存在, 请检查修正后重试! '.format(type_source, source_data_filename))

            cpg_file_name = CFile.change_file_ext(source_data_filename, 'cpg')
            encoding = CResource.Encoding_GBK
            if CFile.file_or_path_exist(cpg_file_name):
                encoding = CFile.file_2_str(cpg_file_name)

            self.__source_data = CVectorDataSets(source_data_filename)
            self.__source_data.open(encoding)
            return self.__source_data.layer_by_index(0)
        elif CUtils.equal_ignore_case(type_source, self.Name_Vector_DataSet):
            source_data_option = CUtils.dict_value_by_name(option_source, type_source, None)
            source_data_filename = CUtils.dict_value_by_name(source_data_option, self.Name_Name, None)
            source_data_layer = CUtils.dict_value_by_name(source_data_option, self.Name_Layer, None)
            if CUtils.equal_ignore_case(source_data_filename, ''):
                raise Exception('[{0}]类型数据源未设置文件名, 请检查修正后重试! '.format(type_source))
            if CUtils.equal_ignore_case(source_data_layer, ''):
                raise Exception('[{0}]类型数据源未设置图层名, 请检查修正后重试! '.format(type_source))
            if not CFile.file_or_path_exist(source_data_filename):
                raise Exception('[{0}]类型数据源设置的文件[{1}]不存在, 请检查修正后重试! '.format(type_source, source_data_filename))

            self.__source_data = CVectorDataSets(source_data_filename)
            self.__source_data.open()
            layer_data = self.__source_data.layer_by_name(source_data_layer)
            if layer_data is None:
                raise Exception('[{0}]类型数据源设置的图层[{1}]不存在, 请检查修正后重试! '.format(type_source, source_data_layer))
            return layer_data
        elif CUtils.equal_ignore_case(type_source, self.Name_Table):
            source_data_option = CUtils.dict_value_by_name(option_source, type_source, None)
            source_database = CUtils.dict_value_by_name(source_data_option, self.Name_DataBase,
                                                        self.DB_Server_ID_Default)
            source_data_table_name = CUtils.dict_value_by_name(source_data_option, self.Name_Name, None)
            if CUtils.equal_ignore_case(source_data_table_name, ''):
                raise Exception('[{0}]类型数据源未设置数据表名, 请检查修正后重试! '.format(self.Name_Table))

            data_set = CFactory().give_me_db(source_database).all_row(
                'select * from {0}'.format(self.replace_placeholder(source_data_table_name)),
                self.__params
            )
            self.__source_data = CDBDataSetSeqReader(data_set)
            return self.__source_data
        elif CUtils.equal_ignore_case(type_source, self.Name_Table):
            source_data_option = CUtils.dict_value_by_name(option_source, type_source, None)
            source_database = CUtils.dict_value_by_name(source_data_option, self.Name_DataBase,
                                                        self.DB_Server_ID_Default)
            source_data_sql = CUtils.dict_value_by_name(source_data_option, self.Name_SQL, None)
            if CUtils.equal_ignore_case(source_data_sql, ''):
                raise Exception('[{0}]类型数据源未设置查询语句, 请检查修正后重试! '.format(type_source))

            data_set = CFactory().give_me_db(source_database).all_row(
                self.replace_placeholder(source_data_sql),
                self.__params
            )
            self.__source_data = CDBDataSetSeqReader(data_set)
            return self.__source_data
        else:
            raise Exception('系统不支持类型为[{0}]的数据源, 请检查修正后重试! '.format(type_source))

    def open_target(self) -> CTable:
        option_target = CUtils.dict_value_by_name(self.__config, self.Name_Target, None)
        if option_target is None:
            raise Exception('导入目标未设置, 请检查修正后重试! ')

        target_database = CUtils.dict_value_by_name(option_target, self.Name_DataBase, self.DB_Server_ID_Default)
        target_data_table_name = CUtils.dict_value_by_name(option_target, self.Name_Name, None)
        if CUtils.equal_ignore_case(target_data_table_name, ''):
            raise Exception('导入目标未设置数据表名, 请检查修正后重试! ')

        table_obj = CTable()
        table_obj.load_info(target_database, target_data_table_name)
        return table_obj

    def import_data(self, data_source: CDataSetSeqReader, data_target: CTable) -> str:
        success_record_count = 0

        if not data_source.first():
            return CResult.merge_result(
                self.Success,
                '数据源无有效导入数据, 系统自动设定导入成功! '
            )

        while True:
            result = self.__import_each_record(data_source, data_target)
            if not CResult.result_success(result):
                return result

            success_record_count = success_record_count + 1

            if not data_source.next():
                break

        return CResult.merge_result(
            self.Success,
            '数据源的全部数据导入成功, 共导入记录数[{0}]! '.format(success_record_count)
        )

    def __import_each_record(self, data_source: CDataSetSeqReader, data_target: CTable) -> str:
        data_target.column_list.reset()
        for column_index in range(data_target.column_list.size()):
            column_obj = data_target.column_list.column_by_index(column_index)
            column_name = column_obj.name
