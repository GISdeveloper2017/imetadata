import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4009_gf6_pms import plugins_4009_gf6_pms
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分六号PMS传感器目录文件")  # 模块标题
class Test_plugins_4009_gf6_pms_File(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4009_gf6_pms(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF6_PMS_E114.5_N32.8_20190115_L1A1119839616',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF6_PMS_E114.5_N32.8_20190115_L1A1119839616'
            }
        ]


if __name__ == '__main__':
    pytest.main()
