# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:33 
# @Author : 王西亚 
# @File : c_detailParser.py
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.database.c_factory import CFactory
import os


class CDetailParser(CParser):
    __detail_file_path__: str
    __detail_file_match_text__: str
    __detail_file_match_type__: int = CFile.MatchType_Common
    __detail_file_recurse__: bool = False

    _file_custom_list: list

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx, file_custom_list: list):
        super().__init__(object_id, object_name, file_info)
        self._file_custom_list = file_custom_list

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据__detail_*变量的定义, 进行目录扫描, 记录到dm2_storage_object_detail中
        :return:
        """
        self._before_process()

        if not CUtils.equal_ignore_case(self.__detail_file_path__, ''):
            list_file_fullname = CFile.file_or_dir_fullname_of_path(
                self.__detail_file_path__,
                self.__detail_file_recurse__,
                self.__detail_file_match_text__,
                self.__detail_file_match_type__)
            result = self.__inbound_object_detail_of_schema(list_file_fullname)
            if not CResult.result_success(result):
                return result

        if len(self._file_custom_list) > 0:
            return self.inbound_object_detail_of_custom(self._file_custom_list)
        else:
            return CResult.merge_result(self.Success, '对象附属文件处理成功结束!')

    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        super().custom_init()
        self.__detail_file_path__ = ''

    def inbound_object_detail_of_custom(self, list_file_fullname):
        if len(list_file_fullname) == 0:
            return CResult.merge_result(self.Success, '自定义列表为空, 无需入库, 正常结束! ')

        return self.__inbound_object_detail_of_schema(list_file_fullname)

    def __inbound_object_detail_of_schema(self, list_file_fullname):
        # sql_detail_insert = '''
        # INSERT INTO dm2_storage_obj_detail(
        #     dodid, dodobjectid, dodfilename, dodfileext, dodfilesize,
        #     dodfilecreatetime, dodfilemodifytime,
        #     dodlastmodifytime, dodstorageid, dodfilerelationname, dodfiletype)
        # VALUES (
        #     :dodid, :dodobjectid, :dodfilename, :dodfileext, :dodfilesize,
        #     :dodfilecreatetime, :dodfilemodifytime, now(),
        #     :dodstorageid, :dodfilerelationname, :dodfiletype)
        # '''
        sql_detail_insert = '''
        INSERT INTO dm2_storage_obj_detail(
            dodid, dodobjectid, dodfilename, dodfileext, dodfilesize, 
            dodfilecreatetime, dodfilemodifytime, 
            dodlastmodifytime, dodfiletype)
        VALUES (
            :dodid, :dodobjectid, :dodfilename, :dodfileext, :dodfilesize, 
            :dodfilecreatetime, :dodfilemodifytime, now(), 
            :dodfiletype)
        '''

        sql_detail_insert_params_list = []

        query_storage_id = self.file_info.storage_id
        query_file_relation_name = self.file_info.file_name_with_rel_path
        for item_file_name_with_path in list_file_fullname:
            CLogger().debug(item_file_name_with_path)
            if not CFile.file_or_path_exist(item_file_name_with_path):
                continue

            params = dict()
            file_relation_name = CFile.file_relation_path(item_file_name_with_path, self.file_info.root_path)
            (root_path_to_storage, inbound_name) = os.path.split(self.file_info.root_path)
            if CUtils.equal_ignore_case(query_file_relation_name, file_relation_name):
                params['dodid'] = self.object_id
            else:
                params['dodid'] = CUtils.one_id()
            # 文件类型
            params['dodfiletype'] = self.FileType_File
            if CFile.is_dir(item_file_name_with_path):
                params['dodfiletype'] = self.FileType_Dir
            params['dodobjectid'] = self.object_id
            params['dodfilename'] = CFile.unify(
                CFile.file_relation_path(
                    item_file_name_with_path,
                    root_path_to_storage
                )
            )
            params['dodfileext'] = CFile.file_ext(item_file_name_with_path)
            params['dodfilesize'] = CFile.file_size(item_file_name_with_path)
            params['dodfilecreatetime'] = CFile.file_create_time(item_file_name_with_path)
            params['dodfilemodifytime'] = CFile.file_modify_time(item_file_name_with_path)
            # params['dodstorageid'] = query_storage_id
            # params['dodfilerelationname'] = CFile.file_relation_path(
            #     item_file_name_with_path,
            #     self.file_info.root_path)
            sql_params_tuple = (sql_detail_insert, params)
            sql_detail_insert_params_list.append(sql_params_tuple)

        if len(sql_detail_insert_params_list) > 0:
            try:
                CFactory().give_me_db(self.file_info.db_server_id).execute_batch(sql_detail_insert_params_list)
            except Exception as error:
                CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__()))
                return CResult.merge_result(self.Failure, '处理失败!')
        return CResult.merge_result(self.Success, '处理完毕!')

    def _before_process(self):
        sql_detail_delete = '''
            delete from dm2_storage_obj_detail where dodobjectid = '{0}'
        '''.format(self.object_id)
        CFactory().give_me_db(self.file_info.db_server_id).execute(sql_detail_delete)  # 先删除detail表中对应的记录


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    # meta_list = [('11','aa'),('11','bb'),('11','cc')]
    meta_list = []
    item1 = ('11', 'aa')
    item2 = ('11', 'bb')
    meta_list.append(item1)
    meta_list.append(item2)
    for key, value in meta_list:
        print('key={0},value={1}'.format(key, value))
