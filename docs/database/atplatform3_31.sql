/*
    dm2_storage
*/

alter table public.dm2_storage
    drop column if exists dstwatchperiod;
alter table public.dm2_storage
    drop column if exists dstwhitelist;
alter table public.dm2_storage
    drop column if exists dstblacklist;
alter table public.dm2_storage
    drop column if exists dstfileext;

alter table public.dm2_storage
    add column if not exists dst_volumn_max bigint DEFAULT 0;
alter table public.dm2_storage
    add column if not exists dst_volumn_warn bigint DEFAULT 0;
alter table public.dm2_storage
    add column if not exists dst_volumn_now bigint DEFAULT 0;
alter table public.dm2_storage
    add column if not exists dsttype character varying(20) COLLATE pg_catalog."default" DEFAULT 'core'::character varying;
alter table public.dm2_storage
    add column if not exists dstuserid character varying(100) COLLATE pg_catalog."default";
alter table public.dm2_storage
    add column if not exists dstownerpath character varying(4000) COLLATE pg_catalog."default";
alter table public.dm2_storage
    add column if not exists dstscanmemo text COLLATE pg_catalog."default";
alter table public.dm2_storage
    add column if not exists dstwatchoption jsonb;

COMMENT ON COLUMN public.dm2_storage.dst_volumn_max IS '存储-容积-最大值';
COMMENT ON COLUMN public.dm2_storage.dst_volumn_warn IS '存储-容积-警告值';
COMMENT ON COLUMN public.dm2_storage.dst_volumn_now IS '存储-容积-当前值';
COMMENT ON COLUMN public.dm2_storage.dsttype IS '存储类型';
COMMENT ON COLUMN public.dm2_storage.dstuserid IS '数管-存储-用户';
COMMENT ON COLUMN public.dm2_storage.dstownerpath IS '数管-存储-私有路径';
COMMENT ON COLUMN public.dm2_storage.dstscanmemo IS '数管-存储-扫描-结果';
COMMENT ON COLUMN public.dm2_storage.dstwatchoption IS '存储-扫描配置';

/*
    dm2_storage_directory
*/

alter table public.dm2_storage_directory
    add column if not exists dsd_volumn_now bigint DEFAULT 0;
alter table public.dm2_storage_directory
    add column if not exists dsdotheroption jsonb;
alter table public.dm2_storage_directory
    add column if not exists dsduserid character varying(100) COLLATE pg_catalog."default";
alter table public.dm2_storage_directory
    add column if not exists dsdscanmemo text COLLATE pg_catalog."default";
alter table public.dm2_storage_directory
    add column if not exists dsd_bus_status character varying(100) COLLATE pg_catalog."default" DEFAULT 'inbound'::character varying;
alter table public.dm2_storage_directory
    add column if not exists dsd_ib_id character varying(100) COLLATE pg_catalog."default";

COMMENT ON COLUMN public.dm2_storage_directory.dsd_volumn_now
    IS '存储-容积-当前值';

COMMENT ON COLUMN public.dm2_storage_directory.dsdotheroption
    IS '其他';

COMMENT ON COLUMN public.dm2_storage_directory.dsduserid
    IS '数管-存储-目录-用户';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscanmemo
    IS '数管-目录-识别备注';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_bus_status
    IS '业务状态';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_ib_id
    IS '入库标识';

CREATE INDEX if not exists idx_dm2_storage_directory_bus_status
    ON public.dm2_storage_directory USING btree
        (dsd_bus_status COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

alter table public.dm2_storage_directory
    drop column if exists dsdidentifystatus;
alter table public.dm2_storage_directory
    drop column if exists dsdidentifyresult;


/*
    dm2_storage_file
*/


alter table public.dm2_storage_file
    drop column if exists dsdidentifystatus;
alter table public.dm2_storage_file
    drop column if exists dsdidentifyresult;
alter table public.dm2_storage_file
    drop column if exists dsffileattr;

alter table public.dm2_storage_file
    add column if not exists dsfotheroption jsonb;
alter table public.dm2_storage_file
    add column if not exists dsfuserid character varying(100) COLLATE pg_catalog."default";
alter table public.dm2_storage_file
    add column if not exists dsfscanmemo text COLLATE pg_catalog."default";
alter table public.dm2_storage_file
    add column if not exists dsf_bus_status character varying(100) COLLATE pg_catalog."default" DEFAULT 'inbound'::character varying;
alter table public.dm2_storage_file
    add column if not exists dsf_ib_id character varying(100) COLLATE pg_catalog."default";

COMMENT ON COLUMN public.dm2_storage_file.dsfotheroption
    IS '其他';

COMMENT ON COLUMN public.dm2_storage_file.dsfuserid
    IS '数管-存储-文件-用户';

COMMENT ON COLUMN public.dm2_storage_file.dsfscanmemo
    IS '数管-文件-识别备注';

COMMENT ON COLUMN public.dm2_storage_file.dsf_bus_status
    IS '业务状态';

COMMENT ON COLUMN public.dm2_storage_file.dsf_ib_id
    IS '入库标识';

CREATE INDEX if not exists idx_dm2_storage_file_bus_status
    ON public.dm2_storage_file USING btree
        (dsf_bus_status COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX if not exists idx_dm2_storage_file_otheroption
    ON public.dm2_storage_file USING gin
        (dsfotheroption)
    TABLESPACE pg_default;

CREATE INDEX if not exists idx_dm2_storage_file_user_id
    ON public.dm2_storage_file USING btree
        (dsfuserid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

DROP TABLE if exists public.dm2_storage_inbound;

CREATE TABLE if not exists public.dm2_storage_inbound
(
    dsiid              character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsistorageid       character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsidirectory       character varying(2000) COLLATE pg_catalog."default",
    dsiotheroption     jsonb,
    dsiaddtime         timestamp(6) without time zone DEFAULT now(),
    dsistatus          integer                        DEFAULT 0,
    dsiproctime        timestamp(6) without time zone DEFAULT now(),
    dsiprocid          character varying(100) COLLATE pg_catalog."default",
    dsiprocmemo        text COLLATE pg_catalog."default",
    dsimemo            text COLLATE pg_catalog."default",
    dsi_na_status      integer                        DEFAULT 1,
    dsi_na_proc_id     character varying(100) COLLATE pg_catalog."default",
    dsi_na_proc_memo   text COLLATE pg_catalog."default",
    dsidirectoryid     character varying(100) COLLATE pg_catalog."default",
    dsiuserid          character varying(100) COLLATE pg_catalog."default",
    dsitargetstorageid character varying(100) COLLATE pg_catalog."default",
    dsibatchno         character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT dm2_storage_inbound_pk PRIMARY KEY (dsiid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_inbound
    OWNER to postgres;

COMMENT ON TABLE public.dm2_storage_inbound
    IS '数管-入库';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiid
    IS '标识';

COMMENT ON COLUMN public.dm2_storage_inbound.dsistorageid
    IS '存储标识';

COMMENT ON COLUMN public.dm2_storage_inbound.dsidirectory
    IS '目录名称';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiotheroption
    IS '其他属性';

COMMENT ON COLUMN public.dm2_storage_inbound.dsistatus
    IS '处理状态';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiproctime
    IS '最小处理时间';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiprocid
    IS '处理标识';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiprocmemo
    IS '处理结果';

COMMENT ON COLUMN public.dm2_storage_inbound.dsimemo
    IS '备注';

COMMENT ON COLUMN public.dm2_storage_inbound.dsi_na_status
    IS '入库结束-通知应用-状态';

COMMENT ON COLUMN public.dm2_storage_inbound.dsi_na_proc_id
    IS '入库结束-通知应用-并行';

COMMENT ON COLUMN public.dm2_storage_inbound.dsi_na_proc_memo
    IS '入库结束-通知应用-备注';

COMMENT ON COLUMN public.dm2_storage_inbound.dsidirectoryid
    IS '入库目录标识';

COMMENT ON COLUMN public.dm2_storage_inbound.dsiuserid
    IS '数管-存储-入库-用户';

COMMENT ON COLUMN public.dm2_storage_inbound.dsitargetstorageid
    IS '目标存储标识';

COMMENT ON COLUMN public.dm2_storage_inbound.dsibatchno
    IS '批次编号';
-- Index: idx_dm2_storage_inbound_na_procid

-- DROP INDEX public.idx_dm2_storage_inbound_na_procid;

CREATE INDEX if not exists idx_dm2_storage_inbound_na_procid
    ON public.dm2_storage_inbound USING btree
        (dsi_na_proc_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_inbound_otheroption

-- DROP INDEX public.idx_dm2_storage_inbound_otheroption;

CREATE INDEX if not exists idx_dm2_storage_inbound_otheroption
    ON public.dm2_storage_inbound USING gin
        (dsiotheroption)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_inbound_procid

-- DROP INDEX public.idx_dm2_storage_inbound_procid;

CREATE INDEX if not exists idx_dm2_storage_inbound_procid
    ON public.dm2_storage_inbound USING btree
        (dsiprocid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

DROP TABLE if exists public.dm2_storage_inbound_log;

CREATE TABLE if not exists public.dm2_storage_inbound_log
(
    dsilid         bigserial                                           NOT NULL,
    dsilownerid    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsildirectory  character varying(2000) COLLATE pg_catalog."default",
    dsilfilename   character varying(2000) COLLATE pg_catalog."default",
    dsilobjectname character varying(100) COLLATE pg_catalog."default",
    dsilobjecttype character varying(100) COLLATE pg_catalog."default",
    dsiladdtime    timestamp(6) without time zone DEFAULT now(),
    dsilinbound    integer                        DEFAULT 0,
    CONSTRAINT dm2_storage_inbound_log_pk PRIMARY KEY (dsilid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_inbound_log
    OWNER to postgres;

COMMENT ON TABLE public.dm2_storage_inbound_log
    IS '数管-入库-日志';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilid
    IS '标识';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilownerid
    IS '所属入库记录标识';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsildirectory
    IS '目录';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilfilename
    IS '文件名';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilobjectname
    IS '对象名';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilobjecttype
    IS '对象类型';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsiladdtime
    IS '添加时间';

COMMENT ON COLUMN public.dm2_storage_inbound_log.dsilinbound
    IS '是否允许入库';


/*
    dm2_storage_obj_detail
*/

alter table public.dm2_storage_obj_detail
    drop column if exists dod_parentid;
alter table public.dm2_storage_obj_detail
    add column if not exists dodfiletype character varying(100) COLLATE pg_catalog."default" DEFAULT 'file'::character varying;
alter table public.dm2_storage_obj_detail
    add column if not exists dodfilecount bigint DEFAULT 1;
alter table public.dm2_storage_obj_detail
    add column if not exists doddircount bigint DEFAULT 0;
alter table public.dm2_storage_obj_detail
    add column if not exists dodother jsonb;

DROP TABLE if exists public.dm2_storage_obj_na;

CREATE TABLE if not exists public.dm2_storage_obj_na
(
    dsonid                bigserial NOT NULL,
    dson_object_id        character varying(100) COLLATE pg_catalog."default",
    dson_app_id           character varying(200) COLLATE pg_catalog."default",
    dson_notify_status    integer                        DEFAULT 1,
    dson_notify_proc_id   character varying(100) COLLATE pg_catalog."default",
    dson_notify_proc_memo text COLLATE pg_catalog."default",
    dson_addtime          timestamp(6) without time zone DEFAULT now(),
    dson_object_access    character varying(100) COLLATE pg_catalog."default",
    dson_audit_username   character varying(100) COLLATE pg_catalog."default",
    dson_audit_time       timestamp(6) without time zone,
    dson_lastmodify_time  timestamp(6) without time zone DEFAULT now(),
    dson_access_memo      text COLLATE pg_catalog."default",
    dson_inbound_id       character varying(100) COLLATE pg_catalog."default",
    dson_otheroption      jsonb,
    CONSTRAINT dm2_storage_obj_na_pk PRIMARY KEY (dsonid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_obj_na
    OWNER to postgres;

COMMENT ON TABLE public.dm2_storage_obj_na
    IS '数管-对象-同步';

COMMENT ON COLUMN public.dm2_storage_obj_na.dsonid
    IS '标识';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_object_id
    IS '对象标识';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_app_id
    IS '应用标识';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_notify_status
    IS '通知状态';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_notify_proc_id
    IS '并行标识';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_notify_proc_memo
    IS '通知结果';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_addtime
    IS '添加时间';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_object_access
    IS '对象-访问权限';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_audit_username
    IS '对象-审批人员';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_audit_time
    IS '对象-审批时间';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_lastmodify_time
    IS '最后修改时间';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_access_memo
    IS '可用性分析备注';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_inbound_id
    IS '入库批次标识';

COMMENT ON COLUMN public.dm2_storage_obj_na.dson_otheroption
    IS '其他属性';
-- Index: idx_dm2_storage_obj_na_access

-- DROP INDEX public.idx_dm2_storage_obj_na_access;

CREATE INDEX if not exists idx_dm2_storage_obj_na_access
    ON public.dm2_storage_obj_na USING btree
        (dson_object_access COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_obj_na_app_id

-- DROP INDEX public.idx_dm2_storage_obj_na_app_id;

CREATE INDEX if not exists idx_dm2_storage_obj_na_app_id
    ON public.dm2_storage_obj_na USING btree
        (dson_app_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_obj_na_object_id

-- DROP INDEX public.idx_dm2_storage_obj_na_object_id;

CREATE INDEX if not exists idx_dm2_storage_obj_na_object_id
    ON public.dm2_storage_obj_na USING btree
        (dson_object_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_obj_na_otheroption

-- DROP INDEX public.idx_dm2_storage_obj_na_otheroption;

CREATE INDEX if not exists idx_dm2_storage_obj_na_otheroption
    ON public.dm2_storage_obj_na USING gin
        (dson_otheroption)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_obj_na_proc_id

-- DROP INDEX public.idx_dm2_storage_obj_na_proc_id;

CREATE INDEX if not exists idx_dm2_storage_obj_na_proc_id
    ON public.dm2_storage_obj_na USING btree
        (dson_notify_proc_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_obj_na_status

-- DROP INDEX public.idx_dm2_storage_obj_na_status;

CREATE INDEX if not exists idx_dm2_storage_obj_na_status
    ON public.dm2_storage_obj_na USING btree
        (dson_notify_status ASC NULLS LAST)
    TABLESPACE pg_default;

/*
    dm2_storage_object
*/
alter table public.dm2_storage_object
    drop column if exists dso_hand_status;
alter table public.dm2_storage_object
    drop column if exists dsolastprocessstatus;
alter table public.dm2_storage_object
    drop column if exists dsolastprocessprocid;
alter table public.dm2_storage_object
    drop column if exists dsolastprocessmemo;
alter table public.dm2_storage_object
    drop column if exists dsolastprocess_starttime;
alter table public.dm2_storage_object
    drop column if exists dsolastprocess_endtime;
alter table public.dm2_storage_object
    drop column if exists dsolastprocess_status;
alter table public.dm2_storage_object
    drop column if exists dsolastprocess_geomtaskid;
alter table public.dm2_storage_object
    drop column if exists dsolastprocess_pictaskid;
alter table public.dm2_storage_object
    drop column if exists dsometadata_bus_parsestatus;

alter table public.dm2_storage_object
    add column if not exists dso_metadata_bus_result integer DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_quality xml;
alter table public.dm2_storage_object
    add column if not exists dso_metadata_result integer DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_volumn_now bigint DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_add_time timestamp(6) without time zone DEFAULT now();
alter table public.dm2_storage_object
    add column if not exists dso_time_parsermemo text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_time_result integer DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_time jsonb;
alter table public.dm2_storage_object
    add column if not exists dso_spatial_parsermemo text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_spatial_result integer DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_geo_bb_wgs84 geometry;
alter table public.dm2_storage_object
    add column if not exists dso_geo_wgs84 geometry;
alter table public.dm2_storage_object
    add column if not exists dso_center_wgs84 geometry;
alter table public.dm2_storage_object
    add column if not exists dso_prj_proj4 character varying(200) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_prj_coordinate character varying(50) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_prj_degree character varying(10) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_prj_zone character varying(10) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_prj_source integer DEFAULT 1;
alter table public.dm2_storage_object
    add column if not exists dso_prj_wkt character varying(1000) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_prj_project character varying(50) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_view_parsermemo text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_view_result integer DEFAULT 0;
alter table public.dm2_storage_object
    add column if not exists dso_browser character varying(2000) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_thumb character varying(2000) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_da_status integer DEFAULT 1;
alter table public.dm2_storage_object
    add column if not exists dso_da_proc_id character varying(100) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_da_result jsonb;
alter table public.dm2_storage_object
    add column if not exists dsootheroption jsonb;
alter table public.dm2_storage_object
    add column if not exists dso_quality_summary jsonb;
alter table public.dm2_storage_object
    add column if not exists dso_da_proc_memo text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_center_native text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_geo_native text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_geo_bb_native text COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dsocopystat jsonb;
alter table public.dm2_storage_object
    add column if not exists dso_obj_lastmodifytime timestamp(6) without time zone;
alter table public.dm2_storage_object
    add column if not exists dso_bus_status character varying(100) COLLATE pg_catalog."default" DEFAULT 'inbound'::character varying;
alter table public.dm2_storage_object
    add column if not exists dso_ib_id character varying(100) COLLATE pg_catalog."default";
alter table public.dm2_storage_object
    add column if not exists dso_priority integer DEFAULT 0;

COMMENT ON COLUMN public.dm2_storage_object.dsoid
    IS '标识';

COMMENT ON COLUMN public.dm2_storage_object.dsoobjectname
    IS '对象名称';

COMMENT ON COLUMN public.dm2_storage_object.dsoobjecttype
    IS '对象类型';

COMMENT ON COLUMN public.dm2_storage_object.dsodatatype
    IS '数据类型:dir-目录;file-文件';

COMMENT ON COLUMN public.dm2_storage_object.dsoalphacode
    IS '拼音';

COMMENT ON COLUMN public.dm2_storage_object.dsoaliasname
    IS '别名';

COMMENT ON COLUMN public.dm2_storage_object.dsoparentobjid
    IS '父对象标识';

COMMENT ON COLUMN public.dm2_storage_object.dso_volumn_now
    IS '存储-容积-当前值';

COMMENT ON COLUMN public.dm2_storage_object.dso_add_time
    IS '入库时间';

COMMENT ON COLUMN public.dm2_storage_object.dsolastmodifytime
    IS '记录最后刷新时间';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparseprocid
    IS '元数据提取进程标识';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparsestatus
    IS '元数据提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dso_quality
    IS '质检详情';

COMMENT ON COLUMN public.dm2_storage_object.dso_metadata_result
    IS '元数据解析结果';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparsememo
    IS '元数据提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatype
    IS '元数据类型;0-txt;1-json;2-xml';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatext
    IS '元数据text';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatajson
    IS '元数据json';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataxml
    IS '元数据xml';

COMMENT ON COLUMN public.dm2_storage_object.dso_metadata_bus_result
    IS '业务元数据解析结果';

COMMENT ON COLUMN public.dm2_storage_object.dsometadata_bus_parsememo
    IS '业务元数据收割备注';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatype_bus
    IS '元数据类型;0-txt;1-json;2-xml';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatext_bus
    IS '业务元数据文本';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatajson_bus
    IS '业务元数据Json';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataxml_bus
    IS '业务元数据XML';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparseprocid
    IS '明细提取标识';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparsestatus
    IS '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparsememo
    IS '明细提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dsotags
    IS '标签';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparseprocid
    IS '明细提取标识';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparsestatus
    IS '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparsememo
    IS '明细提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dso_time_parsermemo
    IS '时间解析说明';

COMMENT ON COLUMN public.dm2_storage_object.dso_time_result
    IS '时间元数据解析结果';

COMMENT ON COLUMN public.dm2_storage_object.dso_time
    IS '时间';

COMMENT ON COLUMN public.dm2_storage_object.dso_spatial_parsermemo
    IS '空间解析说明';

COMMENT ON COLUMN public.dm2_storage_object.dso_spatial_result
    IS '空间元数据解析结果';

COMMENT ON COLUMN public.dm2_storage_object.dso_geo_bb_wgs84
    IS '对象-WGS84-外包框';

COMMENT ON COLUMN public.dm2_storage_object.dso_geo_wgs84
    IS '对象-WGS84-外边框';

COMMENT ON COLUMN public.dm2_storage_object.dso_center_wgs84
    IS '对象-WGS84-中心点';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_proj4
    IS '坐标投影-proj4';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_coordinate
    IS '坐标投影-坐标系';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_degree
    IS '坐标投影-度';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_zone
    IS '坐标投影-带';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_source
    IS '坐标投影-信息来源;1-实体;2-业务元数据;9-人工指定';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_wkt
    IS '坐标投影-wkt';

COMMENT ON COLUMN public.dm2_storage_object.dso_prj_project
    IS '坐标投影-投影';

COMMENT ON COLUMN public.dm2_storage_object.dso_view_parsermemo
    IS '可视化解析说明';

COMMENT ON COLUMN public.dm2_storage_object.dso_view_result
    IS '可视化元数据解析结果';

COMMENT ON COLUMN public.dm2_storage_object.dso_browser
    IS '快视图文件地址';

COMMENT ON COLUMN public.dm2_storage_object.dso_thumb
    IS '拇指图文件地址';

COMMENT ON COLUMN public.dm2_storage_object.dso_da_status
    IS '发布规则审核-状态';

COMMENT ON COLUMN public.dm2_storage_object.dso_da_proc_id
    IS '发布规则审核-并行标识';

COMMENT ON COLUMN public.dm2_storage_object.dso_da_result
    IS '发布规则审核-结果';

COMMENT ON COLUMN public.dm2_storage_object.dsootheroption
    IS '其他';

COMMENT ON COLUMN public.dm2_storage_object.dso_quality_summary
    IS '质检概况';

COMMENT ON COLUMN public.dm2_storage_object.dso_da_proc_memo
    IS '发布规则审核-备注';

COMMENT ON COLUMN public.dm2_storage_object.dso_center_native
    IS '对象-原始-中心点';

COMMENT ON COLUMN public.dm2_storage_object.dso_geo_native
    IS '对象-原始-外边框';

COMMENT ON COLUMN public.dm2_storage_object.dso_geo_bb_native
    IS '对象-原始-外包框';

COMMENT ON COLUMN public.dm2_storage_object.dsocopystat
    IS '数管-对象-副本-统计';

COMMENT ON COLUMN public.dm2_storage_object.dso_obj_lastmodifytime
    IS '数管-对象-最后修改时间';

COMMENT ON COLUMN public.dm2_storage_object.dso_bus_status
    IS '业务状态';

COMMENT ON COLUMN public.dm2_storage_object.dso_ib_id
    IS '入库标识';

COMMENT ON COLUMN public.dm2_storage_object.dso_priority
    IS '优先级';

CREATE INDEX if not exists idx_dm2_storage_object_bus_status
    ON public.dm2_storage_object USING btree
        (dso_bus_status COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_copystat

-- DROP INDEX public.idx_dm2_storage_object_copystat;

CREATE INDEX if not exists idx_dm2_storage_object_copystat
    ON public.dm2_storage_object USING gin
        (dsocopystat)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_da_result

-- DROP INDEX public.idx_dm2_storage_object_da_result;

CREATE INDEX if not exists idx_dm2_storage_object_da_result
    ON public.dm2_storage_object USING gin
        (dso_da_result)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dso_center_wgs84

-- DROP INDEX public.idx_dm2_storage_object_dso_center_wgs84;

CREATE INDEX if not exists idx_dm2_storage_object_dso_center_wgs84
    ON public.dm2_storage_object USING gist
        (dso_center_wgs84)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dso_da_proc_id

-- DROP INDEX public.idx_dm2_storage_object_dso_da_proc_id;

CREATE INDEX if not exists idx_dm2_storage_object_dso_da_proc_id
    ON public.dm2_storage_object USING btree
        (dso_da_proc_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dso_geo_bb_wgs84

-- DROP INDEX public.idx_dm2_storage_object_dso_geo_bb_wgs84;

CREATE INDEX if not exists idx_dm2_storage_object_dso_geo_bb_wgs84
    ON public.dm2_storage_object USING gist
        (dso_geo_bb_wgs84)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dso_geo_wgs84

-- DROP INDEX public.idx_dm2_storage_object_dso_geo_wgs84;

CREATE INDEX if not exists idx_dm2_storage_object_dso_geo_wgs84
    ON public.dm2_storage_object USING gist
        (dso_geo_wgs84)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dsodetailparsestatus

-- DROP INDEX public.idx_dm2_storage_object_dsodetailparsestatus;

CREATE INDEX if not exists idx_dm2_storage_object_dsodetailparsestatus
    ON public.dm2_storage_object USING btree
        (dsodetailparsestatus ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dsometadataparseprocid

-- DROP INDEX public.idx_dm2_storage_object_dsometadataparseprocid;

CREATE INDEX if not exists idx_dm2_storage_object_dsometadataparseprocid
    ON public.dm2_storage_object USING btree
        (dsometadataparseprocid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_dsotagsparsestatus

-- DROP INDEX public.idx_dm2_storage_object_dsotagsparsestatus;

CREATE INDEX if not exists idx_dm2_storage_object_dsotagsparsestatus
    ON public.dm2_storage_object USING btree
        (dsotagsparsestatus ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_ib_id

-- DROP INDEX public.idx_dm2_storage_object_ib_id;

CREATE INDEX if not exists idx_dm2_storage_object_ib_id
    ON public.dm2_storage_object USING btree
        (dso_ib_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_id

-- DROP INDEX public.idx_dm2_storage_object_id;

CREATE INDEX if not exists idx_dm2_storage_object_id
    ON public.dm2_storage_object USING btree
        (dsoid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_json

-- DROP INDEX public.idx_dm2_storage_object_json;

CREATE INDEX if not exists idx_dm2_storage_object_json
    ON public.dm2_storage_object USING gin
        (dsometadatajson)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_json_bus

-- DROP INDEX public.idx_dm2_storage_object_json_bus;

CREATE INDEX if not exists idx_dm2_storage_object_json_bus
    ON public.dm2_storage_object USING gin
        (dsometadatajson_bus)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_name

-- DROP INDEX public.idx_dm2_storage_object_name;

CREATE INDEX if not exists idx_dm2_storage_object_name
    ON public.dm2_storage_object USING btree
        (dsoobjectname COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_objecttype

-- DROP INDEX public.idx_dm2_storage_object_objecttype;

CREATE INDEX if not exists idx_dm2_storage_object_objecttype
    ON public.dm2_storage_object USING btree
        (dsoobjecttype COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_option

-- DROP INDEX public.idx_dm2_storage_object_option;

CREATE INDEX if not exists idx_dm2_storage_object_option
    ON public.dm2_storage_object USING gin
        (dsootheroption)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_proj4

-- DROP INDEX public.idx_dm2_storage_object_proj4;

CREATE INDEX if not exists idx_dm2_storage_object_proj4
    ON public.dm2_storage_object USING btree
        (dso_prj_proj4 COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_tag

-- DROP INDEX public.idx_dm2_storage_object_tag;

CREATE INDEX if not exists idx_dm2_storage_object_tag
    ON public.dm2_storage_object USING btree
        (dsotags COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_time

-- DROP INDEX public.idx_dm2_storage_object_time;

CREATE INDEX if not exists idx_dm2_storage_object_time
    ON public.dm2_storage_object USING gin
        (dso_time)
    TABLESPACE pg_default;


DROP TABLE public.dm2_storage_object_def;

CREATE TABLE public.dm2_storage_object_def
(
    dsodid           character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsodtitle        character varying(1000) COLLATE pg_catalog."default",
    dsodtype         character varying(100) COLLATE pg_catalog."default",
    dsodtypetitle    character varying(100) COLLATE pg_catalog."default",
    dsodtypecode     character varying(100) COLLATE pg_catalog."default",
    dsodgroup        character varying(100) COLLATE pg_catalog."default",
    dsodgrouptitle   character varying(100) COLLATE pg_catalog."default",
    dsodcatalog      character varying(100) COLLATE pg_catalog."default",
    dsodcatalogtitle character varying(100) COLLATE pg_catalog."default",
    dsod_otheroption jsonb,
    CONSTRAINT dm2_storage_object_def_pkey PRIMARY KEY (dsodid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_object_def
    OWNER to postgres;

COMMENT ON TABLE public.dm2_storage_object_def
    IS '数管-存储目录-对象-定义';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodid
    IS '对象标识';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtitle
    IS '对象标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtype
    IS '类型';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtypetitle
    IS '类型标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtypecode
    IS '类型编码';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodgroup
    IS '数管-定义-分组名称';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodgrouptitle
    IS '数管-定义-分组标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodcatalog
    IS '数据类别';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodcatalogtitle
    IS '数据类别-标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsod_otheroption
    IS '其他属性';
-- Index: idx_dm2_storage_object_def_catalog

-- DROP INDEX public.idx_dm2_storage_object_def_catalog;

CREATE INDEX idx_dm2_storage_object_def_catalog
    ON public.dm2_storage_object_def USING btree
        (dsodcatalog COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_def_group

-- DROP INDEX public.idx_dm2_storage_object_def_group;

CREATE INDEX idx_dm2_storage_object_def_group
    ON public.dm2_storage_object_def USING btree
        (dsodgroup COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_def_id

-- DROP INDEX public.idx_dm2_storage_object_def_id;

CREATE INDEX idx_dm2_storage_object_def_id
    ON public.dm2_storage_object_def USING btree
        (dsodid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_def_otheroption

-- DROP INDEX public.idx_dm2_storage_object_def_otheroption;

CREATE INDEX idx_dm2_storage_object_def_otheroption
    ON public.dm2_storage_object_def USING gin
        (dsod_otheroption)
    TABLESPACE pg_default;
-- Index: idx_dm2_storage_object_def_type

-- DROP INDEX public.idx_dm2_storage_object_def_type;

CREATE INDEX idx_dm2_storage_object_def_type
    ON public.dm2_storage_object_def USING btree
        (dsodtype COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


/*
    sch_event and sch_mission
*/

-- Table: public.sch_center

DROP TABLE if exists public.sch_center;

CREATE TABLE public.sch_center
(
    scid             character varying(100) COLLATE pg_catalog."default" NOT NULL,
    sctitle          character varying(200) COLLATE pg_catalog."default" NOT NULL,
    scstatus         integer DEFAULT 1,
    scprocessid      character varying(100) COLLATE pg_catalog."default",
    sclastmodifytime timestamp(6) without time zone,
    scmemo           text COLLATE pg_catalog."default",
    scserver         character varying(100) COLLATE pg_catalog."default",
    sccommand        character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT sch_center_pkey PRIMARY KEY (scid)
)
    TABLESPACE pg_default;

ALTER TABLE public.sch_center
    OWNER to postgres;

COMMENT ON TABLE public.sch_center
    IS '调度-中心';

COMMENT ON COLUMN public.sch_center.scid
    IS '标识';

COMMENT ON COLUMN public.sch_center.sctitle
    IS '标题';

COMMENT ON COLUMN public.sch_center.scstatus
    IS '-1: 停止，0：启动，1：等待启动，2：启动中';

COMMENT ON COLUMN public.sch_center.scprocessid
    IS '并行处理标识';

COMMENT ON COLUMN public.sch_center.sclastmodifytime
    IS '最后修改时间';

COMMENT ON COLUMN public.sch_center.scmemo
    IS '备注';

COMMENT ON COLUMN public.sch_center.scserver
    IS '服务器';

COMMENT ON COLUMN public.sch_center.sccommand
    IS '命令';
-- Index: idx_sch_center_processid

-- DROP INDEX public.idx_sch_center_processid;

CREATE INDEX idx_sch_center_processid
    ON public.sch_center USING btree
        (scprocessid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_sch_center_status

-- DROP INDEX public.idx_sch_center_status;

CREATE INDEX idx_sch_center_status
    ON public.sch_center USING btree
        (scstatus ASC NULLS LAST)
    TABLESPACE pg_default;

DROP TABLE if exists public.sch_center_mission;

CREATE TABLE public.sch_center_mission
(
    scmid             character varying(100) COLLATE pg_catalog."default" NOT NULL,
    scmtitle          character varying(200) COLLATE pg_catalog."default" NOT NULL,
    scmcommand        character varying(100) COLLATE pg_catalog."default",
    scmstatus         integer                        DEFAULT 1,
    scmprocessid      character varying(100) COLLATE pg_catalog."default",
    scmlastmodifytime timestamp(6) without time zone DEFAULT now(),
    scmcenterid       character varying(100) COLLATE pg_catalog."default",
    scmtrigger        text COLLATE pg_catalog."default",
    scmalgorithm      character varying(200) COLLATE pg_catalog."default" NOT NULL,
    scmparams         jsonb,
    scmmemo           text COLLATE pg_catalog."default",
    CONSTRAINT sch_center_mission_pkey PRIMARY KEY (scmid)
)
    TABLESPACE pg_default;

ALTER TABLE public.sch_center_mission
    OWNER to postgres;

COMMENT ON TABLE public.sch_center_mission
    IS '调度-中心';

COMMENT ON COLUMN public.sch_center_mission.scmid
    IS '标识';

COMMENT ON COLUMN public.sch_center_mission.scmtitle
    IS '标题';

COMMENT ON COLUMN public.sch_center_mission.scmcommand
    IS '命令';

COMMENT ON COLUMN public.sch_center_mission.scmstatus
    IS '状态 0：完成，1：待处理，2：处理中';

COMMENT ON COLUMN public.sch_center_mission.scmprocessid
    IS '并行处理标识';

COMMENT ON COLUMN public.sch_center_mission.scmlastmodifytime
    IS '最后修改时间';

COMMENT ON COLUMN public.sch_center_mission.scmcenterid
    IS '所属组标示';

COMMENT ON COLUMN public.sch_center_mission.scmtrigger
    IS '触发器';

COMMENT ON COLUMN public.sch_center_mission.scmalgorithm
    IS '算法';

COMMENT ON COLUMN public.sch_center_mission.scmparams
    IS '详细参数';

COMMENT ON COLUMN public.sch_center_mission.scmmemo
    IS '备注';
-- Index: idx_sch_center_mission_id

-- DROP INDEX public.idx_sch_center_mission_id;

CREATE INDEX idx_sch_center_mission_id
    ON public.sch_center_mission USING btree
        (scmid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_sch_center_mission_processid

-- DROP INDEX public.idx_sch_center_mission_processid;

CREATE INDEX idx_sch_center_mission_processid
    ON public.sch_center_mission USING btree
        (scmprocessid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_sch_center_mission_status

-- DROP INDEX public.idx_sch_center_mission_status;

CREATE INDEX idx_sch_center_mission_status
    ON public.sch_center_mission USING btree
        (scmstatus ASC NULLS LAST)
    TABLESPACE pg_default;

INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('10.job_dm_ib_storage_scan_monitor', '入库存储-扫描入库监控', 'shutdown', 0, 'b55d82a228763c58987a36847f992e2f',
        '2020-09-09 00:26:53.464786', null, 'interval', 'job_dm_ib_storage_scan_monitor', '{
    "trigger": {
      "seconds": 15
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('10.job_dm_ib_storage_sch_scan_monitor', '入库存储-定时扫描入库监控', 'shutdown', 0, '276be817f8e330c9aed5e6895333db1f',
        '2020-09-09 00:26:53.464786', null, 'interval', 'job_dm_ib_storage_sch_scan_monitor', '{
    "trigger": {
      "seconds": 60
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('10.job_dm_root_parser', '混合存储-扫描入库-兼容旧版本', 'shutdown', 0, '31557ee0a0ab3ed78bed090ea55800a0',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_root_parser', '{
    "process": {
      "parallel_count": 1
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('11.job_dm_path_parser', '子目录扫描', 'shutdown', 0, 'a4b8650dc6ef3c5599ab453a1153ddc5',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_path_parser', '{
    "process": {
      "parallel_count": 3
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('12.job_dm_path2object', '目录识别', 'shutdown', 0, 'ee2f44f9cfa43f8d836883abf59670ef',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_path2object', '{
    "process": {
      "parallel_count": 3
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('13.job_dm_file2object', '文件识别', 'shutdown', 0, '9e853125a64d33c8b789d9109172af7c',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_file2object', '{
    "process": {
      "parallel_count": 6
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('14.job_dm_obj_metadata', '对象-核心-解析', 'shutdown', 0, 'dd1d88fdaa01329b82e3e8d1ad976b89',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_obj_metadata', '{
    "process": {
      "parallel_count": 3
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('15.job_dm_obj_detail', '对象-附属文件-解析', 'shutdown', 0, 'f9d902d5a3a638ea92fbb775842bb0db',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_obj_detail', '{
    "process": {
      "parallel_count": 2
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('16.job_dm_obj_tags', '对象-业务分类-解析', 'shutdown', 0, '020193282fc93eee954668f437b2afdd',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_obj_tags', '{
    "process": {
      "parallel_count": 2
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('17.job_dm_obj_da', '对象-第三方模块发布-解析', 'shutdown', 0, '291dc2fa2de232978414d11f3f820d8a',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_obj_da', '{
    "process": {
      "parallel_count": 3
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('18.job_dm_inbound_qi', '入库-质量检验', 'shutdown', 0, 'aa72037541d93a5095a7a608ce41bfff',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_inbound_qi', '{
    "process": {
      "parallel_count": 1
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('19.job_dm_inbound_qi_monitor', '入库-质量检验-进度监控', 'shutdown', 0, '3de3d2a70af2379b87348b961b15bc71',
        '2020-09-09 00:26:53.464786', null, 'interval', 'job_dm_inbound_qi_monitor', '{
    "trigger": {
      "seconds": 15
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('20.job_dm_inbound', '入库', 'shutdown', 0, 'bcc1d78fe16e341fa133754a11546b59', '2020-09-09 00:26:53.464786',
        null, 'db_queue', 'job_dm_inbound', '{
    "process": {
      "parallel_count": 1
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('21.job_dm_inbound_notify', '入库-通知', 'shutdown', 0, '208e247964933b1ca7ec077e5304bdf1',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_inbound_notify', '{
    "process": {
      "parallel_count": 1
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('22.job_dm_inbound_notify_monitor', '入库-通知-进度监控', 'shutdown', 0, '197f8ca686823d87ac9cd38ec134f773',
        '2020-09-09 00:26:53.464786', null, 'interval', 'job_dm_inbound_notify_monitor', '{
    "trigger": {
      "seconds": 15
    }
  }', null);
INSERT INTO public.sch_center_mission (scmid, scmtitle, scmcommand, scmstatus, scmprocessid, scmlastmodifytime,
                                       scmcenterid, scmtrigger, scmalgorithm, scmparams, scmmemo)
VALUES ('23.job_dm_sync_app', '元数据-同步-应用', 'shutdown', 0, 'd5c381d395d5374d833029f5ee94567b',
        '2020-09-09 00:26:53.464786', null, 'db_queue', 'job_dm_sync_app', '{
    "process": {
      "parallel_count": 3
    }
  }', null);



CREATE SEQUENCE if not exists public.sys_seq_autoinc
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE public.sys_seq_autoinc
    OWNER TO postgres;

CREATE SEQUENCE if not exists public.sys_seq_date_autoinc
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE public.sys_seq_date_autoinc
    OWNER TO postgres;


CREATE TABLE if not exists public.dm2_modules
(
    dmid    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dmtitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT dm2_modules_pkey PRIMARY KEY (dmid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_modules
    OWNER to postgres;

COMMENT ON TABLE public.dm2_modules
    IS '数管-第三方模块';

COMMENT ON COLUMN public.dm2_modules.dmid
    IS '标识';

COMMENT ON COLUMN public.dm2_modules.dmtitle
    IS '名称';

CREATE TABLE if not exists public.dm2_quality_group
(
    dqgid    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dqgtitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT dm2_quality_group_pkey PRIMARY KEY (dqgid)
)
    TABLESPACE pg_default;

ALTER TABLE public.dm2_quality_group
    OWNER to postgres;

COMMENT ON TABLE public.dm2_quality_group
    IS '数管-质检-分组';

COMMENT ON COLUMN public.dm2_quality_group.dqgid
    IS '标识';

COMMENT ON COLUMN public.dm2_quality_group.dqgtitle
    IS '描述';
