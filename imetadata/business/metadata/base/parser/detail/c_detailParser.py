# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:33 
# @Author : 王西亚 
# @File : c_detailParser.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.database.c_factory import CFactory


class CDetailParser(CParser):
    __detail_file_path__: str
    __detail_file_match_text__: str
    __detail_file_match_type__: int = CFile.MatchType_Common
    __detail_file_recurse__: bool = False

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据__detail_*变量的定义, 进行目录扫描, 记录到dm2_storage_object_detail中
        todo 负责人: 赵宇飞  内容:完成文件或子目录的扫描入库dm2_storage_object_detail
        :return:
        """
        if self.__detail_file_path__ == '':
            return CUtils.merge_result(self.Success, '附属目录为空, 表明无需处理附属文件, 处理结束!')

        sql_detail_delete = '''
            delete from dm2_storage_obj_detail where dodobjectid = '{0}'
        '''.format(self.__object_id__)

        sql_detail_insert = '''
            INSERT INTO dm2_storage_obj_detail(dodid, dodobjectid, dodfilename, dodfileext, dodfilesize, dodfileattr, dodfilecreatetime, dodfilemodifytime, dodlastmodifytime, dodstorageid, dodfilerelationname)
	            VALUES (:dodid, :dodobjectid, :dodfilename, :dodfileext, :dodfilesize, :dodfileattr, :dodfilecreatetime, :dodfilemodifytime, now(), :dodstorageid, :dodfilerelationname)
        '''

        sql_detail_insert_params_list = []
        list_file_name = CFile.file_or_subpath_of_path(self.__detail_file_path__, self.__detail_file_match_text__,
                                                       self.__detail_file_match_type__)
        print(self.__detail_file_match_type__)
        if self.__detail_file_match_text__:
            pass  # 循环递归文件夹，将文件解析出来，文件夹是否需要记录到detail表中，如果不需要，则需要将list_file_name中删除文件夹的记录，在下面的循环构建params中处理即可

        query_storage_id,query_filerelationname = self.get_storageid_and_filerelationname_by_objectid(self.__object_id__)
        for item_file_name_without_path in list_file_name:
            item_file_name_with_path = CFile.join_file(self.__detail_file_path__, item_file_name_without_path)
            CLogger().debug(item_file_name_with_path)
            params = dict()
            filerelationname = CFile.file_relation_path(item_file_name_with_path, self.__file_info__.__root_path__)
            file_ext = CFile.file_ext(item_file_name_with_path)
            if CUtils.equal_ignore_case(query_filerelationname,filerelationname):
                params['dodid'] = self.__object_id__   #有多个shp附件时候，仅根据后缀名判断会有问题：dodid会有重复，插入失败！
            else:
                params['dodid'] = CUtils.one_id()
            params['dodobjectid'] = self.__object_id__
            params['dodfilename'] = CFile.file_name(item_file_name_with_path)
            params['dodfileext'] = CFile.file_ext(item_file_name_with_path)
            params['dodfilesize'] = CFile.file_size(item_file_name_with_path)
            params['dodfileattr'] = 32
            params['dodfilecreatetime'] = CFile.file_create_time(item_file_name_with_path)
            params['dodfilemodifytime'] = CFile.file_modify_time(item_file_name_with_path)
            params['dodstorageid'] = query_storage_id
            params['dodfilerelationname'] = CFile.file_relation_path(item_file_name_with_path, self.__file_info__.__root_path__)
            sql_params_tuple = (sql_detail_insert, params)
            sql_detail_insert_params_list.append(sql_params_tuple)
        if len(sql_detail_insert_params_list) >0:
            CFactory().give_me_db(self.__db_server_id__).execute(sql_detail_delete)  #先删除detail表中对应的记录
            if not self.execute_batch(self.__db_server_id__,sql_detail_insert_params_list):
                return CUtils.merge_result(self.Failure, '处理失败!')
        return CUtils.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        super().custom_init()
        self.__detail_file_path__ = ''


    def get_storageid_and_filerelationname_by_objectid(self, objectid:str)-> (str,str):
        """
            根据对象id和文件类型(file/dir)获取存储id,文件或目录的名称
        @param objectid:
        @return:
        """
        if self.__file_info__.__file_type__ == self.FileType_File:
            sql_query_info = '''
                select dsfstorageid,dsffilerelationname from dm2_storage_file WHERE dm2_storage_file.dsf_object_id = :dsf_object_id
            '''
            ds = CFactory().give_me_db(self.__db_server_id__).one_row(sql_query_info, {'dsf_object_id': objectid})
            storage_id = ds.value_by_name(0, 'dsfstorageid', None)
            filerelationname = ds.value_by_name(0, 'dsffilerelationname', None)
            return storage_id,filerelationname
        elif self.__file_info__.__file_type__ == self.FileType_Dir:
            sql_query_info = '''
                SELECT dsdstorageid,dsddirectory  from dm2_storage_directory WHERE dsd_object_id = :dsd_object_id
            '''
            ds = CFactory().give_me_db(self.__db_server_id__).one_row(sql_query_info, {'dsd_object_id': objectid})
            storage_id = ds.value_by_name(0, 'dsdstorageid', None)
            directory = ds.value_by_name(0, 'dsddirectory', None)
            return storage_id,directory
        return '', ''

    def execute_batch(self, db_server_id: str, sql_params_tuple:[]) -> bool:
        """
         批处理事务执行
        @param db_server_id: 数据库服务器识别id
        @param sql_params_tuple: sql与dict参数组合的元组集合 [(sql1,dict_params1),(sql2,dict_params2)]
        @return:
        """
        engine = CFactory().give_me_db(db_server_id)
        session = engine.give_me_session()
        try:
            for sql, params in sql_params_tuple:
                engine.session_execute(session, sql, params)
            engine.session_commit(session)
            return True
        except Exception as error:
            CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__))
            engine.session_rollback(session)
            return False
        finally:
            engine.session_close(session)

if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    # meta_list = [('11','aa'),('11','bb'),('11','cc')]
    meta_list = []
    item1 = ('11','aa')
    item2 = ('11', 'bb')
    meta_list.append(item1)
    meta_list.append(item2)
    for key,value in meta_list:
        print('key={0},value={1}'.format(key,value))

