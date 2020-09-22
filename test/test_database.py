# -*- coding: utf-8 -*- 
# @Time : 2020/8/13 16:35 
# @Author : 王西亚 
# @File : test_database.py

from imetadata.base.Exceptions import DBException
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
