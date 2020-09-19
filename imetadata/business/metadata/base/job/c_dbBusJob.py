# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 19:41
# @Author : 赵宇飞
# @File : c_dbBusJob.py

from __future__ import absolute_import
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob


class CDBBusJob(CDMBaseJob):
    """
    数据库操作的业务类，如根据objectid删除对象数据，根据directoryid删除目录id对应的数据记录
    """

    def delete_by_directoryid(self, directory_id):
        """
          根据目录id删除dm2_storage_directory的数据库记录

        :param directory_id:
        :return:
        """
        pass

    def delete_by_fileid(self, file_id):
        """
          根据文件id删除dm2_storage_file数据库记录

        :param file_id:
        :return:
        """
        pass

    def delete_object_by_objectid(self, objectid):
        """
          根据对象id删除数据库记录，包含object表，detail表

        :param objectid:
        :return:
        """
        pass

    def delete_object_by_directoryid(self, directoryid):
        """
        根据目录id删除数据记录，不包含子目录  ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        """
        pass

    def delete_object_by_directoryid_with_dirchild(self, directoryid):
        """
        根据目录id删除数据记录,包含子目录 ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        """

        sql_list =[]
        # 1.file表中的object对象对应的detail表记录
        sql_detail_in_file = '''
          DELETE
          FROM
	          dm2_storage_obj_detail
          WHERE
	          dodobjectid IN (
		          SELECT 
			          dsf_object_id
		          FROM
			          dm2_storage_file
		          WHERE
			          dsf_object_id IS NOT NULL 
                    AND dsf_object_id != ''
		            AND dsfdirectoryid IN (
                        SELECT
                            dsdid
                        FROM
                            dm2_storage_directory 
                        WHERE
                            dsdstorageid = ( SELECT dsdstorageid FROM dm2_storage_directory WHERE dsdid = '{0}}' ) 
                            AND (
                                dsddirectory = ( SELECT dsddirectory FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                            OR dsddirectory LIKE ( SELECT REPLACE ( dsddirectory , '\' , '\\' ) || '\\%' FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                            ) 
	            )
	          ); 
        '''.format(directoryid)

        # 2.directory表中的object对象对应的detail表记录
        sql_detail_in_directory = '''
          DELETE
          FROM
	          dm2_storage_obj_detail
          WHERE
	          dodobjectid IN (
		          SELECT
			          dsd_object_id
		          FROM
			          dm2_storage_directory
		          WHERE
			          dsd_object_id IS NOT NULL
		          AND dsd_object_id != ''
		          AND dsdparentid IN (
	            	SELECT
                        dsdid
                    FROM
                        dm2_storage_directory 
                    WHERE
                        dsdstorageid = ( SELECT dsdstorageid FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                        AND (
                            dsddirectory = ( SELECT dsddirectory FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                        OR dsddirectory LIKE ( SELECT REPLACE ( dsddirectory , '\' , '\\' ) || '\\%' FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                        )
	            )
	          );
        '''.format(directoryid)

        # 3.file表中的object对象记录
        sql_object_in_file = '''
          DELETE
          FROM
	          dm2_storage_object
          WHERE
	          dsoid IN (
		          SELECT
			          dsf_object_id
		          FROM
			          dm2_storage_file
		          WHERE
			          dsf_object_id IS NOT NULL 
                    AND dsf_object_id != ''
		            AND dsfdirectoryid IN (
                        SELECT
                            dsdid
                        FROM
                            dm2_storage_directory 
                        WHERE
                            dsdstorageid = ( SELECT dsdstorageid FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                            AND (
                                dsddirectory = ( SELECT dsddirectory FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                            OR dsddirectory LIKE ( SELECT REPLACE ( dsddirectory , '\' , '\\' ) || '\\%' FROM dm2_storage_directory WHERE dsdid = '{0}' ) 
                           )
                    )
	          );
                '''.format(directoryid)

        # 4.directory表中的object对象记录
        sql_object_in_directory = '''
            DELETE
            FROM
              dm2_storage_object
            WHERE
              dsoid IN (
                  SELECT
                      dsd_object_id
                  FROM
                      dm2_storage_directory
                  WHERE
                      dsd_object_id IS NOT NULL
                  AND dsd_object_id != ''
                  AND dsdparentid IN (
                        SELECT
                        dsdid
                        FROM
                            dm2_storage_directory 
                        WHERE
                            dsdstorageid = ( SELECT dsdstorageid FROM dm2_storage_directory WHERE dsdid = '$directoryid$' ) 
                            AND (
                                dsddirectory = ( SELECT dsddirectory FROM dm2_storage_directory WHERE dsdid = '$directoryid$' ) 
                            OR dsddirectory LIKE ( SELECT REPLACE ( dsddirectory , '\' , '\\' ) || '\\%' FROM dm2_storage_directory WHERE dsdid = '$directoryid$' ) 
                            )
                    )
                );
            '''.format(directoryid)

        #sql_list.append(sql_detail_in_file)
        #sql_list.append(sql_detail_in_directory)
        sql_list.append(sql_object_in_file)
        sql_list.append(sql_object_in_directory)


        pass

    def clear_data_no_valid(self):
        """
        清除垃圾 ，包含directory表，file表，object表，detail表

        :return:
        """
        pass
