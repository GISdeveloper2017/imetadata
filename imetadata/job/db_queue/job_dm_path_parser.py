# -*- coding: utf-8 -*- 
# @Time : 2020/9/11 15:57 
# @Author : 王西亚 
# @File : job_dm_path_parser.py

from __future__ import absolute_import
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.job.c_dbBusJob import CDBBusJob
from imetadata.business.metadata.base.job.c_dmFileInfo import CDMFileInfo
from imetadata.business.metadata.base.job.c_dmPathInfo import CDMPathInfo
from imetadata.database.c_factory import CFactory
from imetadata.base.c_logger import CLogger


class job_dm_path_parser(CDBBusJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanfileprocessid = '{0}', dsdscanfilestatus = 2
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscanfilestatus = 1 
    and dsdscanstatus = 0  
    and dsd_directory_valid = -1
    and dsddirtype <> '2'
  order by dsddirscanpriority desc, dsdaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage.dstunipath as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirscanpriority as query_dir_scan_priority
  , dm2_storage_directory.dsdscanrule as query_dir_scanrule
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dstOtherOption as query_storage_OtherOption  
  , COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid)  as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid) 
where dm2_storage_directory.dsdscanfileprocessid = '{0}'
            '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanfilestatus = 1, dsdscanfileprocessid = null 
where dsdscanfilestatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_id = dataset.value_by_name(0, 'query_dir_id', '')

        # 将所有子目录, 文件的可用性, 都改为未知
        self.init_file_or_subpath_valid_unknown(ds_id)
        try:
            ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
            ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')

            if ds_subpath == '':
                ds_subpath = ds_root_path
            else:
                ds_subpath = CFile.join_file(ds_root_path, ds_subpath)
            CLogger().debug('处理的目录为: {0}'.format(ds_subpath))

            self.parser_path(dataset, ds_subpath)
        finally:
            self.exchange_file_or_subpath_valid_unknown2invalid(ds_id)

    def parser_path(self, dataset, ds_path):
        """
        处理目录(完整路径)下的子目录和文件
        :param ds_path:
        :return:
        """
        file_list = CFile.file_or_subpath_of_path(ds_path)
        for file_name in file_list:
            file_name_with_full_path = CFile.join_file(ds_path, file_name)

            if CFile.is_dir(file_name_with_full_path):
                CLogger().debug('在目录{0}下发现子目录: {1}'.format(ds_path, file_name))
                path_obj = CDMPathInfo(self.FileType_Dir, file_name_with_full_path,
                                       dataset.value_by_name(0, 'query_storage_id', ''),
                                       None,
                                       dataset.value_by_name(0, 'query_dir_id', ''),
                                       dataset.value_by_name(0, 'query_dir_parent_objid', ''),
                                       self.get_mission_db_id())

                if path_obj.white_black_valid():
                    path_obj.db_check_and_update()
                else:
                    CLogger().info('目录[{0}]未通过黑白名单检验, 不允许入库! '.format(file_name_with_full_path))
            elif CFile.is_file(file_name_with_full_path):
                CLogger().debug('在目录{0}下发现文件: {1}'.format(ds_path, file_name))
                file_obj = CDMFileInfo(self.FileType_File, file_name_with_full_path,
                                       dataset.value_by_name(0, 'query_storage_id', ''),
                                       None,
                                       dataset.value_by_name(0, 'query_dir_id', ''),
                                       dataset.value_by_name(0, 'query_dir_parent_objid', ''),
                                       self.get_mission_db_id())
                if file_obj.white_black_valid():
                    file_obj.db_check_and_update()
                    self.save_file(dataset, file_name_with_full_path)
                else:
                    CLogger().info('文件[{0}]未通过黑白名单检验, 不允许入库! '.format(file_name_with_full_path))

        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage_directory
            set dsdscandirstatus = 0, dsddirscanpriority = 0
            where dsdid = '{0}'
            '''.format(dataset.value_by_name(0, 'query_dir_id', ''))
        )
        return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_path))

    def save_subpath(self, dataset, file_name_with_path):
        """
        在这里将指定目录入库
        :param dataset: 数据集
        :param file_name_with_path: 完整路径的目录名
        :return:
        """
        storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_path_with_relation_path = CFile.file_relation_path(file_name_with_path, ds_root_path)

        # 判断目录下是否存在 metadata.rule文件,存在则获取内容、内容里面的类型(DEM/DOM/...)
        path_rule_str = None
        path_rule_type = None
        if CFile.file_or_path_exist(CFile.join_file(file_name_with_path, self.FileName_MetaData_Rule)):
            try:
                path_rule_str = CXml.file_2_str(
                    CFile.join_file(file_name_with_path, self.FileName_MetaData_Rule))
                # 解析rule文件获取type类型值
                xml_obj = CXml()
                xml_obj.load_xml(path_rule_str)
                node = xml_obj.xpath_one('/root/type')
                path_rule_type = xml_obj.get_element_text(node)
            except:
                path_rule = None

        sql_get_exist = '''
select dsdid as exist_dir_id, dsddirlastmodifytime
from dm2_storage_directory 
where dsddirectory = :dsdDirectory and dsdstorageid = :dsdStorageID
        '''

        params = dict()
        params['dsdDirectory'] = ds_path_with_relation_path
        params['dsdStorageID'] = storage_id
        dataset_existed = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_exist, params)
        if dataset_existed.is_empty():
            sql_insert = '''
            insert into dm2_storage_directory(
                dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype, dsdScanRule
                , dsddirectoryname, dsdpath, dsddircreatetime, dsddirlastmodifytime, dsdparentobjid
            ) VALUES(
                uuid_generate_v4(), :dsdparentid, :dsdstorageid, :dsddirectory, :dsddirtype, :dsdScanRule
                , :dsddirectoryname, :dsdpath, :dsddircreatetime, :dsddirlastmodifytime, :dsdparentobjid     
            ) 
            '''
            params = dict()
            params['dsdparentid'] = dataset.value_by_name(0, 'query_dir_id', '')
            params['dsdstorageid'] = storage_id
            params['dsddirectory'] = ds_path_with_relation_path
            params['dsddirtype'] = self.Dir_Type_Directory
            params['dsddirectoryname'] = CFile.file_name(file_name_with_path)
            params['dsdpath'] = CFile.file_path(ds_path_with_relation_path)
            params['dsddircreatetime'] = CFile.file_create_time(file_name_with_path)
            params['dsddirlastmodifytime'] = CFile.file_modify_time(file_name_with_path)
            params['dsdparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)
            params['dsdScanRule'] = path_rule_str

            CFactory().give_me_db(self.get_mission_db_id()).execute(sql_insert, params)
        else:
            # 数据库记录存在，则先判断记录中的ruletype值与文件rule的类型是否相同
            query_dir_scanrule = str(dataset_existed.value_by_name(0, 'query_dir_scanrule', None))
            if query_dir_scanrule != path_rule_type:
                '''
                   当数据库中的rule值与文件rule的值不一致时候， 删除当前目录下的所有子目录，文件 和对象
                   更新记录中的规则
                   设置子目录扫描状态为正常
                   直接返回
                '''

            else:
                file_m_date = CFile.file_modify_time(file_name_with_path)
                if file_m_date == str(dataset_existed.value_by_name(0, 'dsddirlastmodifytime', None)):
                    return CMetaDataUtils.merge_result(CMetaDataUtils.Success,
                                                       '目录[{0}]自上次入库后无变化, 本次将被忽略!'.format(file_name_with_path))
                else:
                    sql_update = '''
                    update dm2_storage_directory
                    set dsdparentid = :dsdparentid
                        , dsddirectory = :dsddirectory
                        , dsddirtype = :dsddirtype
                        , dsddirectoryname = :dsddirectoryname
                        , dsdpath = :dsdpath
                        , dsddircreatetime = :dsddircreatetime
                        , dsddirlastmodifytime = :dsddirlastmodifytime
                        , dsdparentobjid = :dsdparentobjid    
                    where dsdid = :dsdid
                    '''
                    params = dict()
                    params['dsdid'] = dataset_existed.value_by_name(0, 'exist_dir_id', '')
                    params['dsddirectory'] = ds_path_with_relation_path
                    params['dsdparentid'] = dataset.value_by_name(0, 'query_dir_id', '')
                    params['dsddirtype'] = self.Dir_Type_Directory
                    params['dsddirectoryname'] = CFile.file_name(file_name_with_path)
                    params['dsdpath'] = CFile.file_path(ds_path_with_relation_path)
                    params['dsddircreatetime'] = CFile.file_create_time(file_name_with_path)
                    params['dsddirlastmodifytime'] = CFile.file_modify_time(file_name_with_path)
                    params['dsdparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)

                    CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update, params)

    def save_file(self, dataset, file_name_with_path):
        """
        在这里将指定文件入库
        :param dataset: 数据集
        :param file_name_with_path: 完整路径的文件名
        :return:
        """
        storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_path_with_relation_path = CFile.file_relation_path(file_name_with_path, ds_root_path)

        sql_get_exist = '''
select dsfid as exist_file_id, dsffilemodifytime, dsffilesize
from dm2_storage_file
where dsffilerelationname = :dsfFileRelationName and dsfstorageid = :dsfStorageID
        '''

        params = dict()
        params['dsfFileRelationName'] = ds_path_with_relation_path
        params['dsfStorageID'] = storage_id
        dataset_existed = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_exist, params)
        if dataset_existed.is_empty():
            sql_insert = '''
            insert into dm2_storage_file(
                dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname
                , dsffilename, dsffilemainname, dsfext, dsffilecreatetime, dsffilemodifytime, dsf_object_type
                , dsffileattr, dsffilesize,  dsfparentobjid, dsflastmodifytime
            ) VALUES(
                uuid_generate_v4(), :dsfstorageid, :dsfdirectoryid, :dsffilerelationname
                , :dsffilename, :dsffilemainname, :dsfext, :dsffilecreatetime, :dsffilemodifytime, :dsf_object_type
                , :dsffileattr, :dsffilesize, :dsfparentobjid, now()       
            ) 
            '''
            params = dict()
            params['dsfstorageid'] = storage_id
            params['dsfdirectoryid'] = dataset.value_by_name(0, 'query_dir_id', '')
            params['dsffilerelationname'] = ds_path_with_relation_path
            params['dsffilename'] = CFile.file_name(file_name_with_path)
            params['dsffilemainname'] = CFile.file_main_name(file_name_with_path)
            params['dsfext'] = CFile.file_ext(file_name_with_path)
            params['dsffilecreatetime'] = CFile.file_create_time(file_name_with_path)
            params['dsffilemodifytime'] = CFile.file_modify_time(file_name_with_path)
            params['dsf_object_type'] = None
            params['dsffileattr'] = 32
            params['dsffilesize'] = CFile.file_size(file_name_with_path)
            params['dsfparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)

            CFactory().give_me_db(self.get_mission_db_id()).execute(sql_insert, params)
        else:
            file_m_date = CFile.file_modify_time(file_name_with_path)
            file_size = CFile.file_size(file_name_with_path)

            ''' 测试代码
            if file_m_date == str(dataset_existed.value_by_name(0, 'dsffilemodifytime', None)):
                print('相等{0} {1}'.format(file_m_date,dataset_existed.value_by_name(0, 'dsffilemodifytime', None)))
            else:
                print('不相等{0} {1}'.format(file_m_date,dataset_existed.value_by_name(0, 'dsffilemodifytime', None)))

            if file_size == int(dataset_existed.value_by_name(0, 'dsffilesize', 0)):
                print('相等{0} {1}'.format(file_m_date,dataset_existed.value_by_name(0, 'dsffilemodifytime', None)))
            else:
                print('不相等{0} {1}'.format(file_m_date,dataset_existed.value_by_name(0, 'dsffilemodifytime', None)))                
            '''

            # 根据文件修改时间、文件大小是否都相等判断文件是否需要更新
            if file_m_date == str(dataset_existed.value_by_name(0, 'dsffilemodifytime', None)) and str(
                    file_size) == str(dataset_existed.value_by_name(0, 'dsffilesize', 0)):
                return CMetaDataUtils.merge_result(CMetaDataUtils.Success,
                                                   '文件[{0}]自上次入库后无变化, 本次将被忽略!'.format(file_name_with_path))
            else:
                sql_update = '''
                update dm2_storage_file
                set dsfdirectoryid = :dsfdirectoryid
                    , dsffilecreatetime = :dsffilecreatetime
                    , dsffilemodifytime = :dsffilemodifytime                    
                    , dsffilename = :dsffilename
                    , dsffilemainname = :dsffilemainname
                    , dsfext = :dsfext                    
                    , dsflastmodifytime = now()
                    , dsffilesize = :dsffilesize  
                    , dsfparentobjid = :dsfparentobjid 
                where dsfid = :dsfid
                '''
                params = dict()
                params['dsfid'] = dataset_existed.value_by_name(0, 'exist_file_id', '')
                params['dsfdirectoryid'] = dataset.value_by_name(0, 'query_dir_id', '')
                params['dsffilecreatetime'] = CFile.file_create_time(file_name_with_path)
                params['dsffilemodifytime'] = CFile.file_modify_time(file_name_with_path)
                params['dsffilename'] = CFile.file_name(file_name_with_path)
                params['dsffilemainname'] = CFile.file_main_name(file_name_with_path)
                params['dsfext'] = CFile.file_ext(file_name_with_path)
                params['dsf_object_type'] = None
                params['dsffileattr'] = 32
                params['dsffilesize'] = CFile.file_size(file_name_with_path)
                params['dsfparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)

                CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update, params)

    def init_file_or_subpath_valid_unknown(self, ds_id):
        """
        将指定目录标识下的子目录和文件都更新为未知
        :param ds_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_directory
            set dsd_directory_valid = {0}
            where dsdparentid = :id
            '''.format(self.File_Status_Unknown), {'id': ds_id})
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_file
            set dsffilevalid = {0}
            where dsfdirectoryid = :id
            '''.format(self.File_Status_Unknown), {'id': ds_id})

    def exchange_file_or_subpath_valid_unknown2invalid(self, ds_id):
        """
        将指定目录标识下的子目录和文件中, 可用性为未知的, 都更新为不可用
        :param ds_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
                    update dm2_storage_directory
                    set dsd_directory_valid = {0}
                    where dsdparentid = :id and dsd_directory_valid = {1}
                    '''.format(self.File_Status_Invalid, self.File_Status_Unknown), {'id': ds_id})
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
                    update dm2_storage_file
                    set dsffilevalid = {0}
                    where dsfdirectoryid = :id and dsffilevalid = {1}
                    '''.format(self.File_Status_Invalid, self.File_Status_Unknown), {'id': ds_id})


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path_parser('', '').execute()
