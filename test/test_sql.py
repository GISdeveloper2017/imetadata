# -*- coding: utf-8 -*- 
# @Time : 2020/9/8 16:24 
# @Author : 王西亚 
# @File : test_sql.py

from imetadata.database.c_factory import CFactory

if __name__ == '__main__':
    db = CFactory().give_me_db('0')
    session = db.give_me_session()
    try:
        db.session_execute(session, 'delete from dm2_storage')
        db.session_execute(session, 'delete from dm2_storage_directory')
        db.session_rollback(session)
    finally:
        db.session_close(session)
