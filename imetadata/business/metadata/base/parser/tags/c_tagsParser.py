# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:05 
# @Author : 王西亚 
# @File : c_tagsParser.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.database.c_factory import CFactory


class CTagsParser(CParser):
    """
    对标签进行处理
    """

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx, tags_parser_rule):
        super().__init__(object_id, object_name, file_info)
        self._tags_parser_rule = tags_parser_rule

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据tags_parser_rule的定义, 进行标签识别
        :return:
        """
        # 调用父类方法
        super().process()

        if not isinstance(self._tags_parser_rule, list):
            return CResult.merge_result(self.Failure, '标签解析规则必须是一个数组, 您的配置有误, 请检查!')

        error_list = []
        for tags_parser in self._tags_parser_rule:
            catalog = CUtils.any_2_str(CUtils.dict_value_by_name(tags_parser, self.Name_Catalog, ''))
            tag_field_name = CUtils.any_2_str(CUtils.dict_value_by_name(tags_parser, self.Name_Tag, ''))
            keyword_field_list = CUtils.dict_value_by_name(tags_parser, self.Name_Keyword, None)
            data_sample = CUtils.any_2_str(CUtils.dict_value_by_name(tags_parser, self.Name_Data_Sample, ''))
            separator = CUtils.dict_value_by_name(tags_parser, self.Name_Separator, None)
            enable = CUtils.dict_value_by_name(tags_parser, self.Name_Enable, True)

            if not enable:
                continue

            if CUtils.equal_ignore_case(tag_field_name, ''):
                continue

            if CUtils.equal_ignore_case(catalog, ''):
                continue

            if keyword_field_list is None:
                continue

            if len(keyword_field_list) == 0:
                continue

            if CUtils.equal_ignore_case(data_sample, self.Tag_DataSample_MainName):
                tag_data_sample_str = CUtils.any_2_str(self.file_info.file_main_name)
            elif CUtils.equal_ignore_case(data_sample, self.Tag_DataSample_RelationPath):
                tag_data_sample_str = CUtils.any_2_str(self.file_info.file_path_with_rel_path)
            else:
                tag_data_sample_str = CUtils.any_2_str(self.file_info.file_main_name_with_rel_path)

            try:
                tag_data_sample_list = CUtils.split(tag_data_sample_str, separator)
                self.process_tag(catalog, tag_field_name, keyword_field_list, tag_data_sample_list)
            except Exception as error:
                error_list.append(
                    '对象[{0}]在处理标签库[{1}]分类[{2}]有误, 详细错误信息为: {3}'.format(
                        self.object_name,
                        catalog,
                        tag_data_sample_str,
                        error.__str__()
                    )
                )

        if len(error_list) == 0:
            return CResult.merge_result(self.Success,
                                        '文件或目录[{0}]对象业务分类解析成功完成!'.format(self.file_info.file_main_name_with_rel_path))
        else:
            error_message = '文件或目录[{0}]的业务分类解析处理完毕, 但解析过程中出现了错误, 具体如下: \n'.format(
                self.file_info.file_main_name_with_rel_path)
            for error_str in error_list:
                error_message = CUtils.str_append(error_message, error_str)

            return CResult.merge_result(self.Success, error_message)

    def process_tag(self, sql_query_tag: str, tag_field_name: str, keyword_field_list: list, data_sample_list: list):
        """
        绑定标签tag, 注意sql查询的第一个字段为id
        :param sql_query_tag: 标签库SQL查询语句
        :param keyword_field_list: 关键字字段名称
        :param tag_field_name: 标签标示字段名
        :param data_sample_list: 待匹配列表
        :return:
        """
        ds = CFactory().give_me_db(self.file_info.db_server_id).all_row(sql_query_tag)

        if ds.is_empty():
            return

        for row_index in range(ds.size()):
            tag_value = ds.value_by_name(row_index, tag_field_name, '')

            if CUtils.equal_ignore_case(tag_value, ''):
                continue

            tag_should_append = False
            for keyword_field in keyword_field_list:
                keyword_value = ds.value_by_name(row_index, keyword_field, '')
                if CUtils.equal_ignore_case(tag_value, ''):
                    continue
                if CUtils.list_count(data_sample_list, keyword_value) > 0:
                    tag_should_append = True

            if tag_should_append:
                self.update_object_tags(self.object_id, tag_value)

    def update_object_tags(self, object_id: str, tag_value: str):
        """
        通用方法：事务处理，更新对象的标签
        @param object_id:
        @param tag_value:
        @return:
        """
        in_db_tag_value = tag_value
        in_db_tag_value = in_db_tag_value.replace('"', '')
        in_db_tag_value = in_db_tag_value.replace("'", '')
        CFactory().give_me_db(self.file_info.db_server_id).execute(
            '''
            UPDATE dm2_storage_object 
            SET dsotags = array_append(array_remove(dsotags, '{0}'), '{0}'),
                dsolastmodifytime = now() 
            WHERE dsoid = :dsoid
            '''.format(in_db_tag_value),
            {'dsoid': object_id}
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    # tags_parser_text = r'县界'
    tags_parser_text = r'县界_昆明市-2019-2018 2017'
    # 标签分隔符
    tags_parser_split_list: list = ['\\', '_', '/', '-', ' ']
    text_part_list = CUtils.split(tags_parser_text, tags_parser_split_list)
    for item in text_part_list:
        print(item)
