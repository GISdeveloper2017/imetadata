import time
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory


def start_process():
    """
    新增入库跟踪情况的表 dm2_import_step,仅用于测试监控，实际发布时，这个表就不用了：
    内容：单独的调度,每隔30秒，统计各种个数
    个数：目录个数，文件个数，数据个数，附属文件个数，已挂接标签个数，未挂接标签个数
    """
    while True:
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

            time.sleep(30)

        except Exception as error:
            raise Exception(error.__str__())


if __name__ == '__main__':
    start_process()
