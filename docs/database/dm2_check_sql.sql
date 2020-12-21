/*
    验证数据入库总体情况正确性的查询语句
    错误修正: 数据附属文件的名称, 是相对于数据所在的目录进行计算的
    示例:
    . storage: /users/mnt/data_root
    . directory: /dir1/dir2
    . file: /a.shp
    . 附属文件列表:
        /a.dbf
        /a.prj
        /a.shx
        /a.shp
    . 错误附属文件路径
        /users/mnt/data_root/dir1/dir2/a.dbf
*/

/*
    1. 验证数据附属文件中, 包含存储全路径的错误记录
        1. 错误记录范围: /users/mnt/data_root/dir1/dir2/a.dbf
*/
select dsoobjecttype
from (
         select dm2_storage_object.dsoobjectname,
                dm2_storage_object.dsoobjecttype,
                dm2_storage_obj_detail.*
         from dm2_storage_obj_detail
                  left join dm2_storage_object
                            on dm2_storage_obj_detail.dodobjectid = dm2_storage_object.dsoid
                  left join dm2_storage_inbound on dm2_storage_object.dso_ib_id = dm2_storage_inbound.dsiid
                  left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsitargetstorageid
         where position(coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || '/' in
                        dm2_storage_obj_detail.dodfilename || '/') = 1
     ) a
group by dsoobjecttype;

/*
    一个数据目录下, 应该绝大部分文件都应该能够被识别出为数据, 并且存储在附属文件中.
    该查询将查询记录哪些文件没有在任何数据的附属文件列表中, 也就是没有被识别出来, 没有纳入管理
    注意:
    . 没有被识别出来, 不是错误, 是我们的插件还需要补充
    . 我们需要判断那些应该被识别出来, 但是缺没有计入附属文件的记录
*/

select data_all.*, detail.*
from (
         select dm2_storage_object.dsodatatype,
                dm2_storage_directory.dsddirectory || dm2_storage_obj_detail.dodfilename as detail_file_relation_name
         from dm2_storage_obj_detail
                  left join dm2_storage_object
                            on dm2_storage_obj_detail.dodobjectid = dm2_storage_object.dsoid
                  left join dm2_storage_file
                            on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                  left join dm2_storage_directory
                            on dm2_storage_directory.dsdid = dm2_storage_file.dsfdirectoryid
         where dm2_storage_object.dsodatatype = 'file'

         union all

         select dm2_storage_object.dsodatatype,
                dm2_storage_directory.dsddirectory || dm2_storage_obj_detail.dodfilename as detail_file_relation_name
         from dm2_storage_obj_detail
                  left join dm2_storage_object
                            on dm2_storage_obj_detail.dodobjectid = dm2_storage_object.dsoid
                  left join dm2_storage_directory
                            on dm2_storage_directory.dsd_object_id = dm2_storage_object.dsoid
         where dm2_storage_object.dsodatatype = 'dir'

         union all
         select dm2_storage_object.dsodatatype, dm2_storage_obj_detail.dodfilename as detail_file_relation_name
         from dm2_storage_obj_detail
                  left join dm2_storage_object
                            on dm2_storage_obj_detail.dodobjectid = dm2_storage_object.dsoid
         where dm2_storage_object.dsodatatype <> 'dir'
           and dm2_storage_object.dsodatatype <> 'file'
     ) detail
         right join
     (
         select dsffilerelationname
         from dm2_storage_file
     ) data_all on data_all.dsffilerelationname = detail.detail_file_relation_name
where detail.dsodatatype is null
order by data_all.dsffilerelationname;


