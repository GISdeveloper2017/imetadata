import pytest
from imetadata.base.c_file import CFile


class Test_Base_C_File:
    def test_file_name(self):
        file = '/root/gf100000011111111.tar.gz'
        r = CFile.file_name(file)
        assert 'gf100000011111111.tar.gz' == r

    def test_file_main_name(self):
        file = '/root/gf100000011111111.tar.gz'
        r = CFile.file_main_name(file)
        assert 'gf100000011111111.tar' == r


