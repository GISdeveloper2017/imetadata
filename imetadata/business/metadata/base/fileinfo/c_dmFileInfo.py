# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:33 
# @Author : 王西亚 
# @File : c_dmFileInfo.py
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class CDMFileInfo(CDMFilePathInfoEx):
    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        super().custom_init()
        engine = CFactory().give_me_db(self.db_server_id)
        if self.my_id is None:
            self._ds_file_or_path = engine.one_row('''
            select dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext, 
                dsffilecreatetime, dsffilemodifytime, dsffilevalid, 
                dsf_object_type, dsf_object_confirm, dsf_object_id, dsffilesize, dsfparentobjid, dsf_ib_id
            from dm2_storage_file
            where dsfstorageid = :dsfStorageID and dsfdirectoryid = :dsfDirectoryId and dsffilerelationname = :dsfFileRelationName
            ''', {'dsfStorageID': self.storage_id, 'dsfDirectoryId': self.parent_id,
                  'dsfFileRelationName': CFile.unify(self.file_name_with_rel_path)})
            if not self.ds_file_or_path.is_empty():
                self.my_id = self.ds_file_or_path.value_by_name(0, 'dsfid', None)
            if self.my_id is None:
                self.my_id = CUtils.one_id()
        else:
            self._ds_file_or_path = engine.one_row('''
                select dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext, 
                    dsffilecreatetime, dsffilemodifytime, dsffilevalid, 
                    dsf_object_type, dsf_object_confirm, dsf_object_id, dsffilesize, dsfparentobjid, dsf_ib_id
                from dm2_storage_file
                where dsfid = :dsfID
                ''', {'dsfid': self.my_id})

    def db_check_and_update(self, ib_id):
        """
        检查并更新dm2_storage_file表中记录
        :return:
        """
        if not self.ds_file_or_path.is_empty():
            # 如果记录已经存在
            db_file_modify_time = self.ds_file_or_path.value_by_name(0, 'dsddirlastmodifytime', '')
            db_file_size = self.ds_file_or_path.value_by_name(0, 'dsffilesize', 0)
            if CUtils.equal_ignore_case(CUtils.any_2_str(db_file_modify_time),
                                        CUtils.any_2_str(self.file_modify_time)) and (
                    db_file_size == self.file_size):
                CLogger().info('文件[{0}]的大小和最后修改时间, 和库中登记的没有变化, 文件将被设置为忽略刷新! '.format(self.file_name_with_full_path))
                CFactory().give_me_db(self.db_server_id).execute(
                    '''
                    update dm2_storage_file 
                    set dsfScanStatus = 0, dsffilevalid = -1, dsf_ib_id = :ib_id, dsfscanmemo = :message
                    where dsfid = :dsfid 
                    ''',
                    {
                        'dsfid': self.my_id,
                        'ib_id': ib_id,
                        'message': '文件[{0}]的大小和最后修改时间, 和库中登记的没有变化, 文件将被设置为忽略刷新! '.format(self.file_name_with_full_path)
                    }
                )
            else:
                CLogger().info('文件[{0}]的大小和最后修改时间, 和库中登记的有变化, 文件将被设置为重新刷新! '.format(self.file_name_with_full_path))
                CFactory().give_me_db(self.db_server_id).execute(
                    '''
                    update dm2_storage_file 
                    set dsfScanStatus = 1, dsffilevalid = -1, dsf_ib_id = :ib_id, dsfscanmemo = :message
                    where dsfid = :dsfid 
                    ''',
                    {
                        'dsfid': self.my_id,
                        'ib_id': ib_id,
                        'message': '文件[{0}]的大小和最后修改时间, 和库中登记的有变化, 文件将被设置为重新刷新! '.format(self.file_name_with_full_path)
                    }
                )
        else:
            CLogger().info('文件[{0}]未在库中登记, 系统将登记该记录! '.format(self.file_name_with_full_path))
            self.__db_insert(ib_id)

    def __db_insert(self, ib_id):
        """
        将当前目录, 创建一条新记录到dm2_storage_directory表中
        :return:
        """
        sql_insert = '''
        insert into dm2_storage_file(
            dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext
            , dsffilecreatetime, dsffilemodifytime, dsfaddtime, dsflastmodifytime, dsffilevalid
            , dsfscanstatus, dsfprocessid, dsf_object_type, dsf_object_confirm, dsf_object_id
            , dsffilesize, dsfparentobjid, dsf_ib_id) 
        values(
            :dsfid, :dsfstorageid, :dsfdirectoryid, :dsffilerelationname, :dsffilename, :dsffilemainname, :dsfext
            , :dsffilecreatetime, :dsffilemodifytime, now(), now(), -1
            , 1, null, null, 0, null
            , :dsffilesize, :dsfparentobjid, :dsf_ib_id)
        '''
        params = dict()
        params['dsfid'] = self.my_id
        params['dsfdirectoryid'] = self.parent_id
        params['dsfstorageid'] = self.storage_id
        params['dsffilerelationname'] = CFile.unify(self.file_name_with_rel_path)
        params['dsffilename'] = self.file_name_without_path
        params['dsffilemainname'] = self.file_main_name
        params['dsfext'] = self.file_ext
        params['dsffilecreatetime'] = self.file_create_time
        params['dsffilemodifytime'] = self.file_modify_time
        params['dsffilesize'] = self.file_size
        params['dsfparentobjid'] = self.owner_obj_id
        params['dsf_ib_id'] = ib_id
        CFactory().give_me_db(self.db_server_id).execute(sql_insert, params)

    def db_update_status_on_file_invalid(self):
        """
        标记当前文件的dsfFileValid=0无效
        :return:
        """
        sql_update_file_invalid = '''
            update dm2_storage_file
            set dsffilevalid = 0, dsfscanstatus = 0
            where dsfid = :dsfID
            '''
        CFactory().give_me_db(self.db_server_id).execute(sql_update_file_invalid, {'dsfID': self.my_id})

    def db_file2object(self):
        """
        :return:
        """
        db_object_confirm = self.ds_file_or_path.value_by_name(0, 'dsf_object_confirm',
                                                               self.Object_Confirm_IUnKnown)
        db_object_id = CUtils.one_id()
        if (db_object_confirm == self.Object_Confirm_IKnown) or (db_object_confirm == self.Object_Confirm_Maybe):
            db_object_size = self.ds_file_or_path.value_by_name(0, 'dsffilesize', 0)
            db_path_modify_time = self.ds_file_or_path.value_by_name(0, 'dsffilemodifytime', '')
            if CUtils.equal_ignore_case(CUtils.any_2_str(db_path_modify_time),
                                        CUtils.any_2_str(self.file_modify_time)) and (
                    db_object_size == self.file_size):
                CLogger().info('文件[{0}]的大小和最后修改时间, 和库中登记的都没有变化, 对象识别将被忽略! '.format(self.file_name_with_full_path))
                return
            else:
                # 删除对象记录, 清理对象字段
                db_object_id = self.ds_file_or_path.value_by_name(0, 'dsf_object_id', '')
                db_object_type = self.ds_file_or_path.value_by_name(0, 'dsf_object_type', '')
                CLogger().debug(
                    '系统发现文件[{0}]的大小或最后修改时间有变化, 将删除它关联的对象{1}.{2}, 重新识别'.format(
                        self.file_main_name,
                        db_object_type,
                        db_object_id
                    )
                )
                self.db_delete_object_by_id(db_object_id)

        object_confirm = self.Object_Confirm_IUnKnown
        object_name = None
        object_type = None
        classified_obj = CPluginsMng.plugins_classified(self)
        if classified_obj is not None:
            object_confirm = classified_obj.classified_object_confirm()
            object_name = classified_obj.classified_object_name()
            object_type = classified_obj.get_id()

        if (object_confirm == self.Object_Confirm_IUnKnown) or (object_confirm == self.Object_Confirm_IKnown_Not):
            sql_update_file_object = '''
                update dm2_storage_file
                set dsf_object_confirm = :dsf_object_confirm, dsf_object_id = null, dsf_object_type = null
                    , dsffilevalid = -1, dsffilesize = :dsfFileSize, dsffilemodifytime = :fileModifyTime
                where dsfid = :dsfid
                '''
            CFactory().give_me_db(self.db_server_id).execute(
                sql_update_file_object,
                {
                    'dsfid': self.my_id,
                    'dsf_object_confirm': object_confirm,
                    'dsfFileSize': self.file_size,
                    'fileModifyTime': CUtils.any_2_str(self.file_modify_time)
                }
            )
        else:
            sql_insert_object = '''
                insert into dm2_storage_object(dsoid, dsoobjectname, dsoobjecttype, dsodatatype, dsoalphacode, dsoaliasname, dsoparentobjid, dso_ib_id) 
                values(:dsoid, :dsoobjectname, :dsoobjecttype, :dsodatatype, :dsoalphacode, :dsoaliasname, :dsoparentobjid, :dso_ib_id)
                '''

            new_dso_id = db_object_id

            sql_update_file_object = '''
                update dm2_storage_file
                set dsf_object_confirm = :dsf_object_confirm, dsf_object_id = :dsf_object_id, dsf_object_type = :dsf_object_type
                    , dsffilevalid = -1, dsffilesize = :dsfFileSize, dsffilemodifytime = :fileModifyTime
                where dsfid = :dsfid
                '''

            engine = CFactory().give_me_db(self.db_server_id)
            session = engine.give_me_session()
            try:
                params = dict()
                params['dsoid'] = new_dso_id
                params['dsoobjectname'] = object_name
                params['dsoobjecttype'] = object_type
                params['dsodatatype'] = self.FileType_File
                params['dsoalphacode'] = CUtils.alpha_text(object_name)
                params['dsoaliasname'] = object_name
                params['dsoparentobjid'] = self.owner_obj_id
                params['dso_ib_id'] = self.ds_file_or_path.value_by_name(0, 'dsf_ib_id', None)
                engine.session_execute(session, sql_insert_object, params)

                params = dict()
                params['dsfid'] = self.my_id
                params['dsf_object_confirm'] = object_confirm
                params['dsf_object_id'] = new_dso_id
                params['dsf_object_type'] = object_type
                params['dsfFileSize'] = self.file_size
                params['fileModifyTime'] = CUtils.any_2_str(self.file_modify_time)
                engine.session_execute(session, sql_update_file_object, params)

                engine.session_commit(session)
            except Exception as error:
                CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__()))
                engine.session_rollback(session)
            finally:
                engine.session_close(session)
