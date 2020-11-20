# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_xml import CXml
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDMBaseJob(CDBQueueJob):
    Path_MD_Bus_Root = '/root'
    Path_MD_Bus_ProductType = '{0}/ProductType'.format(Path_MD_Bus_Root)

    def metadata_bus_2_params(self, metadata_xml: CXml, params: dict):
        metadata_list = metadata_xml.xpath('{0}/*'.format(self.Path_MD_Bus_Root))
        for metadata_item in metadata_list:
            metadata_item_name = CXml.get_element_name(metadata_item).lower().strip()
            metadata_item_value = CXml.get_element_text(metadata_item).lower().strip()
            params[metadata_item_name] = metadata_item_value

    def clear_anything_in_directory(self, ds_storage_id, ds_ib_directory_name):
        CFactory().give_me_db(self.get_mission_db_id()).execute_batch(
            [
                (
                    '''
                    delete from dm2_storage_obj_detail
                    where dodobjectid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_obj_detail
                    where dodobjectid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_object
                    where dsoid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_object
                    where dsoid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    )
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_file
                    where dsfstorageid = :StorageID and position(:SubDirectory in dsffilerelationname) = 1
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_directory
                    where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    }
                ), (
                    '''
                    delete from dm2_storage_directory
                    where dsdstorageid = :StorageID and dsddirectory = :SubDirectory
                    ''',
                    {
                        'StorageID': ds_storage_id,
                        'SubDirectory': ds_ib_directory_name
                    }
                )
            ]
        )
