# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 18:35 
# @Author : 王西亚 
# @File : job_test_interval.py.py 

from __future__ import absolute_import

import time

from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_import_step_monitor(CTimeJob):
    def execute(self) -> str:
        try:
            db = CFactory().give_me_db()
            sql_result_count = '''
                SELECT now() as query_time,
                ( SELECT COUNT ( * ) FROM dm2_storage_directory ) AS count_dir,
                ( SELECT COUNT ( * ) FROM dm2_storage_file ) AS count_file,
                ( SELECT COUNT ( * ) FROM dm2_storage_object ) AS count_object,
                ( SELECT COUNT ( * ) FROM dm2_storage_obj_detail ) AS count_obj_detail,
                ( SELECT COUNT ( * ) FROM dm2_storage_object WHERE dsotags IS NULL ) AS count_object_tag,
                ( SELECT COUNT ( * ) FROM dm2_storage_object WHERE dsotags IS NOT NULL ) AS count_object_notag
            '''

            count_dataset = db.one_row(sql_result_count)
            dis_query_time = count_dataset.value_by_name(0, 'query_time', '')
            dis_directory_count = count_dataset.value_by_name(0, 'count_dir', '')
            dis_file_count = count_dataset.value_by_name(0, 'count_file', '')
            dis_object_count = count_dataset.value_by_name(0, 'count_object', '')
            dis_detail_count = count_dataset.value_by_name(0, 'count_obj_detail', '')
            dis_object_tag_count = count_dataset.value_by_name(0, 'count_object_tag', '')
            dis_object_notag_count = count_dataset.value_by_name(0, 'count_object_notag', '')

            sql_insert = '''
                    insert into dm2_import_step 
                    ("dis_query_time","dis_id","dis_directory_count","dis_file_count","dis_object_count","dis_detail_count",
                    "dis_object_tag_count","dis_object_notag_count","dis_addtime") 
                    values (:query_time,:disid,:directory_count,:file_count,:object_count,:detail_count,
                    :object_tag_count,:object_notag_count,now())
                '''

            db.execute(sql_insert,
                       {
                           'query_time': dis_query_time,
                           'disid': CUtils.one_id(),
                           'directory_count': dis_directory_count,
                           'file_count': dis_file_count,
                           'object_count': dis_object_count,
                           'detail_count': dis_detail_count,
                           'object_tag_count': dis_object_tag_count,
                           'object_notag_count': dis_object_notag_count
                       }
                       )
            return CResult.merge_result(self.Success, '本次分析定时扫描任务成功结束！')

        except Exception as error:
            raise Exception(error.__str__())

if __name__ == '__main__':
    job_import_step_monitor('', '').execute()