import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4009_gf6_wfv import plugins_4009_gf6_wfv
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分六号WFV传感器目录文件")  # 模块标题
class Test_plugins_4009_gf6_wfv_File(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4009_gf6_wfv(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'GF6_WFV_E115.9_N30.1_20180607_L1A0000632302.tar.gz',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF6_WFV_E115.9_N30.1_20180607_L1A0000632302'
            }
        ]


if __name__ == '__main__':
    pytest.main()
