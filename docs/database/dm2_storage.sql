/*
    2020-10-15
    . 重新整理数据库结构
        . 优化了dm2_storage\dm2_storage_object_def\dm2_storage_object
*/

create table dm2_storage
(
	dstid varchar(100) not null
		constraint dm2_storage_pkey
			primary key,
	dsttitle varchar(200) not null,
	dstunipath varchar(4000),
	dstwatch integer,
	dstwatchperiod varchar(50),
	dstscanlasttime timestamp(6),
	dstscanstatus integer default 1,
	dstprocessid varchar(100),
	dstaddtime timestamp(6) default now(),
	dstlastmodifytime timestamp(6),
	dstmemo varchar(200),
	dstotheroption jsonb,
	dst_volumn_max bigint default 0,
	dst_volumn_warn bigint default 0,
	dst_volumn_now bigint default 0
);

comment on table dm2_storage is '数管-存储目录';

comment on column dm2_storage.dstid is '标识，guid';

comment on column dm2_storage.dsttitle is '数据管理员当前电脑数据目录 Z:\\data';

comment on column dm2_storage.dstunipath is '网络盘符的ip地址路径\\000.000.000.000\data';

comment on column dm2_storage.dstwatch is '是否自动监控本目录编号，0：不是  1：是 默认为1';

comment on column dm2_storage.dstwatchperiod is '监控扫描周期，1.一周；2.一月';

comment on column dm2_storage.dstscanlasttime is '上次扫描时间';

comment on column dm2_storage.dstscanstatus is '0：已扫描完毕；1：立刻扫描；2：扫描中';

comment on column dm2_storage.dstprocessid is '并行处理标识';

comment on column dm2_storage.dstaddtime is '添加时间';

comment on column dm2_storage.dstlastmodifytime is '最后修改时间';

comment on column dm2_storage.dstmemo is '备注';

comment on column dm2_storage.dstotheroption is '其他配置';

comment on column dm2_storage.dst_volumn_max is '存储-容积-最大值';

comment on column dm2_storage.dst_volumn_warn is '存储-容积-警告值';

comment on column dm2_storage.dst_volumn_now is '存储-容积-当前值';

alter table dm2_storage owner to postgres;

create index idx_dm2_storage_processid
	on dm2_storage (dstprocessid);

create index idx_dm2_storage_scanstatus
	on dm2_storage (dstscanstatus);

create index idx_dm2_storage_title
	on dm2_storage (dsttitle);

create index idx_dm2_storage_watch
	on dm2_storage (dstwatch);

create index idx_dm2_storage_watchperiod
	on dm2_storage (dstwatchperiod);

create table dm2_storage_directory
(
	dsdid varchar(100) not null
		constraint dm2_storage_directory_pkey
			primary key,
	dsdparentid varchar(100) not null,
	dsdstorageid varchar(100) not null,
	dsddirectory varchar(4000) not null,
	dsddirtype varchar(100),
	dsdscanstatus integer default 1,
	dsdprocessid varchar(100),
	dsdaddtime timestamp(6) default now(),
	dsdlastmodifytime timestamp(6),
	dsddirectoryname varchar(1000),
	dsd_object_type varchar(100),
	dsd_object_confirm integer default 0,
	dsd_object_id varchar(200),
	dsd_directory_valid integer default '-1'::integer,
	dsdscanfilestatus integer default 1,
	dsdscanfileprocessid varchar(100),
	dsdscandirstatus integer default 1,
	dsdscandirprocessid varchar(100),
	dsdpath varchar(4000),
	dsddircreatetime timestamp(6),
	dsddirlastmodifytime timestamp(6),
	dsddirscanpriority integer default 0,
	dsdparentobjid varchar(100),
	dsdscanrule xml,
	dsd_volumn_now bigint default 0
);

comment on table dm2_storage_directory is '数管-存储目录-子目录';

comment on column dm2_storage_directory.dsdid is '标识，guid';

comment on column dm2_storage_directory.dsdparentid is 'pid父目录编号';

comment on column dm2_storage_directory.dsdstorageid is '存储盘编号，对应dm2_storage的dstid字段';

comment on column dm2_storage_directory.dsddirectory is '文件的相对目录路径（不带工作区路径、不带文件名）\\dir1\\dir2\\';

comment on column dm2_storage_directory.dsddirtype is '文件夹类型：1.普通目录；2.虚拟目录；3.根目录';

comment on column dm2_storage_directory.dsdscanstatus is '对象识别状态(处理完成是0，待处理是1，处理中是2)';

comment on column dm2_storage_directory.dsdprocessid is '并行识别对象标识';

comment on column dm2_storage_directory.dsdaddtime is '添加时间';

comment on column dm2_storage_directory.dsdlastmodifytime is '最后修改时间';

comment on column dm2_storage_directory.dsddirectoryname is '目录名称 dir2 ';

comment on column dm2_storage_directory.dsd_object_type is '数据对象类型';

comment on column dm2_storage_directory.dsd_object_confirm is '数据对象识别概率;-1:确认是对象;0:不知道;1:有可能;2:确认不是对象';

comment on column dm2_storage_directory.dsd_object_id is '数据对象标识';

comment on column dm2_storage_directory.dsd_directory_valid is '目录是否有效';

comment on column dm2_storage_directory.dsdscanfilestatus is '并行扫描文件状态(处理完成是0，待处理是1，处理中是2)';

comment on column dm2_storage_directory.dsdscanfileprocessid is '并行扫描文件进程';

comment on column dm2_storage_directory.dsdscandirstatus is '并行扫描子目录状态(处理完成是0，待处理是1，处理中是2)';

comment on column dm2_storage_directory.dsdscandirprocessid is '并行扫描目录进程';

comment on column dm2_storage_directory.dsdpath is '目录的上级路径';

comment on column dm2_storage_directory.dsddircreatetime is '目录创建时间';

comment on column dm2_storage_directory.dsddirlastmodifytime is '目录最后修改时间';

comment on column dm2_storage_directory.dsddirscanpriority is '目录扫描优先级';

comment on column dm2_storage_directory.dsdparentobjid is '父对象标识';

comment on column dm2_storage_directory.dsdscanrule is '扫描的规则-metadata.rule文件内容';

comment on column dm2_storage_directory.dsd_volumn_now is '存储-容积-当前值';

alter table dm2_storage_directory owner to postgres;

create index idx_dm2_storage_directory_directoryname
	on dm2_storage_directory (dsddirectoryname);

create index idx_dm2_storage_directory_dirtype
	on dm2_storage_directory (dsddirtype);

create index idx_dm2_storage_directory_dsddirectory
	on dm2_storage_directory (dsddirectory);

create index idx_dm2_storage_directory_dsdscandirprocessid
	on dm2_storage_directory (dsdscandirprocessid);

create index idx_dm2_storage_directory_dsdscandirstatus
	on dm2_storage_directory (dsdscandirstatus);

create index idx_dm2_storage_directory_dsdscanfileprocessid
	on dm2_storage_directory (dsdscanfileprocessid);

create index idx_dm2_storage_directory_dsdscanfilestatus
	on dm2_storage_directory (dsdscanfilestatus);

create index idx_dm2_storage_directory_id
	on dm2_storage_directory (dsdid);

create index idx_dm2_storage_directory_parentid
	on dm2_storage_directory (dsdparentid);

create index idx_dm2_storage_directory_processid
	on dm2_storage_directory (dsdprocessid);

create index idx_dm2_storage_directory_scanfileprocessid
	on dm2_storage_directory (dsdscanfileprocessid);

create index idx_dm2_storage_directory_scanstatus
	on dm2_storage_directory (dsdscanstatus);

create table dm2_storage_file
(
	dsfid varchar(100) not null
		constraint dm2_storage_file_pkey
			primary key,
	dsfstorageid varchar(100) not null,
	dsfdirectoryid varchar(100) not null,
	dsffilerelationname varchar(4000),
	dsffilename varchar(1000),
	dsffilemainname varchar(1000),
	dsfext varchar(100),
	dsffilecreatetime timestamp(6),
	dsffilemodifytime timestamp(6),
	dsfaddtime timestamp(6) default now(),
	dsflastmodifytime timestamp(6),
	dsffilevalid integer default '-1'::integer,
	dsfscanstatus integer default 1,
	dsfprocessid varchar(100),
	dsf_object_type varchar(100),
	dsf_object_confirm integer default 0,
	dsf_object_id varchar(200),
	dsffilesize bigint default 0,
	dsfparentobjid varchar(100)
);

comment on table dm2_storage_file is '数管-存储目录-文件';

comment on column dm2_storage_file.dsfid is '标识，guid';

comment on column dm2_storage_file.dsfstorageid is '存储盘编号';

comment on column dm2_storage_file.dsfdirectoryid is '文件的目录标识';

comment on column dm2_storage_file.dsffilerelationname is '文件相对名称';

comment on column dm2_storage_file.dsffilename is '文件名称，无路径，含扩展名';

comment on column dm2_storage_file.dsffilemainname is '文件主名，无扩展名';

comment on column dm2_storage_file.dsfext is '扩展名，无点';

comment on column dm2_storage_file.dsffilecreatetime is '文件创建时间';

comment on column dm2_storage_file.dsffilemodifytime is '文件最后修改时间';

comment on column dm2_storage_file.dsfaddtime is '记录添加时间';

comment on column dm2_storage_file.dsflastmodifytime is '记录最后刷新时间';

comment on column dm2_storage_file.dsffilevalid is '文件是否有效';

comment on column dm2_storage_file.dsfscanstatus is '对象识别状态(处理完成是0，待处理是1，处理中是2)';

comment on column dm2_storage_file.dsfprocessid is '并行处理标识';

comment on column dm2_storage_file.dsf_object_type is '数据对象类型';

comment on column dm2_storage_file.dsf_object_confirm is '数据对象识别概率;-1:确认是对象;0:不知道;1:有可能;2:确认不是对象';

comment on column dm2_storage_file.dsf_object_id is '数据对象标识';

comment on column dm2_storage_file.dsffilesize is '文件大小';

comment on column dm2_storage_file.dsfparentobjid is '父对象标识';

alter table dm2_storage_file owner to postgres;

create index idx_dm2_storage_file_dsf_object_type
	on dm2_storage_file (dsf_object_type);

create index idx_dm2_storage_file_dsfdirectoryid
	on dm2_storage_file (dsfdirectoryid);

create index idx_dm2_storage_file_dsfstorageid
	on dm2_storage_file (dsfstorageid);

create index idx_dm2_storage_file_processid
	on dm2_storage_file (dsfprocessid);

create index idx_dm2_storage_file_scanstatus
	on dm2_storage_file (dsfscanstatus);

create table dm2_storage_obj_detail
(
	dodid varchar(100) not null
		constraint dm2_storage_obj_detail_pkey
			primary key,
	dodobjectid varchar(100) not null,
	dodfilename varchar(1000) not null,
	dodfileext varchar(100),
	dodfilesize bigint default 0,
	dodfilecreatetime timestamp(6),
	dodfilemodifytime timestamp(6),
	dodlastmodifytime timestamp(6) default now(),
	dodstorageid varchar(100),
	dodfilerelationname varchar(2000),
	dodfiletype varchar(100)
);

comment on table dm2_storage_obj_detail is '数管-存储文件';

comment on column dm2_storage_obj_detail.dodid is '标识guid';

comment on column dm2_storage_obj_detail.dodobjectid is '外键，关联dm2_storage_object表中的oid字段';

comment on column dm2_storage_obj_detail.dodfilename is '文件名带扩展名 aaa.img';

comment on column dm2_storage_obj_detail.dodfileext is '文件扩展名, 带前缀点 .img';

comment on column dm2_storage_obj_detail.dodfilesize is '大小';

comment on column dm2_storage_obj_detail.dodfilecreatetime is '文件的创建时间';

comment on column dm2_storage_obj_detail.dodfilemodifytime is '文件的修改时间';

comment on column dm2_storage_obj_detail.dodlastmodifytime is '记录的最后修改时间';

comment on column dm2_storage_obj_detail.dodstorageid is '存储标识';

comment on column dm2_storage_obj_detail.dodfilerelationname is '相对路径';

comment on column dm2_storage_obj_detail.dodfiletype is '文件类型';

alter table dm2_storage_obj_detail owner to postgres;

create table dm2_storage_object
(
	dsoid varchar(100) not null
		constraint dm2_storage_object_pkey
			primary key,
	dsoobjectname varchar(1000) not null,
	dsoobjecttype varchar(100) not null,
	dsodatatype varchar(100),
	dsoalphacode varchar(100),
	dsoaliasname varchar(1000),
	dsoparentobjid varchar(100),
	dso_volumn_now bigint default 0,

	dso_add_time timestamp(6) default now(),
	dsolastmodifytime timestamp(6),

	dsometadataparseprocid varchar(100),
	dsometadataparsestatus integer default 1,

	dso_quality xml,

	dso_metadata_result integer default 0,
	dsometadataparsememo text,
	dsometadatatype integer default 0,
	dsometadatatext text,
	dsometadatajson jsonb,
	dsometadataxml xml,

	dso_metadata_bus_result integer default 0,
	dsometadata_bus_parsememo text,
	dsometadatatype_bus integer default 1,
	dsometadatatext_bus text,
	dsometadatajson_bus jsonb,
	dsometadataxml_bus xml,

	dsotagsparseprocid varchar(100),
	dsotagsparsestatus integer default 1,
	dsotagsparsememo text,
	dsotags character varying[],

	dsodetailparseprocid varchar(100),
	dsodetailparsestatus integer default 1,
	dsodetailparsememo text,

	dso_time_parsermemo text,
	dso_time_result integer default 0,
	dso_time jsonb,

	dso_spatial_parsermemo text,
	dso_spatial_result integer default 0,
	dso_geo_bb_native geometry,
	dso_geo_native geometry,
	dso_center_native geometry,
	dso_geo_bb_wgs84 geometry,
	dso_geo_wgs84 geometry,
	dso_center_wgs84 geometry,
	dso_prj_proj4 varchar(200),
	dso_prj_coordinate varchar(50),
	dso_prj_degree varchar(10),
	dso_prj_zone varchar(10),
	dso_prj_source integer default 1,
	dso_prj_wkt varchar(1000),
	dso_prj_project varchar(50),

	dso_view_parsermemo text,
	dso_view_result integer default 0,
	dso_browser varchar(2000),
	dso_thumb varchar(2000),

	dso_da_status integer default 1,
	dso_da_proc_id varchar(100),
	dso_da_result jsonb
);

comment on table dm2_storage_object is '数管-存储目录-对象';

comment on column dm2_storage_object.dsoid is '标识';

comment on column dm2_storage_object.dsoobjectname is '对象名称';

comment on column dm2_storage_object.dsoobjecttype is '对象类型';

comment on column dm2_storage_object.dsodatatype is '数据类型:dir-目录;file-文件';

comment on column dm2_storage_object.dsometadatatext is '元数据text';

comment on column dm2_storage_object.dsometadatajson is '元数据json';

comment on column dm2_storage_object.dsometadatajson_bus is '业务元数据Json';

comment on column dm2_storage_object.dsometadataxml is '元数据xml';

comment on column dm2_storage_object.dsometadatatype is '元数据类型;0-txt;1-json;2-xml';

comment on column dm2_storage_object.dsometadataparsestatus is '元数据提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

comment on column dm2_storage_object.dsometadataparseprocid is '元数据提取进程标识';

comment on column dm2_storage_object.dsotags is '标签';

comment on column dm2_storage_object.dsolastmodifytime is '记录最后刷新时间';

comment on column dm2_storage_object.dsometadataparsememo is '元数据提取说明';

comment on column dm2_storage_object.dsodetailparsememo is '明细提取说明';

comment on column dm2_storage_object.dsodetailparsestatus is '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

comment on column dm2_storage_object.dsodetailparseprocid is '明细提取标识';

comment on column dm2_storage_object.dsotagsparsememo is '明细提取说明';

comment on column dm2_storage_object.dsotagsparsestatus is '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

comment on column dm2_storage_object.dsotagsparseprocid is '明细提取标识';

comment on column dm2_storage_object.dsoalphacode is '拼音';

comment on column dm2_storage_object.dsoaliasname is '别名';

comment on column dm2_storage_object.dsoparentobjid is '父对象标识';

comment on column dm2_storage_object.dsometadataxml_bus is '业务元数据XML';

comment on column dm2_storage_object.dsometadatatext_bus is '业务元数据文本';

comment on column dm2_storage_object.dsometadatatype_bus is '元数据类型;0-txt;1-json;2-xml';

comment on column dm2_storage_object.dsometadata_bus_parsememo is '业务元数据收割备注';

comment on column dm2_storage_object.dso_volumn_now is '存储-容积-当前值';

comment on column dm2_storage_object.dso_add_time is '入库时间';

comment on column dm2_storage_object.dso_time is '时间';

comment on column dm2_storage_object.dso_geo_bb_native is '对象-原始-外包框';

comment on column dm2_storage_object.dso_geo_native is '对象-原始-外边框';

comment on column dm2_storage_object.dso_center_native is '对象-原始-中心点';

comment on column dm2_storage_object.dso_geo_bb_wgs84 is '对象-WGS84-外包框';

comment on column dm2_storage_object.dso_geo_wgs84 is '对象-WGS84-外边框';

comment on column dm2_storage_object.dso_center_wgs84 is '对象-WGS84-中心点';

comment on column dm2_storage_object.dso_quality is '质检详情';

comment on column dm2_storage_object.dso_time_parsermemo is '时间解析说明';

comment on column dm2_storage_object.dso_spatial_parsermemo is '空间解析说明';

comment on column dm2_storage_object.dso_view_parsermemo is '可视化解析说明';

comment on column dm2_storage_object.dso_browser is '快视图文件地址';

comment on column dm2_storage_object.dso_thumb is '拇指图文件地址';

comment on column dm2_storage_object.dso_metadata_result is '元数据解析结果';

comment on column dm2_storage_object.dso_metadata_bus_result is '业务元数据解析结果';

comment on column dm2_storage_object.dso_spatial_result is '空间元数据解析结果';

comment on column dm2_storage_object.dso_view_result is '可视化元数据解析结果';

comment on column dm2_storage_object.dso_time_result is '时间元数据解析结果';

comment on column dm2_storage_object.dso_prj_proj4 is '坐标投影-proj4';

comment on column dm2_storage_object.dso_prj_coordinate is '坐标投影-坐标系';

comment on column dm2_storage_object.dso_prj_degree is '坐标投影-度';

comment on column dm2_storage_object.dso_prj_zone is '坐标投影-带';

comment on column dm2_storage_object.dso_prj_source is '坐标投影-信息来源;1-实体;2-业务元数据;9-人工指定';

comment on column dm2_storage_object.dso_prj_wkt is '坐标投影-wkt';

comment on column dm2_storage_object.dso_prj_project is '坐标投影-投影';

comment on column dm2_storage_object.dso_da_status is '发布规则审核-状态';

comment on column dm2_storage_object.dso_da_proc_id is '发布规则审核-并行标识';

comment on column dm2_storage_object.dso_da_result is '发布规则审核-结果';

alter table dm2_storage_object owner to postgres;

create index idx_dm2_storage_object_id
	on dm2_storage_object (dsoid);

create index idx_dm2_storage_object_json
	on dm2_storage_object (dsometadatajson);

create index idx_dm2_storage_object_json_bus
	on dm2_storage_object (dsometadatajson_bus);

create index idx_dm2_storage_object_objecttype
	on dm2_storage_object (dsoobjecttype);

create index idx_dm2_storage_object_tag
	on dm2_storage_object (dsotags);

create table dm2_storage_object_def
(
	dsodid varchar(100) not null
		constraint dm2_storage_object_def_pkey
			primary key,
	dsodname varchar(100) not null,
	dsodtitle varchar(1000) not null,

	dsodtype varchar(100),
	dsodtype_title varchar(300),

	dsodcode varchar(100),
	dsocatalog integer
);

comment on table dm2_storage_object_def is '数管-存储目录-对象-定义';

comment on column dm2_storage_object_def.dsodid is '对象标识';

comment on column dm2_storage_object_def.dsodname is '对象名称';

comment on column dm2_storage_object_def.dsodtitle is '对象标题';

comment on column dm2_storage_object_def.dsodtype is '大类';

comment on column dm2_storage_object_def.dsodtype_title is '大类标题';

comment on column dm2_storage_object_def.dsodcode is '类型编码';

comment on column dm2_storage_object_def.dsocatalog is '数据类别：0-普通 1-业务单体 2-业务数据集';

alter table dm2_storage_object_def owner to postgres;

create index idx_dm2_storage_object_def_id
	on dm2_storage_object_def (dsodid);

create index idx_dm2_storage_object_def_name
	on dm2_storage_object_def (dsodname);

create index idx_dm2_storage_object_def_type
	on dm2_storage_object_def (dsodtype);

/*
    2020-10-20
    . 增加专用序列, 创建每日的数据批次
*/

create sequence sys_seq_autoinc increment by 1 minvalue 1 no maxvalue start with 1;
create sequence sys_seq_date_autoinc increment by 1 minvalue 1 no maxvalue start with 1;

delete from ro_global_config where gcfgid = 10001;
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo)
 values (10001, 'sys_seq_date_autoinc', '日期自增序列最后记录', current_date::text, null);



/*
    2020-10-22
    . 开始设计数据入库的具体设计
        . 在dm2_storage表中, 增加不同类型的存储
            . dstType varchar
                . core: 核心存储
                . inbound: 入库存储
        . 在dm2_storage_directory表中, 增加其他属性字段
            . dsdOtherOption jsonb
                . 用于存储其他不重要的, 或者待扩展的信息
                    . instore.allow: int(-1:true;0:false): 是否允许提交入库
        . 在dm2_storage_file表中, 增加其他属性字段
            . dsfOtherOption jsonb
                . 用于存储其他不重要的, 或者待扩展的信息
        . 在dm2_storage_object表中, 增加其他属性字段
            . dsoOtherOption jsonb
                . 用于存储其他不重要的, 或者待扩展的信息
                    . instore.allow: int(-1:true;0:false): 是否允许提交入库
*/
alter table dm2_storage add column dstType varchar(20) default 'core';
comment on column dm2_storage.dstType is '存储类型';

alter table dm2_storage_directory add column dsdOtherOption jsonb;
comment on column dm2_storage_directory.dsdOtherOption is '其他';

alter table dm2_storage_file add column dsfOtherOption jsonb;
comment on column dm2_storage_file.dsfOtherOption is '其他';

alter table dm2_storage_object add column dsoOtherOption jsonb;
comment on column dm2_storage_object.dsoOtherOption is '其他';

alter table dm2_storage_object add column dso_quality_summary jsonb;
comment on column dm2_storage_object.dso_quality_summary is '质检概况';

/*
    2020-10-23
    开始数据入库的数据表设计
    . dm2_storage_inbound
        . 数据入库主表
    . dm2_storage_inbound_log
        . 数据入库日志
*/
drop table dm2_storage_inbound cascade ;

create table dm2_storage_inbound
(
    dsiid         serial       not null
        constraint dm2_storage_inbound_pk primary key,
    dsistorageid  varchar(100) not null,
    dsidirectory  varchar(2000),
    dsibatchno    varchar(20),
    dsiOtherOption jsonb,
    dsiaddtime    timestamp(6) default now(),
    dsistatus     integer default 0,
    dsiProcTime   timestamp(6) default now(),
    dsiProcID   varchar(100),
    dsiProcMemo text,
    dsiMemo     text
);

comment on table dm2_storage_inbound is '数管-入库';

comment on column dm2_storage_inbound.dsiid is '标识';
comment on column dm2_storage_inbound.dsistorageid is '存储标识';
comment on column dm2_storage_inbound.dsidirectory is '目录名称';
comment on column dm2_storage_inbound.dsibatchno is '批次编号';
comment on column dm2_storage_inbound.dsiOtherOption is '其他属性';
comment on column dm2_storage_inbound.dsistatus is '处理状态';
comment on column dm2_storage_inbound.dsiProcTime is '最小处理时间';
comment on column dm2_storage_inbound.dsiProcID is '处理标识';
comment on column dm2_storage_inbound.dsiProcMemo is '处理结果';
comment on column dm2_storage_inbound.dsiMemo is '备注';
alter table dm2_storage_inbound owner to postgres;

drop table dm2_storage_inbound_log cascade ;

create table dm2_storage_inbound_log
(
    dsilid         serial       not null
        constraint dm2_storage_inbound_log_pk primary key,
    dsilownerid int not null,
    dsildirectory  varchar(2000),
    dsilfilename  varchar(2000),
    dsilobjectname  varchar(100),
    dsilobjecttype  varchar(100),
    dsiladdtime    timestamp(6) default now(),
    dsilinbound     integer default 0
);

comment on table dm2_storage_inbound_log is '数管-入库-日志';

comment on column dm2_storage_inbound_log.dsilid is '标识';
comment on column dm2_storage_inbound_log.dsilownerid is '所属入库记录标识';
comment on column dm2_storage_inbound_log.dsildirectory is '目录';
comment on column dm2_storage_inbound_log.dsilfilename is '文件名';
comment on column dm2_storage_inbound_log.dsilobjectname is '对象名';
comment on column dm2_storage_inbound_log.dsilobjecttype is '对象类型';
comment on column dm2_storage_inbound_log.dsiladdtime is '添加时间';
comment on column dm2_storage_inbound_log.dsilinbound is '是否允许入库';
alter table dm2_storage_inbound_log owner to postgres;



/*
    2020-10-28
    . 取消dm2_storage_obj_detail中的两个字段
*/

alter table dm2_storage_obj_detail drop column dodstorageid ;
alter table dm2_storage_obj_detail drop column dodfilerelationname ;

drop index if exists idx_dm2_storage_object_json CASCADE;
create index if not exists idx_dm2_storage_object_json
	on dm2_storage_object USING gin (dsometadatajson);

drop index if exists idx_dm2_storage_object_json_bus CASCADE;
create index if not exists idx_dm2_storage_object_json_bus
	on dm2_storage_object USING gin (dsometadatajson_bus);

drop index if exists idx_dm2_storage_object_time CASCADE;
create index if not exists idx_dm2_storage_object_time on dm2_storage_object USING gin (dso_time);

drop index if exists idx_dm2_storage_object_da_result CASCADE;
create index if not exists idx_dm2_storage_object_da_result on dm2_storage_object USING gin (dso_da_result);

drop index if exists idx_dm2_storage_object_option CASCADE;
create index if not exists idx_dm2_storage_object_option on dm2_storage_object USING gin (dsoOtherOption);

alter table dm2_storage_object add column dso_da_proc_memo text;
comment on column dm2_storage_object.dso_da_proc_memo is '发布规则审核-备注';

/*
    2020-10-29
    . 发现由于成果数据的坐标系不统一, 原生的成果数据外边框和中心点坐标等内容, 均无法直接存储到geometry字段中, 只能按照text类型存储了
*/
alter table dm2_storage_object drop column dso_center_native ;
alter table dm2_storage_object drop column dso_geo_native ;
alter table dm2_storage_object drop column dso_geo_bb_native ;

alter table dm2_storage_object add column dso_center_native text;
alter table dm2_storage_object add column dso_geo_native text;
alter table dm2_storage_object add column dso_geo_bb_native text;
comment on column dm2_storage_object.dso_geo_bb_native is '对象-原始-外包框';
comment on column dm2_storage_object.dso_geo_native is '对象-原始-外边框';
comment on column dm2_storage_object.dso_center_native is '对象-原始-中心点';

/*
    2020-10-29
    . 考虑到和第三方系统同步数据的时机, 决定从inbound表进行触发, 字段前缀为dsi_na_(notify_app)
    . 由于入库后, 目录名称会发生变化, 这里增加记录原待入库目录的标识, 便于数据同步调度查询入库后的批次数据
*/
alter table dm2_storage_inbound add column dsi_na_status int default 1;
alter table dm2_storage_inbound add column dsi_na_proc_id varchar(100);
alter table dm2_storage_inbound add column dsi_na_proc_memo text;
comment on column dm2_storage_inbound.dsi_na_status is '入库结束-通知应用-状态';
comment on column dm2_storage_inbound.dsi_na_proc_id is '入库结束-通知应用-并行';
comment on column dm2_storage_inbound.dsi_na_proc_memo is '入库结束-通知应用-备注';

alter table dm2_storage_inbound add column dsiDirectoryId varchar(100);
comment on column dm2_storage_inbound.dsiDirectoryId is '入库目录标识';

/*
    2020-10-30
    . 为核心数据表, 增加部分业务字段
        . 用户信息
    . 考虑到每一个对象要同步到第三方系统, 增加数据对象与第三方系统的同步记录表
*/

alter table dm2_storage add column dstUserId varchar(100);
comment on column dm2_storage.dstUserId is '数管-存储-用户';

alter table dm2_storage_directory add column dsdUserId varchar(100);
comment on column dm2_storage_directory.dsdUserId is '数管-存储-目录-用户';

alter table dm2_storage_file add column dsfUserId varchar(100);
comment on column dm2_storage_file.dsfUserId is '数管-存储-文件-用户';

alter table dm2_storage_inbound add column dsiUserId varchar(100);
comment on column dm2_storage_inbound.dsiUserId is '数管-存储-入库-用户';

/*
    2020-11-02
    . 扩展object_def表, 支持可视化展示
        . 增加数据类型的分组
    . 扩展object表, 支持对重复对象的检查结果分析
*/
alter table dm2_storage_object_def add column dsodgroupname varchar(100);
comment on column dm2_storage_object_def.dsodgroupname is '数管-定义-分组名称';
alter table dm2_storage_object_def add column dsodgrouptitle varchar(100);
comment on column dm2_storage_object_def.dsodgrouptitle is '数管-定义-分组标题';

alter table dm2_storage_object add column dsocopystat jsonb;
comment on column dm2_storage_object.dsocopystat is '数管-对象-副本-统计';

drop index if exists idx_dm2_storage_object_copystat CASCADE;
create index if not exists idx_dm2_storage_object_copystat on dm2_storage_object USING gin (dsocopystat);

alter table dm2_storage_directory add column dsdscanmemo text;
comment on column dm2_storage_directory.dsdscanmemo is '数管-目录-识别备注';

alter table dm2_storage_file add column dsfscanmemo text;
comment on column dm2_storage_file.dsfscanmemo is '数管-文件-识别备注';


/*
    2020-11-09
    . 扩展dm2_storage, 考虑支持linux和windows应用的协同应用
*/
alter table dm2_storage add column dstOwnerPath varchar(4000);
comment on column dm2_storage.dstOwnerPath is '数管-存储-私有路径';

alter table dm2_storage add column dstScanMemo text;
comment on column dm2_storage.dstScanMemo is '数管-存储-扫描-结果';


/*
    补充dm2_storage_obj_na表设计
*/

drop table if exists dm2_storage_obj_na;

create table if not exists dm2_storage_obj_na
(
	dsonid serial not null
		constraint dm2_storage_obj_na_pk
			primary key,
	dson_object_id varchar(100),
	dson_app_id varchar(200),
	dson_notify_status integer default 1,
	dson_notify_proc_id varchar(100),
	dson_notify_proc_memo text,
	dson_addtime timestamp(6) default now()
);

comment on table dm2_storage_obj_na is '数管-对象-同步';

comment on column dm2_storage_obj_na.dsonid is '标识';

comment on column dm2_storage_obj_na.dson_object_id is '对象标识';

comment on column dm2_storage_obj_na.dson_app_id is '应用标识';

comment on column dm2_storage_obj_na.dson_notify_status is '通知状态';

comment on column dm2_storage_obj_na.dson_notify_proc_id is '并行标识';

comment on column dm2_storage_obj_na.dson_notify_proc_memo is '通知结果';

comment on column dm2_storage_obj_na.dson_addtime is '添加时间';

alter table dm2_storage_obj_na owner to postgres;

/*
    2020-11-13
    . 为解决对象的更新, 对object表进行扩展
*/

alter table dm2_storage_object add column dso_obj_lastmodifytime timestamp(6);
comment on column dm2_storage_object.dso_obj_lastmodifytime is '数管-对象-最后修改时间';

/*
    2020-11-14
    . 调整和优化dm2_storage_object_def结构
*/

drop table if exists dm2_storage_object_def;

create table if not exists dm2_storage_object_def
(
	dsodid varchar(100) not null
		constraint dm2_storage_object_def_pkey
			primary key,
    dsodname varchar(100) not null,
	dsodtitle varchar(1000) not null,
	dsodcode varchar(100),
	dsodtype varchar(100),
	dsodtype_title varchar(300),
	dsodgroupname varchar(100),
	dsodgrouptitle varchar(100),
	dsodcatalog varchar(100)
);

comment on table dm2_storage_object_def is '数管-存储目录-对象-定义';

comment on column dm2_storage_object_def.dsodid is '对象标识';

comment on column dm2_storage_object_def.dsodname is '对象名称';

comment on column dm2_storage_object_def.dsodtitle is '对象标题';

comment on column dm2_storage_object_def.dsodtype is '大类';

comment on column dm2_storage_object_def.dsodtype_title is '大类标题';

comment on column dm2_storage_object_def.dsodcode is '类型编码';

comment on column dm2_storage_object_def.dsodgroupname is '数管-定义-分组名称';

comment on column dm2_storage_object_def.dsodgrouptitle is '数管-定义-分组标题';

comment on column dm2_storage_object_def.dsodcatalog is '数据类别';

alter table dm2_storage_object_def owner to postgres;

create index idx_dm2_storage_object_def_id
	on dm2_storage_object_def (dsodid);

create index idx_dm2_storage_object_def_name
	on dm2_storage_object_def (dsodname);

create index idx_dm2_storage_object_def_type
	on dm2_storage_object_def (dsodtype);


