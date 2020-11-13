# -*- coding: utf-8 -*- 
# @Time : 2020/8/13 16:35 
# @Author : 王西亚 
# @File : test_database.py

from sqlalchemy import text
import pytest
from imetadata.base.exceptions import DBException
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.c_factory import CFactory


class Test_DataBase:
    def test_fatch_one_row(self):
        try:
            factory = CFactory()
            db = factory.give_me_db('0')

            dataset = db.all_row("select * from dm2_storage where dstid in :id", {'id': "'01', '02'"})
            assert dataset.size() == 2
        except DBException as err:
            assert False

    def test_fatch_multi_row(self):
        try:
            factory = CFactory()
            db = factory.give_me_db('0')

            dataset = db.all_row("select * from dm2_storage where dstid = '1'")
            assert dataset.size() == 1
        except DBException as err:
            assert False

    def test_if_exist(self):
        try:
            factory = CFactory()
            db = factory.give_me_db('0')
            assert not db.if_exists("select * from dm2_storage where dstid = '0'")
        except DBException as err:
            assert False


if __name__ == '__main__':
    sql_available_storage = '''
    select dm2_storage.dstid, dm2_storage.dsttitle, dm2_storage.dst_volumn_max, dm2_storage.dst_volumn_max - coalesce(stat.file_size_sum, 0) as free_space
    from dm2_storage left join (
        select dsfstorageid, sum(dsffilesize) as file_size_sum
        from dm2_storage_file left join dm2_storage
            on dm2_storage_file.dsfstorageid = dm2_storage.dstid
        where dm2_storage.dsttype = 'core'
        group by dsfstorageid
        ) stat on dm2_storage.dstid = stat.dsfstorageid
    where dm2_storage.dsttype = 'core'
    order by dm2_storage.dst_volumn_max desc        
    '''
    ds_available_storage = CFactory().give_me_db().all_row(sql_available_storage)

    for storage_index in range(0, ds_available_storage.size()):
        print(ds_available_storage.value_by_name(storage_index, 'dsttitle', ''))
    # sql = '''
    # insert into test(id, string, clob, blob) values(:id, :string, :clob, :blob)
    # '''
    # statement = text(sql)
    # exe_params = statement.compile(engine.engine()).params
    # print(exe_params)
    # for param in exe_params:
    #     print(param)
    #
    # engine.execute('delete from test')
    #
    # params = {}
    # params['id'] = '1'
    # params['string'] = 6
    # params['clob'] = 5
    # CDataSet.file2param(params, 'bloB', '/Users/wangxiya/Downloads/IMG_9986.JPG')
    # engine.execute(sql, params)
    #
    # dataset = engine.one_row('select blob from test where id = 1')
    # dataset.blob2file(0, 'blob', '/Users/wangxiya/Downloads/output.jpg')

