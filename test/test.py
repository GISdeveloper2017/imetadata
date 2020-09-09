#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Li'guang


from imetadata.base.c_file import CFile
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob
from imetadata.base.c_logger import CLogger
from sqlalchemy import text


if __name__ == "__main__":
    storage_root_path = '/Users/wangxiya/Documents/交换/1.给我的/生态审计/产品样例数据-昆明矢量/基础地理信息/市界'
    sql_update_root_storage_dir = '''
            update1 dm2_storage_directory
            set dsdParentID = '-1', dsdDirectory = :dsdDirectory, dsdDirtype = 3
                , dsdDirectoryName = '', dsdPath = ''
                , dsdDirCreateTime = :dsddircreatetime, dsdDirLastModifyTime = :dsddirlastmodifytime
                , dsdLastModifyTime = Now()
            where dsdStorageId = :dsdStorageID and dsdid = :dsdID
            '''

    params = dict()
    params['dsdDircreatetime'] = CFile.file_modify_time(storage_root_path)
    params['dsdDirlastmodifytime'] = CFile.file_modify_time(storage_root_path)
    params['DSDDIRECTORY'] = 'Haha'
    params['DSDSTORAGEID'] = 1
    params['DSDID'] = 1

    factory = CFactory()
    db = factory.give_me_db('0')
    statement = text(sql_update_root_storage_dir)
    exe_params = statement.compile(db.engine()).params
    exe_params_names = exe_params.keys()
    new_params = dict()
    for exe_param_name in exe_params_names:
        exe_param_value = CMetaDataUtils.dict_value_by_name(params, exe_param_name)
        if exe_param_value is not None:
            new_params[exe_param_name] = str(exe_param_value)
        else:
            new_params[exe_param_name] = None

    db.execute(sql_update_root_storage_dir, new_params)
