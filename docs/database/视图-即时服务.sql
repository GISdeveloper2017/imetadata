--视图0 cm_nation_area  替换原来即时服务系统中的库表（查询出的字段与原表的字段一致）
CREATE OR REPLACE VIEW public.cm_nation_area
 AS
 SELECT ro_global_dim_space.gdsid AS id,
    ro_global_dim_space.gdsparentid AS pid,
    ro_global_dim_space.gdstitle AS title,
    ro_global_dim_space.gdstreelevel AS level,
    ro_global_dim_space.gdsgeometry AS ngeometry,
    ro_global_dim_space.gdsuserid AS operid,
    ro_global_dim_space.gdstreeindex AS sort,
    ro_global_dim_space.gdscode AS code,
    ro_global_dim_space.gdsarea AS area,
    ro_global_dim_space.centerx AS centerlon,
    ro_global_dim_space.centery AS centerlat,
    ro_global_dim_space.gdspostcode AS postcode,
    ro_global_dim_space.gdsalphacode AS alphacode,
    ro_global_dim_space.gds_geo_bbox AS nbounds,
    ro_global_dim_space.gdsaddtime AS addtime
   FROM ro_global_dim_space;

ALTER TABLE public.cm_nation_area
    OWNER TO postgres;


--视图1 view_dm2_dataset  与原来的有区别（dm2_storage_object_def表字段和条件），修改后的
CREATE 
	OR REPLACE VIEW PUBLIC.view_dm2_dataset AS SELECT
	dm2_storage_object.dsoid AS dataset_objectid,
	dm2_storage_directory.dsdstorageid AS storage_id,
	dm2_storage_directory.dsdid AS directory_id,
	dm2_storage_object.dsoobjectname,
	dm2_storage_object.dsodatatype,
	dm2_storage_object.dsoobjecttype,
	dm2_storage_object_def.dsodtitle,
	dm2_storage_object_def.dsodtype,
	dm2_storage.dstunipath,
	dm2_storage_directory.dsddirectory,
	dm2_storage.dstunipath :: TEXT || dm2_storage_directory.dsddirectory :: TEXT AS dataset_path 
FROM
	dm2_storage_object
	LEFT JOIN dm2_storage_object_def ON dm2_storage_object.dsoobjecttype :: TEXT = dm2_storage_object_def.dsodid ::
	TEXT LEFT JOIN dm2_storage_directory ON dm2_storage_directory.dsd_object_id :: TEXT = dm2_storage_object.dsoid ::
	TEXT LEFT JOIN dm2_storage ON dm2_storage.dstid :: TEXT = dm2_storage_directory.dsdstorageid :: TEXT 
WHERE
	dm2_storage_directory.dsd_object_confirm = '-1' :: INTEGER 
	AND dm2_storage_directory.dsd_directory_valid = '-1' :: INTEGER 
	AND dm2_storage_object_def.dsodgroup :: TEXT = 'land_dataset' :: TEXT;
ALTER TABLE PUBLIC.view_dm2_dataset OWNER TO postgres;
COMMENT ON VIEW PUBLIC.view_dm2_dataset IS '所有数据集的记录信息';

--视图2 view_dm2_dataset_detail  与原来的有区别（查询条件和注释的表字段），修改后的
 CREATE OR REPLACE VIEW public.view_dm2_dataset_detail
 AS 
 SELECT dm2_storage_obj_detail.dodid AS obj_detail_id,
    dm2_storage_obj_detail.dodobjectid AS object_id,
    dm2_storage_object.dsoparentobjid AS dataset_objectid,
    dm2_storage_directory.dsdstorageid AS storage_id,
    dm2_storage_directory.dsdid AS directory_id,
    dm2_storage_object.dsoparentobjid,
    dm2_storage_obj_detail.dodfilename,
    dm2_storage_obj_detail.dodfileext,
    dm2_storage_obj_detail.dodfilesize,
    --dm2_storage_obj_detail.dodfileattr,
    --dm2_storage_obj_detail.dod_parentid,
    dm2_storage.dstunipath,
    dm2_storage_directory.dsddirectory,
    ((dm2_storage.dstunipath::text || dm2_storage_directory.dsddirectory::text) || '\'::text) || dm2_storage_obj_detail.dodfilename::text AS datafullname_ip
   FROM dm2_storage_obj_detail
     LEFT JOIN dm2_storage_object ON dm2_storage_object.dsoid::text = dm2_storage_obj_detail.dodobjectid::text
     LEFT JOIN ( SELECT dm2_storage_object_1.dsoid,
            dm2_storage_object_1.dsoobjectname,
            dm2_storage_object_1.dsoobjecttype,
            dm2_storage_object_1.dsodatatype,
            dm2_storage_object_1.dsometadatatext,
            dm2_storage_object_1.dsometadatajson,
            dm2_storage_object_1.dsometadatajson_bus,
            dm2_storage_object_1.dsometadataxml,
            dm2_storage_object_1.dsometadatatype,
            dm2_storage_object_1.dsometadataparsestatus,
            dm2_storage_object_1.dsometadataparseprocid,
            dm2_storage_object_1.dsotags,
            dm2_storage_object_1.dsolastmodifytime,
            dm2_storage_object_1.dsometadataparsememo,
            dm2_storage_object_1.dsodetailparsememo,
            dm2_storage_object_1.dsodetailparsestatus,
            dm2_storage_object_1.dsodetailparseprocid,
            dm2_storage_object_1.dsotagsparsememo,
            dm2_storage_object_1.dsotagsparsestatus,
            dm2_storage_object_1.dsotagsparseprocid,
            dm2_storage_object_1.dsoalphacode,
            dm2_storage_object_1.dsoaliasname,
            --dm2_storage_object_1.dso_hand_status,
            --dm2_storage_object_1.dsolastprocessstatus,
            --dm2_storage_object_1.dsolastprocessprocid,
            --dm2_storage_object_1.dsolastprocessmemo,
            dm2_storage_object_1.dsoparentobjid,
            dm2_storage_object_1.dsometadataxml_bus,
            dm2_storage_object_1.dsometadatatext_bus,
            dm2_storage_object_1.dsometadatatype_bus,
            dm2_storage_object_1.dsometadata_bus_parsememo
            --dm2_storage_object_1.dsometadata_bus_parsestatus
           FROM dm2_storage_object dm2_storage_object_1) dataset_object ON dataset_object.dsoid::text = dm2_storage_object.dsoparentobjid::text
     LEFT JOIN ( SELECT dm2_storage_file.dsf_object_id AS object_id,
            dm2_storage_file.dsffilename AS object_name,
            dm2_storage_file.dsffilerelationname AS object_relationname,
            dm2_storage_file.dsfdirectoryid AS object_directoryid,
            dm2_storage_file.dsfaddtime AS object_addtime,
            dm2_storage_file.dsffilevalid AS object_valid
           FROM dm2_storage_file
          WHERE dm2_storage_file.dsf_object_confirm = '-1'::integer
        UNION ALL
         SELECT dm2_storage_directory_1.dsd_object_id AS object_id,
            dm2_storage_directory_1.dsddirectoryname AS object_name,
            dm2_storage_directory_1.dsddirectory AS object_relationname,
            dm2_storage_directory_1.dsdparentid AS object_directoryid,
            dm2_storage_directory_1.dsdaddtime AS object_addtime,
            dm2_storage_directory_1.dsd_directory_valid AS object_valid
           FROM dm2_storage_directory dm2_storage_directory_1
          WHERE dm2_storage_directory_1.dsd_object_confirm = '-1'::integer) objfile ON objfile.object_id::text = dm2_storage_object.dsoid::text
     LEFT JOIN dm2_storage_directory ON objfile.object_directoryid::text = dm2_storage_directory.dsdid::text
     LEFT JOIN dm2_storage ON dm2_storage.dstid::text = dm2_storage_directory.dsdstorageid::text
     LEFT JOIN dm2_storage_object_def ON dataset_object.dsoobjecttype::text = dm2_storage_object_def.dsodid::text
  WHERE dm2_storage_object.dsoparentobjid IS NOT NULL AND dm2_storage_object_def.dsodgroup::text = 'land_dataset'::text;
	
	ALTER TABLE public.view_dm2_dataset_detail
    OWNER TO postgres;
COMMENT ON VIEW public.view_dm2_dataset_detail
    IS '数据集所包含的所有文件信息，包括全路径，记录中obj_detail_id=object_id 的为主文件记录';
	

	
--视图3 view_dm2_object_dirandfile 与原来的没有区别，原来的直接用
CREATE OR REPLACE VIEW public.view_dm2_object_dirandfile
 AS
 SELECT dm2_storage_object.dsoid AS dps_object_id,
    dm2_storage_file.dsffilename AS dps_object_name,
    dm2_storage_object.dsoobjecttype AS dps_object_type,
    dm2_storage_file.dsfext AS dps_object_ext_type,
    dm2_storage_object.dsoparentobjid,
    dm2_storage_object.dsodatatype AS dps_dsodatatype,
    detail.object_size AS dps_object_size,
    dm2_storage_file.dsffilemodifytime AS dps_object_date,
    dm2_storage.dstunipath AS storagepath,
    dm2_storage_directory.dsddirectory AS relatedir,
    dm2_storage.dstunipath::text || dm2_storage_file.dsffilerelationname::text AS dps_object_fullname,
    dm2_storage_file.dsffilerelationname AS dps_object_relationname,
    dm2_storage_directory.dsddirectory AS dps_object_relationpath,
    dm2_storage_file.dsfstorageid AS dps_object_storageid,
    md5(lower((((((dm2_storage_file.dsfstorageid::text || '-'::text) || dm2_storage_file.dsffilerelationname::text) || '-'::text) || detail.object_size::character varying::text) || '-'::text) || dm2_storage_file.dsffilemodifytime::character varying::text)) AS dps_object_fp
   FROM dm2_storage_object
     LEFT JOIN dm2_storage_obj_detail ON dm2_storage_object.dsoid::text = dm2_storage_obj_detail.dodid::text
     LEFT JOIN dm2_storage_file ON dm2_storage_file.dsf_object_id::text = dm2_storage_object.dsoid::text
     LEFT JOIN dm2_storage_directory ON dm2_storage_file.dsfdirectoryid::text = dm2_storage_directory.dsdid::text
     LEFT JOIN dm2_storage ON dm2_storage.dstid::text = dm2_storage_directory.dsdstorageid::text
     LEFT JOIN ( SELECT dm2_storage_obj_detail_1.dodobjectid,
            sum(dm2_storage_obj_detail_1.dodfilesize) AS object_size
           FROM dm2_storage_obj_detail dm2_storage_obj_detail_1
          GROUP BY dm2_storage_obj_detail_1.dodobjectid) detail ON dm2_storage_object.dsoid::text = detail.dodobjectid::text
  WHERE dm2_storage_object.dsodatatype::text = 'file'::text AND dm2_storage_file.dsffilevalid = '-1'::integer
UNION ALL
 SELECT dm2_storage_object.dsoid AS dps_object_id,
    dm2_storage_directory.dsddirectoryname AS dps_object_name,
    dm2_storage_object.dsoobjecttype AS dps_object_type,
    ''::character varying AS dps_object_ext_type,
    dm2_storage_object.dsoparentobjid,
    dm2_storage_object.dsodatatype AS dps_dsodatatype,
    detail.object_size AS dps_object_size,
    detail.object_time AS dps_object_date,
    dm2_storage.dstunipath AS storagepath,
    dm2_storage_directory.dsddirectory AS relatedir,
    dm2_storage.dstunipath::text || dm2_storage_directory.dsddirectory::text AS dps_object_fullname,
    dm2_storage_directory.dsddirectory AS dps_object_relationname,
    dm2_storage_directory.dsdpath AS dps_object_relationpath,
    dm2_storage_directory.dsdstorageid AS dps_object_storageid,
    md5(lower((((((dm2_storage_directory.dsdstorageid::text || '-'::text) || dm2_storage_directory.dsddirectory::text) || '-'::text) || detail.object_size::character varying::text) || '-'::text) || detail.object_time::character varying::text)) AS dps_object_fp
   FROM dm2_storage_object
     LEFT JOIN dm2_storage_obj_detail ON dm2_storage_object.dsoid::text = dm2_storage_obj_detail.dodid::text
     LEFT JOIN dm2_storage_directory ON dm2_storage_object.dsoid::text = dm2_storage_directory.dsd_object_id::text
     LEFT JOIN dm2_storage ON dm2_storage.dstid::text = dm2_storage_directory.dsdstorageid::text
     LEFT JOIN ( SELECT dm2_storage_obj_detail_1.dodobjectid,
            sum(dm2_storage_obj_detail_1.dodfilesize) AS object_size,
            max(dm2_storage_obj_detail_1.dodfilemodifytime) AS object_time
           FROM dm2_storage_obj_detail dm2_storage_obj_detail_1
          GROUP BY dm2_storage_obj_detail_1.dodobjectid) detail ON dm2_storage_object.dsoid::text = detail.dodobjectid::text
  WHERE dm2_storage_object.dsodatatype::text = 'dir'::text AND dm2_storage_directory.dsd_directory_valid = '-1'::integer;

ALTER TABLE public.view_dm2_object_dirandfile
    OWNER TO postgres;
COMMENT ON VIEW public.view_dm2_object_dirandfile
    IS '所有数据产品的列表，包括数据集产品和单个数据产品，以及数据集所包含的数据产品，能够查看数据的文件信息，其dps_object_id为rsp表中的aprid';
	

--视图4 view_dm2_object_filedetail 与原来的没有区别，原来的直接用
CREATE OR REPLACE VIEW public.view_dm2_object_filedetail
 AS
 SELECT b.dps_object_id AS objectid,
    c.dodid AS obj_detail_id,
    c.dodfilename,
    b.dps_object_storageid AS storageid,
    ((b.storagepath::text || b.relatedir::text) || '\'::text) || c.dodfilename::text AS dps_object_fullname
   FROM ap3_product_rsp a,
    view_dm2_object_dirandfile b,
    dm2_storage_obj_detail c
  WHERE a.aprid::text = b.dps_object_id::text AND b.dps_object_id::text = c.dodobjectid::text;

ALTER TABLE public.view_dm2_object_filedetail
    OWNER TO postgres;
COMMENT ON VIEW public.view_dm2_object_filedetail
    IS '该视图将根据产品的aprid，将产品的存储storage root路径和mount路径获取到';
	
	
--视图5 view_dm2_object_stat 与原来的有区别（查询的表字段dsodcatalog->dsodgroup），修改后的
CREATE OR REPLACE VIEW public.view_dm2_object_stat
 AS
SELECT dm2_storage_object_def.dsodtypecode as dsodcode,
    dm2_storage_object_def.dsodgroup,
    detail.objectsize,
        --CASE dm2_storage_object.dsolastprocess_status
        --    WHEN '01'::text THEN 0::numeric
        --    WHEN '02'::text THEN 0::numeric
        --    WHEN '03'::text THEN 0::numeric
        --    WHEN '04'::text THEN 0::numeric
        --    WHEN '05'::text THEN 0::numeric
        --    WHEN '06'::text THEN 0::numeric
        --    WHEN '07'::text THEN 0::numeric
        --    WHEN '08'::text THEN 0::numeric
        --    WHEN '081'::text THEN 0::numeric
        --    WHEN '082'::text THEN 0::numeric
        --    ELSE to_number(dm2_storage_object.dsolastprocess_status::text, '9'::text)
        -- END AS lastprocessstatus,
		dm2_storage_obj_na_1.dson_notify_status as lastprocessstatus,
		dm2_storage_obj_na_1.dson_addtime as dsolastprocess_starttime,
		dm2_storage_obj_na_1.dson_lastmodify_time as dsolastprocess_endtime,		
    dm2_storage_object.dsoid AS object_id,
    dm2_storage_directory.dsdstorageid AS storage_id,
    dm2_storage_directory.dsdid AS directory_id,
    dm2_storage_object.dsoparentobjid,
    dm2_storage_object.dsoobjectname,
    dm2_storage_object.dsodatatype,
    dm2_storage_object.dsoobjecttype,
    --dm2_storage_object.dsolastprocess_starttime,
    --dm2_storage_object.dsolastprocess_endtime,
    dm2_storage.dstunipath,
    dm2_storage_directory.dsddirectory,
    dm2_storage.dstunipath::text || objfile.object_relationname::text AS object_fullname,
    dm2_storage.dstunipath::text || dm2_storage_directory.dsddirectory::text AS object_path
   FROM dm2_storage_object
     LEFT JOIN ( SELECT dm2_storage_file.dsf_object_id AS object_id,
            dm2_storage_file.dsffilename AS object_name,
            dm2_storage_file.dsffilerelationname AS object_relationname,
            dm2_storage_file.dsfdirectoryid AS object_directoryid,
            dm2_storage_file.dsfaddtime AS object_addtime,
            dm2_storage_file.dsf_object_confirm AS object_confirm,
            dm2_storage_file.dsffilevalid AS object_valid
           FROM dm2_storage_file
          WHERE dm2_storage_file.dsf_object_confirm = '-1'::integer
        UNION ALL
         SELECT dm2_storage_directory_1.dsd_object_id AS object_id,
            dm2_storage_directory_1.dsddirectoryname AS object_name,
            dm2_storage_directory_1.dsddirectory AS object_relationname,
            dm2_storage_directory_1.dsdparentid AS object_directoryid,
            dm2_storage_directory_1.dsdaddtime AS object_addtime,
            dm2_storage_directory_1.dsd_object_confirm AS object_confirm,
            dm2_storage_directory_1.dsd_directory_valid AS object_valid
           FROM dm2_storage_directory dm2_storage_directory_1
          WHERE dm2_storage_directory_1.dsd_object_confirm = '-1'::integer) objfile ON objfile.object_id::text = dm2_storage_object.dsoid::text
     LEFT JOIN dm2_storage_directory ON dm2_storage_directory.dsdid::text = objfile.object_directoryid::text
     LEFT JOIN dm2_storage ON dm2_storage.dstid::text = dm2_storage_directory.dsdstorageid::text
     LEFT JOIN dm2_storage_object_def ON dm2_storage_object.dsoobjecttype::text = dm2_storage_object_def.dsodid::text
		 left join ( SELECT * FROM dm2_storage_obj_na WHERE dm2_storage_obj_na.dson_app_id = 'module_distribution' ) dm2_storage_obj_na_1 ON dm2_storage_object.dsoid = dm2_storage_obj_na_1.dson_object_id 
     LEFT JOIN ( SELECT dm2_storage_obj_detail.dodobjectid,
            sum(dm2_storage_obj_detail.dodfilesize) AS objectsize
           FROM dm2_storage_obj_detail
          GROUP BY dm2_storage_obj_detail.dodobjectid) detail ON dm2_storage_object.dsoid::text = detail.dodobjectid::text
  WHERE objfile.object_confirm = '-1'::integer AND objfile.object_valid = '-1'::integer AND dm2_storage_object_def.dsodgroup in ('land_data','raster','vector')
UNION ALL
 SELECT dm2_storage_object_def.dsodtypecode as dsodcode,
    dm2_storage_object_def.dsodgroup,
    dataset_detail.objectsize,
       -- CASE dm2_storage_object.dsolastprocess_status
         --   WHEN '01'::text THEN 0::numeric
         --   WHEN '02'::text THEN 0::numeric
        --    WHEN '03'::text THEN 0::numeric
        --    WHEN '04'::text THEN 0::numeric
        --    WHEN '05'::text THEN 0::numeric
        --    WHEN '06'::text THEN 0::numeric
        --    WHEN '07'::text THEN 0::numeric
        --    WHEN '08'::text THEN 0::numeric
         --   WHEN '081'::text THEN 0::numeric
        --    WHEN '082'::text THEN 0::numeric
        --    ELSE to_number(dm2_storage_object.dsolastprocess_status::text, '9'::text)
       -- END AS lastprocessstatus,
	 	dm2_storage_obj_na_1.dson_notify_status as lastprocessstatus,
		dm2_storage_obj_na_1.dson_addtime as dsolastprocess_starttime,
		dm2_storage_obj_na_1.dson_lastmodify_time as dsolastprocess_endtime,	
    dm2_storage_object.dsoid AS object_id,
    dm2_storage_directory.dsdstorageid AS storage_id,
    dm2_storage_directory.dsdid AS directory_id,
    dm2_storage_object.dsoparentobjid,
    dm2_storage_object.dsoobjectname,
    dm2_storage_object.dsodatatype,
    dm2_storage_object.dsoobjecttype,
    --dm2_storage_object.dsolastprocess_starttime,
    --dm2_storage_object.dsolastprocess_endtime,
    dm2_storage.dstunipath,
    dm2_storage_directory.dsddirectory,
    dm2_storage.dstunipath::text || objfile.object_relationname::text AS object_fullname,
    dm2_storage.dstunipath::text || dm2_storage_directory.dsddirectory::text AS object_path
   FROM dm2_storage_object
     LEFT JOIN ( SELECT dm2_storage_file.dsf_object_id AS object_id,
            dm2_storage_file.dsffilename AS object_name,
            dm2_storage_file.dsffilerelationname AS object_relationname,
            dm2_storage_file.dsfdirectoryid AS object_directoryid,
            dm2_storage_file.dsfaddtime AS object_addtime,
            dm2_storage_file.dsf_object_confirm AS object_confirm,
            dm2_storage_file.dsffilevalid AS object_valid
           FROM dm2_storage_file
          WHERE dm2_storage_file.dsf_object_confirm = '-1'::integer
        UNION ALL
         SELECT dm2_storage_directory_1.dsd_object_id AS object_id,
            dm2_storage_directory_1.dsddirectoryname AS object_name,
            dm2_storage_directory_1.dsddirectory AS object_relationname,
            dm2_storage_directory_1.dsdparentid AS object_directoryid,
            dm2_storage_directory_1.dsdaddtime AS object_addtime,
            dm2_storage_directory_1.dsd_object_confirm AS object_confirm,
            dm2_storage_directory_1.dsd_directory_valid AS object_valid
           FROM dm2_storage_directory dm2_storage_directory_1
          WHERE dm2_storage_directory_1.dsd_object_confirm = '-1'::integer) objfile ON objfile.object_id::text = dm2_storage_object.dsoid::text
     LEFT JOIN dm2_storage_directory ON dm2_storage_directory.dsdid::text = objfile.object_directoryid::text
     LEFT JOIN dm2_storage ON dm2_storage.dstid::text = dm2_storage_directory.dsdstorageid::text
     LEFT JOIN dm2_storage_object_def ON dm2_storage_object.dsoobjecttype::text = dm2_storage_object_def.dsodid::text
		 left join ( SELECT * FROM dm2_storage_obj_na WHERE dm2_storage_obj_na.dson_app_id = 'module_distribution' ) dm2_storage_obj_na_1 ON dm2_storage_object.dsoid = dm2_storage_obj_na_1.dson_object_id 
     LEFT JOIN ( SELECT dm2_storage_object_1.dsoparentobjid,
            sum(dm2_storage_obj_detail.dodfilesize) AS objectsize
           FROM dm2_storage_obj_detail
             LEFT JOIN dm2_storage_object dm2_storage_object_1 ON dm2_storage_object_1.dsoid::text = dm2_storage_obj_detail.dodobjectid::text
             LEFT JOIN ( SELECT dm2_storage_object_2.dsoid,
                    dm2_storage_object_2.dsoobjectname,
                    dm2_storage_object_2.dsoobjecttype,
                    dm2_storage_object_2.dsodatatype,
                    dm2_storage_object_2.dsometadatatext,
                    dm2_storage_object_2.dsometadatajson,
                    dm2_storage_object_2.dsometadatajson_bus,
                    dm2_storage_object_2.dsometadataxml,
                    dm2_storage_object_2.dsometadatatype,
                    dm2_storage_object_2.dsometadataparsestatus,
                    dm2_storage_object_2.dsometadataparseprocid,
                    dm2_storage_object_2.dsotags,
                    dm2_storage_object_2.dsolastmodifytime,
                    dm2_storage_object_2.dsometadataparsememo,
                    dm2_storage_object_2.dsodetailparsememo,
                    dm2_storage_object_2.dsodetailparsestatus,
                    dm2_storage_object_2.dsodetailparseprocid,
                    dm2_storage_object_2.dsotagsparsememo,
                    dm2_storage_object_2.dsotagsparsestatus,
                    dm2_storage_object_2.dsotagsparseprocid,
                    dm2_storage_object_2.dsoalphacode,
                    dm2_storage_object_2.dsoaliasname,
                    --dm2_storage_object_2.dso_hand_status,
                    --dm2_storage_object_2.dsolastprocessstatus,
                    --dm2_storage_object_2.dsolastprocessprocid,
                    --dm2_storage_object_2.dsolastprocessmemo,
                    dm2_storage_object_2.dsoparentobjid,
                    dm2_storage_object_2.dsometadataxml_bus,
                    dm2_storage_object_2.dsometadatatext_bus,
                    dm2_storage_object_2.dsometadatatype_bus,
                    dm2_storage_object_2.dsometadata_bus_parsememo
                    --dm2_storage_object_2.dsometadata_bus_parsestatus,
                    --dm2_storage_object_2.dsolastprocess_starttime,
                    --dm2_storage_object_2.dsolastprocess_endtime
                   FROM dm2_storage_object dm2_storage_object_2) dataset_object ON dataset_object.dsoid::text = dm2_storage_object_1.dsoparentobjid::text
          WHERE dm2_storage_object_1.dsoparentobjid IS NOT NULL
          GROUP BY dm2_storage_object_1.dsoparentobjid) dataset_detail ON dm2_storage_object.dsoid::text = dataset_detail.dsoparentobjid::text
  WHERE objfile.object_confirm = '-1'::integer AND objfile.object_valid = '-1'::integer AND dm2_storage_object_def.dsodgroup = 'land_dataset';
	
		ALTER TABLE public.view_dm2_object_stat
    OWNER TO postgres;
