# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 15:18 
# @Author : 王西亚 
# @File : c_filePlugins_guoto_dom.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerDOM import CMDTransformerDOM
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_DOM(CFilePlugins_GUOTU):

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将dom的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        transformer = CMDTransformerDOM(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        file_metadata_name_with_path = CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__)
        check_file_metadata_name_exist = False
        ext_list = ['xls', 'xlsx', 'mat', 'mdb']
        for ext in ext_list:
            temp_metadata_bus_file = '{0}.{1}'.format(file_metadata_name_with_path, ext)
            if CFile.file_or_path_exist(temp_metadata_bus_file):
                check_file_metadata_name_exist = True
                self.metadata_bus_transformer_type = ext
                self.metadata_bus_src_filename_with_path = temp_metadata_bus_file
                break

        if not check_file_metadata_name_exist:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(self.metadata_bus_src_filename_with_path)
                }
            )

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []
