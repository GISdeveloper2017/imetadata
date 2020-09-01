truncate table da_search_package;

insert into da_search_package(
  datype, daTitle, daIndexID, daIndexClass, daIndexType, daFileID, daDescription, dafiletype, dafilemetadata, 
  dafileseqid, dafilename, dafilemainname, dafileext, dafilesize, dafiledate, daSearch) 

select * from dblink(
  'hostaddr=172.172.5.194 port=5432 dbname=datamng user=postgres password=postgres', 
  '
select ''package'' as datype,
  dm_index_ptd.diDescription as daTitle, 
  dm_index_ptd.diid as daIndexID,
  dm_index_ptd.diClass as daIndexClass,
  dm_index_ptd.diType as daIndexType,
  ro_file.fid as daFileID,
  COALESCE(dm_index_ptd.diDescription, '''') || ''|'' || COALESCE(dm_index_ptd_files.diFileName, '''') || ''|'' || COALESCE(dm_index_ptd.diMemo,'''') as daDescription,
  COALESCE(dm_index_ptd_files.diIsSpatial, -1) as dafiletype,
  dm_index_ptd_files.diSpatialMetaData as dafilemetadata,
  dm_index_ptd_files.diSeqId as dafileseqid,
  dm_index_ptd_files.diFileName as dafilename,
  dm_index_ptd_files.diFileName as dafilemainname, 
  dm_index_ptd_files.diFileExt as dafileext,
  dm_index_ptd_files.diFileSize as dafilesize, 
  dm_index_ptd_files.diFileDate as dafiledate,   
  to_tsVector(COALESCE(dm_index_ptd.diDescription, '''') || ''|'' || COALESCE(dm_index_ptd_files.diFileName, '''') || ''|'' || COALESCE(dm_index_ptd.diMemo,'''')) as dasearch
from dm_index_ptd 
  left join dm_index_ptd_files on dm_index_ptd.diid = dm_index_ptd_files.diid
  left join dm_index_file on dm_index_ptd.diid = dm_index_file.indexid
  left join ro_file on dm_index_file.fileid = ro_file.fid
where dm_index_ptd_files.diSeqId is not null
limit 100000
  '
)
as t(
datype text, daTitle text, daIndexID text, daIndexClass text, daIndexType text, 
daFileID text, daDescription text, dafiletype integer, dafilemetadata xml,
dafileseqid bigint, dafilename text, dafilemainname text, dafileext text, dafilesize bigint,
dafiledate timestamp without time zone, daSearch tsVector 
);