# -*- coding: utf-8 -*- 
# @Time : 2020/8/13 16:35 
# @Author : 王西亚 
# @File : test_database.py

from sqlalchemy import text

from imetadata.base.exceptions import DBException
from imetadata.database.base.c_dataset import CDataSet
from imetadata.database.c_factory import CFactory


class Test_DataBase:
    def test_fatch_one_row(self):
        try:
            factory = CFactory()
            db = factory.give_me_db('0')

            dataset = db.one_row("select * from dm2_storage where dstid = '1'")
            assert dataset.size() == 1
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
    engine = CFactory().give_me_db()
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

    print(engine.seq_next_value(engine.Seq_Type_Date_AutoInc))
