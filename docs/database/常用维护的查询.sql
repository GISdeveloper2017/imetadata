-- 初始化以及重新入库
update dm2_storage_inbound
set dsistatus        = 1
  , dsiprocid        = null
  , dsiprocmemo      = null
  , dsiaddtime       = now()
  , dsi_na_proc_id   = null
  , dsi_na_status    = 1
  , dsi_na_proc_memo = null
  , dsiotheroption   = null
  , dsidirectoryid   = null
  , dsibatchno       = null
;


truncate table dm2_storage_directory cascade;
truncate table dm2_storage_file cascade;
truncate table dm2_storage_inbound_log cascade;
truncate table dm2_storage_object cascade;
truncate table dm2_storage_obj_na cascade;
truncate table dm2_storage_obj_detail cascade;
truncate table dm2_storage_object cascade;
delete
from dm2_storage_inbound
where dsistorageid in (select dstid from dm2_storage where dsttype = 'inbound');

update sch_center_mission
set scmcommand = 'start',
    scmstatus  = 1;

update sch_center_mission
set scmcommand = 'shutdown',
    scmstatus  = 0;


-- 指定子系统, 启动重新提醒机制
update dm2_storage_inbound
set dsi_na_status    = 1
  , dsi_na_proc_memo = null
  , dsiotheroption   = '{
  "notify": {
    "module": [
      "module_distribution111"
    ]
  }
}'::jsonb
;


select dsiotheroption
from dm2_storage_inbound;

-- 注意: 合并时, 将根据第一次对象进行合并, 也就是说原属性中的notify对象, 将被第二个参数完整覆盖, 而不能覆盖notify下的module属性
select coalesce(dsiotheroption::text, '{}')::jsonb || '{
  "notify": {
    "module": [
      "module_distribution"
    ]
  }
}'::jsonb
from dm2_storage_inbound;


select dsometadataparsestatus
     , dsometadataparsememo
     , dso_metadata_bus_result
     , dsometadata_bus_parsememo
     , dso_spatial_result
     , dso_spatial_parsermemo
     , dso_view_result
     , dso_view_parsermemo
     , dso_time_result
     , dso_time_parsermemo
     , dso_metadataparser_retry
from dm2_storage_object
where dsometadataparsestatus > 2;


select dsfscanstatus, count(*)
from dm2_storage_file
group by dsfscanstatus;

select dsometadataparsestatus, dsotagsparsestatus, dsodetailparsestatus, dso_da_status, count(*)
from dm2_storage_object
group by dsometadataparsestatus, dsotagsparsestatus, dsodetailparsestatus, dso_da_status;

select count(*)
from dm2_storage_object
where dsometadataparsestatus = 0
  and dsodetailparsestatus = 0
  and dsotagsparsestatus = 0
  and dso_da_status = 0;


select count(*)
from dm2_storage_object
where dsometadataparsestatus <> 0
  and dso_metadataparser_retry = 3;





