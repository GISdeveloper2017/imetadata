# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_3001_gdb.py


from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.c_table import CTable


class plugins_3001_gdb(CDirPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'gdb'
        information[self.Plugins_Info_Type_Title] = 'GDB矢量数据集'
        # information[self.Plugins_Info_Name] = 'gdb'
        information[self.Plugins_Info_Type_Code] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Vector_DataSet
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Vector
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Directory_Itself
        # information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_gdb'
        information[self.Plugins_Info_Child_Layer_Data_Type] = 'layer'
        information[self.Plugins_Info_Child_Layer_Plugins_Name] = 'plugins_6050_layer_vector'
        information[self.Plugins_Info_Type_Code] = '020203'
        information[self.Plugins_Info_Is_Spatial] = self.DB_True
        information[self.Plugins_Info_Is_Dataset] = self.DB_True
        return information

    def classified(self):
        self._object_confirm = self.Object_Confirm_IUnKnown
        self._object_name = None

        current_path = self.file_info.file_name_with_full_path
        if (self.file_info.file_name_without_path.lower().endswith('.gdb')) \
                and CFile.find_file_or_subpath_of_path(current_path, '*.gdbtable'):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_main_name
        return self._object_confirm, self._object_name

    def parser_metadata_custom(self, parser: CMetaDataParser) -> str:
        """
        自定义的元数据解析, 在所有质检和其他处理之后触发
        :param parser:
        :return:
        """
        meta_data_json = parser.metadata.metadata_json()
        if meta_data_json is None:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 无法获取JSON格式的元数据! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )

        json_data_source = meta_data_json.xpath_one('datasource', None)

        layer_list = meta_data_json.xpath_one(self.Name_Layers, None)
        if layer_list is None:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 元数据中无法找到layers节点! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )

        gdb_ib_id = CFactory().give_me_db(self.file_info.db_server_id).one_value(
            '''
            select dso_ib_id
            from dm2_storage_object
            where dsoid = :object_id
            ''',
            {
                'object_id': parser.object_id
            }
        )

        error_message_list = []
        table = CTable()
        table.load_info(self.file_info.db_server_id, self.TableName_DM_Object)

        for layer in layer_list:
            layer_name = CUtils.dict_value_by_name(layer, self.Name_Name, '')
            if CUtils.equal_ignore_case(layer_name, ''):
                continue

            layer_alias_name = CUtils.dict_value_by_name(layer, self.Name_Description, layer_name)

            layer_metadata_json = CJson()
            layer_metadata_json.set_value_of_name('datasource', json_data_source)
            layer_metadata_json.set_value_of_name('layer_count', 1)
            layer_metadata_json.set_value_of_name('layers', [layer])
            layer_metadata_text = layer_metadata_json.to_json()

            try:
                sql_find_layer_existed = '''
                select dsoid as layer_id_existed
                from dm2_storage_object
                where upper(dsoobjectname) = upper(:layer_name)
                    and dsoparentobjid = :object_id
                '''
                layer_id_existed = CFactory().give_me_db(self.file_info.db_server_id).one_value(
                    sql_find_layer_existed,
                    {
                        'layer_name': layer_name,
                        'object_id': parser.object_id
                    }
                )
                if layer_id_existed is None:
                    layer_id_existed = CUtils.one_id()

                table.column_list.reset()
                table.column_list.column_by_name('dsoid').set_value(layer_id_existed)
                table.column_list.column_by_name('dsoobjectname').set_value(layer_name)
                table.column_list.column_by_name('dsoobjecttype').set_value(
                    CUtils.dict_value_by_name(
                        self.get_information(),
                        self.Plugins_Info_Child_Layer_Plugins_Name,
                        ''
                    )
                )
                table.column_list.column_by_name('dsodatatype').set_value(
                    CUtils.dict_value_by_name(
                        self.get_information(),
                        self.Plugins_Info_Child_Layer_Data_Type,
                        ''
                    )
                )
                table.column_list.column_by_name('dsoalphacode').set_value(CUtils.alpha_text(layer_name))
                table.column_list.column_by_name('dsoaliasname').set_value(layer_alias_name)
                table.column_list.column_by_name('dsoparentobjid').set_value(parser.object_id)
                table.column_list.column_by_name('dso_ib_id').set_value(gdb_ib_id)

                table.column_list.column_by_name('dsometadatatext').set_value(layer_metadata_text)
                table.column_list.column_by_name('dsometadatajson').set_value(layer_metadata_text)
                table.column_list.column_by_name('dsometadataparsestatus').set_value(self.ProcStatus_InQueue)
                table.column_list.column_by_name('dsotagsparsestatus').set_value(self.ProcStatus_InQueue)
                table.column_list.column_by_name('dsodetailparsestatus').set_value(self.ProcStatus_InQueue)
                result = table.save_data()
                if not CResult.result_success(result):
                    error_message_list.append(
                        '图层[{0}]的创建过程出现错误, 详细信息为: {1}'.format(
                            layer_name,
                            CResult.result_message(result)
                        )
                    )
            except Exception as error:
                error_message_list.append('图层[{0}]的创建过程出现错误, 详细信息为: {1}'.format(layer_name, error.__str__()))

        if len(error_message_list) > 0:
            return CResult.merge_result(
                self.Failure,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 详细情况如下: \n{1}'.format(
                    self.file_info.file_name_with_full_path,
                    CUtils.list_2_str(error_message_list, '', '\n', '', True)
                )
            )
        else:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的自定义元数据解析完毕! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )
