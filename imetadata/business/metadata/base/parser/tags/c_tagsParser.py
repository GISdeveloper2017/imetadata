# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:05 
# @Author : 王西亚 
# @File : c_tagsParser.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.database.c_factory import CFactory


class CTagsParser(CParser):
    """
    对标签进行处理
    """
    # 标签识别用的字符串
    __tags_parser_text__: str
    # 标签分隔符
    __tags_parser_split_list__: list = ['\\', '_', '/', '-', ' ']

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据__tags_*变量的定义, 进行标签识别
        todo(赵宇飞)  内容:完成文件或子目录标签识别, 保存dm2_storage_object.dsoTags中
        对__tags_parser_text__进行分隔符拆解
        对拆解的每一部分, 匹配ro_global_dim_xxx表中的记录
        :return:
        """
        # 调用父类方法
        super().process()

        sql_tag_custom = '''
            SELECT
                gdcid AS ID,
                gdctitle AS title
            FROM
                ro_global_dim_custom
        '''

        sql_tag_custom_bus = '''
              SELECT
                  gdcbid AS ID,
                  gdcbtitle AS title,
                  gdcbquickcode as quickcode
              FROM
                  ro_global_dim_custom_bus
          '''

        sql_tag_time = '''
            SELECT
                gdtid AS id,
                gdttitle AS title,
                gdtquickcode AS quickcode 
            FROM
                ro_global_dim_time
        '''

        sql_tag_space = '''
            SELECT
                gdsid AS ID,
                gdstitle AS title,
                gdsquickcode AS quickcode 
            FROM
                ro_global_dim_space
        '''

        # 将__tags_parser_text__进行拆分成数组
        text_part_list = CUtils.split(self.__tags_parser_text__, self.__tags_parser_split_list__)
        # 1.绑定tag_custom
        process_result = self.process_tag(sql_tag_custom, text_part_list)
        if not CResult.result_success(process_result):
            return process_result

        # 2.绑定tag_custom_bus
        process_result = self.process_tag(sql_tag_custom_bus, text_part_list)
        if not CResult.result_success(process_result):
            return process_result

        # 3.绑定tag_time
        process_result = self.process_tag(sql_tag_time, text_part_list)
        if not CResult.result_success(process_result):
            return process_result

        # 4.绑定tag_space
        process_result = self.process_tag(sql_tag_space, text_part_list)
        if not CResult.result_success(process_result):
            return process_result
        return CResult.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        """
        自定义初始化
        对标签识别用的字符串进行设置
        :return:
        """
        super().custom_init()
        self.__tags_parser_text__ = ''

    def process_tag(self, sql_query_tag: str, text_part_list: list) -> str:
        """
        绑定标签tag, 注意sql查询的第一个字段为id
        @param sql_query_tag:
        @param text_part_list:
        @return:
        """
        list_tag_id = []
        ds = CFactory().give_me_db(self.file_info.db_server_id).all_row(sql_query_tag)
        if not ds.is_empty():
            field_count = ds.field_count()
            for row_index in range(ds.size()):
                tag_id = ds.value_by_index(row_index, 0, "")  # 取出id值
                check_exist = False
                for field_index in range(field_count):
                    if field_index == 0:
                        continue
                    field_value = ds.value_by_index(row_index, field_index, "")
                    if text_part_list.__contains__(CUtils.any_2_str(field_value)):
                        check_exist = True
                if check_exist:
                    list_tag_id.append(tag_id)
            if len(list_tag_id) > 0:
                process_result = self.update_object_tags(self.object_id, list_tag_id)
                return process_result
        return CResult.merge_result(self.Success, '处理完毕!')

    def update_object_tags(self, object_id: str, list_tag_id: list) -> str:
        """
        通用方法：事务处理，更新对象的标签
        @param object_id:
        @param list_tag_id:
        @return:
        """
        if len(list_tag_id) == 0:
            return
        sql_update_object_tag = '''
            UPDATE dm2_storage_object 
            SET dsotags = array_append(array_remove (dsotags,  '{0}'), '{0}'),
            dsolastmodifytime = now( ) 
            WHERE
                dsoid = :dsoid;
        '''
        sql_tag_update_list = []
        for tag_id in list_tag_id:
            params = dict()
            params['dsoid'] = object_id
            sql_temp = sql_update_object_tag.format(tag_id)
            sql_tag_update_tuple = (sql_temp, params)
            sql_tag_update_list.append(sql_tag_update_tuple)
        if len(sql_tag_update_list) > 0:
            if not CFactory().give_me_db(self.file_info.db_server_id).execute_batch(sql_tag_update_list):
                return CResult.merge_result(self.Failure, '处理失败!')
        return CResult.merge_result(self.Success, '处理完毕!')


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
