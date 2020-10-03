dm_index
	dm_index_ys   -- 原始数据
	dm_index_Spatial  -- 支持空间范围的编目数据表
		dm_index_ndi  -- 分景数据（分景标准+增值）   dm_index_ndi
		dm_index_zz   -- 增值数据（镶嵌后）   dm_index
dm_index_file   -- 编目和文件之间的关系   dm_index_ndi_ex


------------------------dm_Index 根数据

drop TABLE public.dm_index;
CREATE TABLE public.dm_index
(
    diid          varchar(50) NOT NULL,
    dixmlmeta     xml,
    dixmlversion  varchar(50),
    dizipfilelist text,
    diClass       varchar(50) not null,
    ditype        varchar(50),
    didate        timestamp,
    diimporttime  timestamp,
    didatasource  varchar(200),
    CONSTRAINT "dm_index_PK" PRIMARY KEY ("diid")
);

COMMENT ON COLUMN public.dm_index.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index.dixmlmeta IS 'XML元数据';
COMMENT ON COLUMN public.dm_index.dixmlversion IS 'XML版本号';
COMMENT ON COLUMN public.dm_index.dizipfilelist IS '数据包文件列表';
COMMENT ON COLUMN public.dm_index.diClass IS '大类;ys-原始;ndi-分景;zz-增值';
COMMENT ON COLUMN public.dm_index.ditype IS '数据类型';
COMMENT ON COLUMN public.dm_index.diimporttime IS '入库时间';
COMMENT ON COLUMN public.dm_index.didatasource IS '数据来源';

drop Index idx_dm_index_id;
Create Index idx_dm_index_id on dm_index (diid);

drop Index idx_dm_index_Class;
Create Index idx_dm_index_Class on dm_index (diClass);

drop Index idx_dm_index_Class_Type;
Create Index idx_dm_index_Class_Type on dm_index (diClass, diType);


------------------------dm_Index_Spatial 支持空间范围的编目数据表
drop TABLE public.dm_index_Spatial;

CREATE TABLE public.dm_index_Spatial
(
    dixmlfile  varchar(1000),
    digeometry geometry,
    diserverid varchar(50),
    CHECK ( diClass = 'ys' or diClass = 'zz')
) INHERITS (dm_index);

COMMENT ON COLUMN public.dm_index_Spatial.dixmlfile IS '元数据文件路径';
COMMENT ON COLUMN public.dm_index_Spatial.digeometry IS '编目空间范围';
COMMENT ON COLUMN public.dm_index_Spatial.diserverid IS '编目服务器标示';

drop Index idx_dm_index_Spatial_Class;
Create Index idx_dm_index_Spatial_Class on dm_index_Spatial (diClass);


------------------------dm_Index_ys 原始数据
drop TABLE public.dm_index_ys;

CREATE TABLE public.dm_index_ys
(
    CHECK ( diClass = 'ys')
) INHERITS (dm_index);

drop Index idx_dm_index_ys_Class;
Create Index idx_dm_index_ys_Class on dm_index_ys (diClass);


------------------------dm_Index_zz 增值数据
drop TABLE public.dm_index_zz;

CREATE TABLE public.dm_index_zz
(
    dibrowserimg   varchar(1000),
    ditransformimg varchar(1000),
    dithumbimg     varchar(1000),
    dicoverageimg  varchar(1000),
    CHECK ( diClass = 'zz')
) INHERITS (dm_index_Spatial);

COMMENT ON COLUMN public.dm_index_zz.dibrowserimg IS '缩略图文件路径';
COMMENT ON COLUMN public.dm_index_zz.ditransformimg IS '斜视图文件路径';
COMMENT ON COLUMN public.dm_index_zz.dithumbimg IS '拇指图文件路径';
COMMENT ON COLUMN public.dm_index_zz.dicoverageimg IS '覆盖图文本路径';

drop Index idx_dm_index_zz_Class;
Create Index idx_dm_index_zz_Class on dm_index_zz (diClass);

------------------------dm_Index_ndi 分景数据
drop TABLE public.dm_index_ndi;

CREATE TABLE public.dm_index_ndi
(
    dipanbrowserimg   varchar(1000),
    dipantransformimg varchar(1000),
    dipanthumbimg     varchar(1000),
    dipantifimg       varchar(1000),
    dipankmzimg       varchar(1000),
    dimuxbrowserimg   varchar(1000),
    dimuxtransformimg varchar(1000),
    dimuxthumbimg     varchar(1000),
    dimuxtifimg       varchar(1000),
    dimuxkmzimg       varchar(1000),
    CHECK ( diClass = 'ndi')
) INHERITS (dm_index_Spatial);

COMMENT ON COLUMN public.dm_index_ndi.dixmlfile IS '元数据文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dipanbrowserimg IS '全色缩略图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dipantransformimg IS '全色斜视图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dipanthumbimg IS '全色拇指图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dipantifimg IS 'GeoTiff格式全色浏览图';
COMMENT ON COLUMN public.dm_index_ndi.dipankmzimg IS 'KMZ格式全色浏览图';
COMMENT ON COLUMN public.dm_index_ndi.dimuxbrowserimg IS '多光谱缩略图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dimuxtransformimg IS '多光谱斜视图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dimuxthumbimg IS '多光谱拇指图文件路径';
COMMENT ON COLUMN public.dm_index_ndi.dimuxtifimg IS 'GeoTiff格式多光谱浏览图';
COMMENT ON COLUMN public.dm_index_ndi.dimuxkmzimg IS 'KMZ格式多光谱浏览图';
COMMENT ON COLUMN public.dm_index_ndi.digeometry IS '编目空间范围';
COMMENT ON COLUMN public.dm_index_ndi.diserverid IS '编目服务器标示';
COMMENT ON COLUMN public.dm_index_ndi.linkid IS '链接标示';

drop Index idx_dm_index_ndi_Class;
Create Index idx_dm_index_ndi_Class on dm_index_ndi (diClass);

------------------------dm_index_ndi_ex NDI编目扩展信息表

drop TABLE public.dm_index_ndi_ex;

CREATE TABLE public.dm_index_ndi_ex
(
    diid         varchar(50)           NOT NULL,
    -- ndi产品分级的元数据描述
    productlevel character varying(50) NOT NULL,
    panmetafile  character varying(2000),
    msmetafile   character varying(2000),
    CONSTRAINT "dm_index_ndi_ex_PK" PRIMARY KEY (diid, productlevel)
);

COMMENT ON COLUMN public.dm_index_ndi_ex.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index_ndi_ex.productlevel IS '产品级别';
COMMENT ON COLUMN public.dm_index_ndi_ex.panmetafile IS '全色元数据文件';
COMMENT ON COLUMN public.dm_index_ndi_ex.msmetafile IS '多光谱元数据文件';

drop Index idx_dm_index_ndi_ex_id;
Create Index idx_dm_index_ndi_ex_id on dm_index_ndi_ex (diid);

------------------------dm_index_export 编目同步信息表

drop TABLE public.dm_index_export;

CREATE TABLE public.dm_index_export
(
    diid               varchar(50) NOT NULL,

    exportLAN          integer DEFAULT 1,
    exportLANTime      timestamptz,

    exportInternet     integer DEFAULT 1,
    exportInternetTime timestamptz,

    CONSTRAINT "dm_index_export_PK" PRIMARY KEY (diid)
);

COMMENT ON COLUMN public.dm_index_export.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index_export.exportLAN IS '是否导出到内网；1未导出，-1导出成功';
COMMENT ON COLUMN public.dm_index_export.exportLANTime IS '内网同步时间';
COMMENT ON COLUMN public.dm_index_export.exportInternet IS '是否导出到外网；1未导出，-1导出成功';
COMMENT ON COLUMN public.dm_index_export.exportInternetTime IS '外网同步时间';

drop Index idx_dm_index_export_id;
Create Index idx_dm_index_export_id on dm_index_export (diid);

------------------------dm_index_file 编目-文件关联表

DROP TABLE public.dm_index_file;

CREATE TABLE public.dm_index_file
(
    -- 编目与文件的关系
    fileid  character varying(50) NOT NULL,
    indexid character varying(50) NOT NULL,
    CONSTRAINT "dm_index_file_PK" PRIMARY KEY (fileid, indexid)
);

COMMENT ON COLUMN public.dm_index_file.fileid IS '文件标示';
COMMENT ON COLUMN public.dm_index_file.indexid IS '编目标示';

drop Index idx_dm_index_file_fileid;
Create Index idx_dm_index_file_fileid on dm_index_file (fileid);

drop Index idx_dm_index_file_indexid;
Create Index idx_dm_index_file_indexid on dm_index_file (indexid);

------------------------dm_index_catalog 编目定义表

DROP TABLE public.dm_index_catalog;

CREATE TABLE public.dm_index_catalog
(
    diccode          varchar(50)  NOT NULL,
    dictitle         varchar(100) NOT NULL,
    dictreecode      varchar(200) NOT NULL,
    dicisgroup       int4,
    dicenable        int4,
    dicsell          int4,
    dicptreecode     varchar(200),
    dicexportoption  text,
    dicarchiveoption text,
    dicrestoreoption text,
    dicclearoption   text,
    dicmemo          text,
    CONSTRAINT "dm_index_catalog_PK" PRIMARY KEY (diccode)
);

COMMENT ON COLUMN public.dm_index_catalog.diccode IS '类型编码';
COMMENT ON COLUMN public.dm_index_catalog.dictitle IS '类型标题';
COMMENT ON COLUMN public.dm_index_catalog.dictreecode IS '树编码';
COMMENT ON COLUMN public.dm_index_catalog.dicisgroup IS '是否组';
COMMENT ON COLUMN public.dm_index_catalog.dicenable IS '是否可用';
COMMENT ON COLUMN public.dm_index_catalog.dicsell IS '是否销售';
COMMENT ON COLUMN public.dm_index_catalog.dicptreecode IS '树节点父编码';
COMMENT ON COLUMN public.dm_index_catalog.dicexportoption IS '编目导出设置';
COMMENT ON COLUMN public.dm_index_catalog.dicarchiveoption IS '归档设置';
COMMENT ON COLUMN public.dm_index_catalog.dicrestoreoption IS '恢复设置';
COMMENT ON COLUMN public.dm_index_catalog.dicclearoption IS '清理设置';
COMMENT ON COLUMN public.dm_index_catalog.dicmemo IS '备注';


------------------------dm_dept_delivery 部门产品分发配置表


CREATE TABLE public.dm_dept_delivery
(
    ddid         character varying(200) NOT NULL, -- 部门ID
    ddtitle      character varying(200),          -- 部门标题
    ddlevel      integer,                         -- 部门默认申请级别，1普通，2紧急，3特急
    ddmountpath  character varying(2000),         -- 在Linux上数据回迁的mount根目录
    ddsourcepath character varying(2000),         -- Windows下的数据分发根目录
    CONSTRAINT dm_dept_delivery_pkey PRIMARY KEY (ddid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_dept_delivery
    OWNER TO postgres;
COMMENT ON COLUMN public.dm_dept_delivery.ddid IS '部门ID';
COMMENT ON COLUMN public.dm_dept_delivery.ddtitle IS '部门标题';
COMMENT ON COLUMN public.dm_dept_delivery.ddlevel IS '部门默认申请级别';
COMMENT ON COLUMN public.dm_dept_delivery.ddmountpath IS '在Linux上数据回迁的mount根目录';
COMMENT ON COLUMN public.dm_dept_delivery.ddsourcepath IS 'Windows下的数据分发根目录';


------------------------dm_index_catalog 产品定义表

CREATE TABLE public.dm_index_catalog
(
    diccode             character varying(50) NOT NULL, -- diccode
    dictitle            character varying(200),         -- dictitle
    dictreecode         character varying(1000),        -- dictreecode
    dicptreecode        character varying(1000),        -- dicptreecode
    dicisgroup          bigint,                         -- dicisgroup
    dicinstoremode      bigint,                         -- dicInstoreMode
    dicinstoremodelid   character varying(200),         -- dicInstoreModelID
    dicinstoreparams    text,                           -- dicInstoreParams
    dicallowexportlan   bigint,                         -- dicAllowExportLAN
    dicallowexportwan   bigint,                         -- dicAllowExportWAN
    dicallowarchive     bigint,                         -- dicAllowArchive
    dicarchiverootname  character varying(100),         -- dicarchiverootname
    dicarchiveusergroup character varying(1000),        -- dicarchiveusergroup
    dicarchivepath      character varying(2000),        -- dicarchivepath
    dicallowdelete      bigint,                         -- dicallowdelete
    dicdeletescheme     bigint,                         -- dicdeletescheme
    dicdeleteparams     text,                           -- dicdeleteparams
    dicmemo             text,                           -- dicmemo
    CONSTRAINT "dm_index_catalog_PK" PRIMARY KEY (diccode)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_catalog
    OWNER TO postgres;
COMMENT ON COLUMN public.dm_index_catalog.diccode IS '产品代码';
COMMENT ON COLUMN public.dm_index_catalog.dictitle IS '产品名称';
COMMENT ON COLUMN public.dm_index_catalog.dictreecode IS '产品编码';
COMMENT ON COLUMN public.dm_index_catalog.dicptreecode IS '产品父编码';
COMMENT ON COLUMN public.dm_index_catalog.dicisgroup IS '是否是分组';
COMMENT ON COLUMN public.dm_index_catalog.dicinstoremode IS '入库模式';
COMMENT ON COLUMN public.dm_index_catalog.dicinstoremodelid IS '入库模型标识';
COMMENT ON COLUMN public.dm_index_catalog.dicinstoreparams IS '入库参数';
COMMENT ON COLUMN public.dm_index_catalog.dicallowexportlan IS '是否同步至内网';
COMMENT ON COLUMN public.dm_index_catalog.dicallowexportwan IS '是否同步至外网';
COMMENT ON COLUMN public.dm_index_catalog.dicallowarchive IS '是否支持归档';
COMMENT ON COLUMN public.dm_index_catalog.dicarchiverootname IS '归档磁带库的名称';
COMMENT ON COLUMN public.dm_index_catalog.dicarchiveusergroup IS '归档磁带池的名称';
COMMENT ON COLUMN public.dm_index_catalog.dicarchivepath IS '归档路径';
COMMENT ON COLUMN public.dm_index_catalog.dicallowdelete IS '是否支持清理';
COMMENT ON COLUMN public.dm_index_catalog.dicdeletescheme IS '清理模式';
COMMENT ON COLUMN public.dm_index_catalog.dicdeleteparams IS '清理参数';
COMMENT ON COLUMN public.dm_index_catalog.dicmemo IS '备注';

drop Index idx_dm_index_catalog_diccode;
Create Index idx_dm_index_catalog_diccode on dm_index_catalog (diccode);


------------------------2015-09-09 dm_index_catalog 产品定义表
-- 加速sch_mission表针对Event的维护功能

CREATE INDEX smeventid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smeventid COLLATE pg_catalog."default");



------------------------2015-09-10  加速归档列表的检索功能

------------------------dm_archive_task 归档任务表 
CREATE INDEX fileid_idx_dm_archive_task ON dm_archive_task (fileid);

------------------------ro_file 实体文件表 
CREATE INDEX fid_idx_ro_file ON ro_file (fid);


------------------------磁带库数据库 确认产品入库成功的SQL
select requestinfo.RequestID
from STORAGEFILE
         left join requestinfo on requestinfo.StorageObjectId = STORAGEFILE.StorageObjectId
where STORAGEFILE.filename like '%GF1_PMS2_E118.0_N46.3_20150607_L1A0000851777%'
  and requestinfo.RequestStateId = 0


------------------------2015-09-19  扩展dm_index_spatial，支持普通的空间文件类型

ALTER TABLE dm_index_spatial
    DROP CONSTRAINT dm_index_spatial_diclass_check;
ALTER TABLE dm_index_spatial
    ADD CONSTRAINT dm_index_spatial_diclass_check CHECK (diclass::text = 'ndi'::text OR diclass::text = 'zz'::text OR
                                                         diclass::text = 'geo'::text);

ALTER TABLE dm_index
    ADD COLUMN dititle character varying(4000);
COMMENT ON COLUMN dm_index.dititle IS '产品标题';
update dm_index
set dititle = diid;

------------------------2015-09-19  增加部门空间文件数据表

CREATE TABLE public.dm_index_dept_geo
(
-- 继承 from table dm_index_spatial:  diid character varying(3000) NOT NULL,
-- 继承 from table dm_index_spatial:  dixmlmeta xml,
-- 继承 from table dm_index_spatial:  dixmlversion character varying(50),
-- 继承 from table dm_index_spatial:  dizipfilelist text,
-- 继承 from table dm_index_spatial:  diclass character varying(50) NOT NULL,
-- 继承 from table dm_index_spatial:  ditype character varying(50),
-- 继承 from table dm_index_spatial:  didate timestamp without time zone,
-- 继承 from table dm_index_spatial:  diimporttime timestamp without time zone,
-- 继承 from table dm_index_spatial:  didatasource character varying(200),
-- 继承 from table dm_index_spatial:  dixmlfile character varying(1000),
-- 继承 from table dm_index_spatial:  digeometry geometry,
-- 继承 from table dm_index_spatial:  diserverid character varying(50),
    dideptid character varying(100) NOT NULL,
    CONSTRAINT dm_index_dept_geo_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_dept_geo_diclass_check CHECK (diclass::text = 'geo'::text)
)
    INHERITS (public.dm_index_spatial)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_dept_geo
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_dept_geo
    IS '产品编目-部门文件-空间';

COMMENT ON COLUMN public.dm_index_dept_geo.dideptid IS '部门标识';

-- Index: public.idx_dm_index_dept_geo_class

-- DROP INDEX public.idx_dm_index_dept_geo_class;

CREATE INDEX idx_dm_index_dept_geo_class
    ON public.dm_index_dept_geo
        USING btree
        (diclass COLLATE pg_catalog."default");

CREATE INDEX idx_dm_index_dept_geo_dititle_dideptid
    ON public.dm_index_dept_geo (dideptid, dititle);

------------------------2015-09-19  增加部门非空间普通文件数据表
CREATE TABLE public.dm_index_dept_common
(
-- 继承 from table dm_index:  diid character varying(3000) NOT NULL,
-- 继承 from table dm_index:  dixmlmeta xml,
-- 继承 from table dm_index:  dixmlversion character varying(50),
-- 继承 from table dm_index:  dizipfilelist text,
-- 继承 from table dm_index:  diclass character varying(50) NOT NULL,
-- 继承 from table dm_index:  ditype character varying(50),
-- 继承 from table dm_index:  didate timestamp without time zone,
-- 继承 from table dm_index:  diimporttime timestamp without time zone,
-- 继承 from table dm_index:  didatasource character varying(200),
    dideptid character varying(100) NOT NULL,
    CONSTRAINT dm_index_dept_common_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_dept_common_diclass_check CHECK (diclass::text = 'common'::text)
)
    INHERITS (public.dm_index)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_dept_common
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_dept_common
    IS '产品编目-文件-普通';
COMMENT ON COLUMN public.dm_index_dept_common.dideptid IS '部门标识';


-- Index: public.idx_dm_index_dept_common_class

-- DROP INDEX public.idx_dm_index_dept_common_class;

CREATE INDEX idx_dm_index_dept_common_class
    ON public.dm_index_dept_common
        USING btree
        (diclass COLLATE pg_catalog."default");

CREATE INDEX idx_dm_index_dept_common_dititle_dideptid
    ON public.dm_index_dept_common (dideptid, dititle);

------------------------2015-09-19  整理各个数据表的作用

COMMENT ON TABLE public.dm_index_catalog IS '产品编目定义';

COMMENT ON TABLE public.dm_index IS '产品编目';
COMMENT ON TABLE public.dm_index_spatial IS '产品编目-空间相关';
COMMENT ON TABLE public.dm_index_dept_geo IS '产品编目-部门文件-空间';
COMMENT ON TABLE public.dm_index_ndi IS '产品编目-标准产品';
COMMENT ON TABLE public.dm_index_ndi_ex IS '产品编目-标准产品-分级扩展信息';
COMMENT ON TABLE public.dm_index_zz IS '产品编目-增值产品';
COMMENT ON TABLE public.dm_index_ys IS '产品编目-原始数据';
COMMENT ON TABLE public.dm_index_dept_common IS '产品编目-部门文件-普通';
COMMENT ON TABLE public.dm_index_export IS '产品编目-同步记录';
COMMENT ON TABLE public.dm_index_file IS '产品编目-实体文件';

COMMENT ON TABLE public.dm_order IS '产品分发-单据';
COMMENT ON TABLE public.dm_order_delivery IS '产品分发-交付';

COMMENT ON TABLE public.dm_archive_task IS '产品归档-任务';
COMMENT ON TABLE public.dm_archive_object IS '产品归档-结果';
COMMENT ON TABLE public.dm_archive_clear IS '产品归档-清理';

COMMENT ON TABLE public.dm_plan_task IS '产品回迁-任务';
COMMENT ON TABLE public.dm_restore_task IS '产品回迁-结果';

COMMENT ON TABLE public.dm_task_log IS '产品处理-日志';


----------------------2015-09-21 dm_index_catalog 扩展支持编目同步的业务
ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicexportlanbusid character varying(200);
ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicexportwanbusid character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dicexportlanbusid IS '内网编目同步流程';
COMMENT ON COLUMN public.dm_index_catalog.dicexportwanbusid IS '互联网编目同步流程';

--需要更新系统的元数据！！


-- 2015-09-22 根据日历，统计最近一个月的归档和清理的统计数据

select calendar.gcdate                          as 日期
     , handinstore.handinstorecount             as 入库产品数
     , stat.archivecount                        as 归档产品数
     , success.successcount                     as 归档成功产品数
     , stat.archivecount - success.successcount as 归档失败产品数
     , clear.clearcount                         as 清理产品数
from (
         select ro_global_calendar.gcdate
         from ro_global_calendar
         where ro_global_calendar.gcdate between current_date - 30 and current_date
     ) calendar
         left join
     (
         select diimporttime::date as handinstoredate, count(*) as handinstorecount
         from dm_index
         group by diimporttime::date
     ) handinstore on calendar.gcdate = handinstore.handinstoredate

         left join
     (
         select createtime::date as archivedate, count(*) as archivecount
         from dm_archive_task
         group by createtime::date
     ) stat on calendar.gcdate = stat.archivedate
         left join
     (
         select createtime::date as archivedate, count(*) as successcount
         from dm_archive_task
         where taskstatus = -1
         group by createtime::date
     ) success on calendar.gcdate = success.archivedate
         left join
     (
         select cleartime::date as cleardate, count(*) as clearcount
         from dm_archive_clear
         group by cleartime::date
     ) clear on calendar.gcdate = clear.cleardate
order by calendar.gcdate desc


-- 2015-09-22 根据产品定义，统计各类产品的在线、近线存储情况
select dm_index_catalog.diccode                                  as 产品代码
     , dm_index_catalog.dictitle                                 as 产品名称
     , coalesce(ro_file_stat.stat_size_g, 0)                     as 产品总量
     , coalesce(ro_file_stat.stat_count, 0)                      as 产品总数
     , coalesce((ro_file_stat.stat_size_g - coalesce(ro_file_near_store.stat_size_g, 0) -
                 coalesce(ro_file_out_store.stat_size_g, 0)), 0) as 在线存储量
     , coalesce((ro_file_stat.stat_count - coalesce(ro_file_near_store.stat_count, 0) -
                 coalesce(ro_file_out_store.stat_count, 0)), 0)  as 在线数
     , coalesce(ro_file_near_store.stat_size_g, 0)               as 近线存储量
     , coalesce(ro_file_near_store.stat_count, 0)                as 近线数
     , coalesce(ro_file_out_store.stat_size_g, 0)                as 离线存储量
     , coalesce(ro_file_out_store.stat_count, 0)                 as 离线数
from dm_index_catalog
         left join
     (
         select fcatalog, count(*) as stat_count, round(sum(fsize) / 1024 / 1024 / 1024) as stat_size_g
         from ro_file
         group by fcatalog
     ) ro_file_stat on ro_file_stat.fcatalog = dm_index_catalog.diccode
         left join
     (
         select ro_file.fcatalog, count(*) as stat_count, round(sum(ro_file.fsize) / 1024 / 1024 / 1024) as stat_size_g
         from ro_file,
              dm_archive_object
         where ro_file.fid = dm_archive_object.fileid
           and dm_archive_object.filestatus = 3 -- near_store
         group by ro_file.fcatalog
     ) ro_file_near_store on ro_file_near_store.fcatalog = dm_index_catalog.diccode
         left join
     (
         select ro_file.fcatalog, count(*) as stat_count, round(sum(ro_file.fsize) / 1024 / 1024 / 1024) as stat_size_g
         from ro_file,
              dm_archive_object
         where ro_file.fid = dm_archive_object.fileid
           and dm_archive_object.filestatus = 2 -- outstore
         group by ro_file.fcatalog
     ) ro_file_out_store on ro_file_out_store.fcatalog = dm_index_catalog.diccode

order by dm_index_catalog.dictreecode


----------------------------2015-09-22 扩展产品定义表，加入产品大类
ALTER TABLE dm_index_catalog
    ADD COLUMN dicclass character varying(100);
COMMENT ON COLUMN dm_index_catalog.dicclass IS '产品大类';

----------------------------2015-09-23 扩展任务表，加入最后创建时间

ALTER TABLE public.sch_mission
    ADD COLUMN smcreatetime timestamp with time zone DEFAULT now();

----------------------------2015-09-23 创建编目同步控制表dm_index_sync，废弃dm_index_expert

CREATE TABLE public.dm_index_sync
(
    diid        character varying(3000) NOT NULL, -- 编目标示
    ditype      character varying(200)  NOT NULL, -- 编目类型
    synclan     integer DEFAULT 1,                -- 是否导出到内网；1未导出，-1导出成功
    synclantime timestamp with time zone,         -- 内网同步时间
    synclanflag character varying(200),           -- 内网同步标记
    syncwan     integer DEFAULT 1,                -- 是否导出到外网；1未导出，-1导出成功
    syncwantime timestamp with time zone,         -- 外网同步时间
    syncwanflag character varying(200),           -- 外网同步标记
    CONSTRAINT "dm_index_sync_PK" PRIMARY KEY (diid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_sync
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_sync
    IS '产品编目-同步记录';
COMMENT ON COLUMN public.dm_index_sync.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index_sync.ditype IS '编目类型';
COMMENT ON COLUMN public.dm_index_sync.synclan IS '是否导出到内网；1未导出，-1导出成功';
COMMENT ON COLUMN public.dm_index_sync.synclantime IS '内网同步时间';
COMMENT ON COLUMN public.dm_index_sync.synclanflag IS '内网同步标记';
COMMENT ON COLUMN public.dm_index_sync.syncwan IS '是否导出到外网；1未导出，-1导出成功';
COMMENT ON COLUMN public.dm_index_sync.syncwantime IS '外网同步时间';
COMMENT ON COLUMN public.dm_index_sync.syncwanflag IS '外网同步标记';


-- Index: public.idx_dm_index_sync_id

-- DROP INDEX public.idx_dm_index_sync_id;

CREATE INDEX idx_dm_index_sync_id
    ON public.dm_index_sync
        USING btree
        (diid COLLATE pg_catalog."default");

-- Index: public.idx_dm_index_sync_type

-- DROP INDEX public.idx_dm_index_sync_type;

CREATE INDEX idx_dm_index_sync_type
    ON public.dm_index_sync
        USING btree
        (ditype COLLATE pg_catalog."default");

-- Index: public.idx_dm_index_sync_type_synclanflag

-- DROP INDEX public.idx_dm_index_sync_type_synclanflag;

CREATE INDEX idx_dm_index_sync_type_synclanflag
    ON public.dm_index_sync
        USING btree
        (ditype COLLATE pg_catalog."default", synclanflag COLLATE pg_catalog."default");

-- Index: public.idx_dm_index_sync_type_syncwanflag

-- DROP INDEX public.idx_dm_index_sync_type_syncwanflag;

CREATE INDEX idx_dm_index_sync_type_syncwanflag
    ON public.dm_index_sync
        USING btree
        (ditype COLLATE pg_catalog."default", syncwanflag COLLATE pg_catalog."default");


----------------------------2015-09-23 监控记录表，加入最后创建时间

ALTER TABLE public.ro_datacenter_watch_cpu
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();

ALTER TABLE public.ro_datacenter_watch_disk
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();

ALTER TABLE public.ro_datacenter_watch_login
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();

ALTER TABLE public.ro_datacenter_watch_memory
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();

ALTER TABLE public.ro_datacenter_watch_process
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();

ALTER TABLE public.ro_datacenter_watch_system
    ADD COLUMN dccreatetime timestamp with time zone DEFAULT now();


----------------------------2015-11-25 编目同步日志记录表
DROP TABLE public.log_index_sync;

CREATE TABLE public.log_index_sync
(
    lisid           character varying(100) NOT NULL, -- 同步标示
    listitle        character varying(200) NOT NULL, -- 同步标题
    listype         integer DEFAULT 1,               -- 同步类型；1-内网；2外网
    lisindextype    character varying(100) NOT NULL, -- 同步产品编目标示
    lissuccess      integer DEFAULT 0,               -- 同步是否成功;0-否;-1-是
    lisindexcount   integer DEFAULT 0,               -- 同步产品编目个数
    lissuccesscount integer DEFAULT 0,               -- 成功同步产品编目个数
    lisstarttime    timestamp with time zone,        -- 同步开始时间
    lisendtime      timestamp with time zone,        -- 同步结束时间
    lismemo         text,                            -- 同步备注
    CONSTRAINT "log_index_sync_PK" PRIMARY KEY (lisid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.log_index_sync
    OWNER TO postgres;
COMMENT ON TABLE public.log_index_sync IS '日志-产品编目-同步记录';

COMMENT ON COLUMN public.log_index_sync.lisid IS '同步标示';
COMMENT ON COLUMN public.log_index_sync.listitle IS '同步标题';
COMMENT ON COLUMN public.log_index_sync.listype IS '同步类型；1-内网；2外网';
COMMENT ON COLUMN public.log_index_sync.lisindextype IS '同步产品编目标示';
COMMENT ON COLUMN public.log_index_sync.lissuccess IS '同步是否成功;0-否;-1-是';
COMMENT ON COLUMN public.log_index_sync.lisindexcount IS '同步产品编目个数';
COMMENT ON COLUMN public.log_index_sync.lissuccesscount IS '成功同步产品编目个数';
COMMENT ON COLUMN public.log_index_sync.lisstarttime IS '同步开始时间';
COMMENT ON COLUMN public.log_index_sync.lisendtime IS '同步结束时间';
COMMENT ON COLUMN public.log_index_sync.lismemo IS '同步备注';


----------------------------2015-11-26 将编目表中以前入库的，版本为空的记录进行自动初始化
update dm_index
set dixmlversion = '1.0'
where dixmlversion is null;

----------------------------2015-11-26 处理BJ1编目数据中数据生产日期错误的问题

update dm_index
set dixmlversion = '2.0'
where diclass = 'ndi'
  and ditype = 'BJ1_L0'
  and didate > '2013-01-01';

update dm_index
set didate = (substr(diid, 1, 4) || '-' || substr(diid, 5, 2) || '-' || substr(diid, 7, 2))::text::timestamp
where diclass = 'ndi'
  and ditype = 'BJ1_L0'
  and didate > '2013-01-01';

----------------------------2015-11-26 处理SJ9A编目数据中数据生产日期为空的问题

update dm_index_ndi
set didate = (substr(diid, 6, 4) || '-' || substr(diid, 10, 2) || '-' || substr(diid, 12, 2))::text::TIMESTAMP
where ditype = 'SJ9_L0';



--*****************************************************************************************2015-12-2 计划修改


-- Table: public.dm_order

-- DROP TABLE public.dm_order;

CREATE TABLE public.dm_order
(
    -- 必填项
    orderid         character varying(200) NOT NULL, -- 订单ID，UUID
    deptid          character varying(100),          -- 部门ID，重要，关联着数据分发的目标根路径，此路径在数管的另外一张表中配置。

    -- 选填项
    orderlevel      integer,                         -- 订单级别，1普通，2紧急，3特急，影响到数据回迁的优先级

    --输出项
    orderstate      integer,                         -- 订单状态，1待处理，2正在处理，-1处理成功，0失败

    -- 无用项
    ordertitle      character varying(200),          -- 订单标题，文字描述，对数管来说无实际意义
    ordersource     character varying(200),          -- 订单来源，文字描述，对数管来说无实际意义
    ordersourcetype integer,                         -- 订单来源数据类型，1内网订单，2外网订单，目前外网订单将直接交付网闸，以后就无实际意义了。
    orderendtime    timestamp(6) without time zone,  -- 订单需要完成时间，要求完成时间，对数管来说无实际意义
    userid          character varying(50),           -- 用户ID，文字描述，对数管来说无实际意义
    username        character varying(50),           -- 用户名称，文字描述，对数管来说无实际意义
    createtime      timestamp(6) without time zone,  -- 创建时间，对数管来说无实际意义
    lastmodifytime  timestamp(6) without time zone,  -- 最后修改时间，对数管来说无实际意义
    memo            text,                            -- 备注，对数管来说无实际意义
    CONSTRAINT dm_order_pkey PRIMARY KEY (orderid)
);

-- Table: public.dm_order_delivery

-- DROP TABLE public.dm_order_delivery;

CREATE TABLE public.dm_order_delivery
(
    -- 必填项
    orderid        character varying(200) NOT NULL, -- 订单ID，输入参数，必填
    dataid         character varying(200) NOT NULL, -- 数据ID，输入参数，必填

    --输出项
    datastatus     integer,                         -- 数据状态，1待处理，2数据准备中，-1完成，0失败
    distributepath character varying(2000),         -- 分发路径，输出参数，具体的数据回迁后的完整路径文件名

    -- 无用项
    datatype       character varying(200),          -- 数据类型，输出参数，对数管来说无实际意义
    createtime     timestamp(6) without time zone,  -- 创建时间，对数管来说无实际意义
    lastmodifytime timestamp(6) without time zone,  -- 最后修改时间，对数管来说无实际意义
    memo           character varying(50),           -- 备注，对数管来说无实际意义
    CONSTRAINT dm_order_delivery_pkey PRIMARY KEY (orderid, dataid)
);


----------------------------------2015-12-5 dm_index_catalog 增加产品英文名

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dictitle_en character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dictitle_en IS '产品英文名';

----------------------------------2015-12-7 dm_order_astype2dmlevel 增加数管-类型 to 紧急级别

DROP TABLE public.dm_order_astype2dmlevel;

CREATE TABLE public.dm_order_astype2dmlevel
(
    ordertype  character varying(50), -- 订单类型，描述订单的紧急程度，取字典表
    orderlevel integer,               -- 订单级别，0-15
    CONSTRAINT dm_order_astype2dmlevel_pkey PRIMARY KEY (ordertype, orderlevel)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_order_astype2dmlevel
    OWNER TO postgres;

COMMENT ON COLUMN public.dm_order_astype2dmlevel.ordertype IS '订单类型';
COMMENT ON COLUMN public.dm_order_astype2dmlevel.orderlevel IS '订单级别';

insert into public.dm_order_astype2dmlevel(ordertype, orderlevel)
values ('general', 5);
insert into public.dm_order_astype2dmlevel(ordertype, orderlevel)
values ('medium', 6);
insert into public.dm_order_astype2dmlevel(ordertype, orderlevel)
values ('urgency', 7);

----------------------------------2015-12-7 dm_order 修改订单级别的意义，取消123的备选，改为0-15的任意数值，该级别将直接反馈给磁带库出库系统
COMMENT ON COLUMN public.dm_order.orderlevel IS '订单级别，0-15';

----------------------------------2015-12-7 dm_order 取消mountpath、sourcepath等信息，改为直接从dm_dept_delivery表中获取

ALTER TABLE public.dm_order
    DROP COLUMN orderxml;
ALTER TABLE public.dm_order
    DROP COLUMN orderendtime;
ALTER TABLE public.dm_order
    DROP COLUMN mountpath;
ALTER TABLE public.dm_order
    DROP COLUMN sourcepath;

----------------------------------2015-12-7 as_afterorderapproved 修改订单级别的判断标准，改为从辅助表中获取

-- Function: public.as_afterorderapproved()

-- DROP FUNCTION public.as_afterorderapproved();

CREATE OR REPLACE FUNCTION public.as_afterorderapproved()
    RETURNS trigger AS
$BODY$
BEGIN
    /*--内网订单审批后，即as_order表orderstate = '10'后，将as_order,as_order_delivery数据更新到dm_order,dm_order_delivery数据表中*/
    IF (NEW.orderstate = '10') THEN
        insert into dm_order(orderid, ordertitle, ordersource, orderlevel, orderstate, userid, username, createtime,
                             lastmodifytime, ordersourcetype)
        select as_order.id,
               as_order.ordertitle,
               as_order.ordersource,
               (coalesce(dm_order_astype2dmlevel.orderlevel, 10)) as orderlevel,
               1                                                  as orderstate,
               userid,
               sys_user.name,
               current_timestamp,
               current_timestamp,
               1                                                  as ordersourcetype
        from sys_user,
             as_order
                 left join dm_order_astype2dmlevel on as_order.ordertype = dm_order_astype2dmlevel.ordertype
        where as_order.userid = sys_user.id
          and as_order.id = NEW.id;

        insert into dm_order_delivery(orderid, dataid, datastatus, datatype, createtime, lastmodifytime)
        select orderid,
               dataid,
               (case
                    when state = '0' then 1 --0待交付-->1待处理
                    when state = '1' then -1 --1待交付-->-1交付成功
                    when state = '2' then 0 end) as datastatus, --2交付失败-->-0交付失败
               datatype,
               current_timestamp,
               current_timestamp
        from as_order_delivery
        where orderid = NEW.id;
    END IF;
    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.as_afterorderapproved()
    OWNER TO postgres;

----------------------------------2015-12-7 修正ro_file表中扩展名不正确的记录

update ro_file
set ftype = '.zip'
where ftype = 'zip';

----------------------------------2015-12-13 修正dm_index表，增加备注、删除状态等字段

ALTER TABLE dm_index
    ADD COLUMN dimemo text;
COMMENT ON COLUMN dm_index.dimemo IS '产品备注';

ALTER TABLE dm_index
    ADD COLUMN dideleted integer default 0;
COMMENT ON COLUMN dm_index.dideleted IS '产品已删除';

ALTER TABLE dm_index
    ADD COLUMN dideletedTime timestamp with time zone;
COMMENT ON COLUMN dm_index.dideletedTime IS '产品删除时间';

CREATE INDEX idx_dm_index_deleted ON public.dm_index (dideleted);


---------------------------2015-12-13 修正标准镶嵌产品的所属时间
update dm_index
set didate = to_date(split_part(diid, '_', 3) || '-01-01', 'YYYY-MM-DD')
where didate is null
  and ditype = 'SCI_STD'

---------------------------2015-12-13 修正RNS产品的所属时间
update dm_index
set didate = to_date(split_part(diid, '_', 1) || '-01-01', 'YYYY-MM-DD')
where didate is null
  and ditype = 'RNS'

---------------------------2015-12-13 修正SCI_WL产品的所属时间
update dm_index
set didate = to_date(split_part(diid, '_', 3) || '-01-01', 'YYYY-MM-DD')
where didate is null
  and ditype = 'SCI_WL'

---------------------------2015-12-13 修正GF1_L0产品的所属时间
update dm_index
set didate = to_date(split_part(diid, '_', 5), 'YYYYMMDD')
where didate is null
  and ditype = 'GF1_L0'



----------------------------------2015-12-14 添加存储无空间信息的项目成果

-- DROP TABLE public.dm_index_ptd;

CREATE TABLE public.dm_index_ptd
(
-- 继承 from table dm_index:  diid character varying(3000) NOT NULL,
-- 继承 from table dm_index:  dixmlmeta xml,
-- 继承 from table dm_index:  dixmlversion character varying(50),
-- 继承 from table dm_index:  dizipfilelist text,
-- 继承 from table dm_index:  diclass character varying(50) NOT NULL,
-- 继承 from table dm_index:  ditype character varying(50),
-- 继承 from table dm_index:  didate timestamp without time zone,
-- 继承 from table dm_index:  diimporttime timestamp without time zone,
-- 继承 from table dm_index:  didatasource character varying(200),
-- 继承 from table dm_index:  dititle character varying(4000),
    dideptid  character varying(100),
    diaudited integer,
    CONSTRAINT dm_index_ptd_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_ptd_diclass_check CHECK (diclass::text = 'ptd'::text)
)
    INHERITS (public.dm_index)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_ptd
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_ptd
    IS '产品编目-项目专题成果';

COMMENT ON COLUMN dm_index_ptd.dideptid IS '产品所属部门';
COMMENT ON COLUMN dm_index_ptd.diaudited IS '产品是否已检验';


-- Index: public.idx_dm_index_ptd_class

-- DROP INDEX public.idx_dm_index_ptd_class;

CREATE INDEX idx_dm_index_ptd_class ON public.dm_index_ptd (diclass);

----------------------------------2015-12-14 添加存储项目成果的明细文件列表

-- DROP TABLE public.dm_index_ptd_files;

CREATE TABLE public.dm_index_ptd_files
(
    diid       character varying(3000) NOT NULL,
    difilename character varying(4000),
    CONSTRAINT dm_index_ptd_files_pkey PRIMARY KEY (diid, difilename)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_ptd_files
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_ptd_files
    IS '产品编目-项目专题成果文件明细';

COMMENT ON COLUMN dm_index_ptd_files.diid IS '产品标示';
COMMENT ON COLUMN dm_index_ptd_files.difilename IS '产品文件';

-------------------------------2015-12-15 将sch_mission表中的smTitle字段进行长度扩展，以适应更高的需要
ALTER TABLE public.sch_mission
    ALTER COLUMN smtitle TYPE character varying(4000);
COMMENT ON COLUMN public.sch_mission.smtitle IS '标题';

-------------------------------2015-12-16 sch_mission 增加任务所属字段
ALTER TABLE public.sch_mission
    Add COLUMN smOwner character varying(100);
COMMENT ON COLUMN public.sch_mission.smOwner IS '任务所有者';
ALTER TABLE public.sch_mission
    Add COLUMN smExecuter character varying(100);
COMMENT ON COLUMN public.sch_mission.smExecuter IS '任务执行者';

-------------------------------2015-12-17 将ro_file表中的fTitle字段进行长度扩展，以适应更高的需要
ALTER TABLE public.ro_file
    ALTER COLUMN fTitle TYPE character varying(4000);
COMMENT ON COLUMN public.ro_file.fTitle IS '标题';



-------------------------------2015-12-18 ro_dept 部门字典表

-- DROP TABLE public.dm_dept;

CREATE TABLE public.dm_dept
(
    ddcode  character varying(100) NOT NULL,
    ddtitle character varying(200)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_dept
    OWNER TO postgres;
COMMENT ON TABLE public.dm_dept
    IS '数管-部门字典表';

COMMENT ON COLUMN public.dm_dept.ddcode IS '部门代码';
COMMENT ON COLUMN public.dm_dept.ddtitle IS '部门名称';

insert into dm_dept(ddcode, ddtitle)
values ('infoproduce', '信息产品部');
insert into dm_dept(ddcode, ddtitle)
values ('imageproduce', '数据产品部');
insert into dm_dept(ddcode, ddtitle)
values ('qa', '质量管理部');

CREATE INDEX idx_sch_event_segroup ON public.sch_event (segroup);
CREATE INDEX idx_sch_event_secreatedate ON public.sch_event (secreatedate);


-------------------------------2015-12-23 dm_index_ptd 增加成果描述字段
ALTER TABLE public.dm_index_ptd
    Add COLUMN diDescription character varying(4000);
COMMENT ON COLUMN public.dm_index_ptd.diDescription IS '成果描述';


-------------------------------2015-12-29 dm_index_catalog 删除归档目录字段，改为从ro_file_server表中读取
ALTER TABLE dm_index_catalog
    DROP COLUMN dicarchivepath;


-------------------------------2015-12-31 dm_index_ptd_files 增加文件大小字段
ALTER TABLE dm_index_ptd_files
    Add COLUMN diFileSize integer;
COMMENT ON COLUMN public.dm_index_ptd_files.diFileSize IS '文件大小';

ALTER TABLE dm_index_ptd_files
    Add COLUMN diFileExt character varying(100);
COMMENT ON COLUMN public.dm_index_ptd_files.diFileExt IS '文件扩展名';

ALTER TABLE dm_index_ptd_files
    Add COLUMN diFileDate timestamp with time zone;
COMMENT ON COLUMN public.dm_index_ptd_files.diFileDate IS '文件日期';

ALTER TABLE dm_index_ptd_files
    Add COLUMN diIsSpatial integer;
COMMENT ON COLUMN public.dm_index_ptd_files.diIsSpatial IS '是否是空间文件';

ALTER TABLE dm_index_ptd_files
    Add COLUMN diSpatialMetaData xml;
COMMENT ON COLUMN public.dm_index_ptd_files.diSpatialMetaData IS '空间元数据';

ALTER TABLE dm_index_ptd_files
    Add COLUMN dimemo text;
COMMENT ON COLUMN public.dm_index_ptd_files.dimemo IS '备注';

ALTER TABLE public.dm_index_ptd_files
    ALTER COLUMN difilesize TYPE bigint;
COMMENT ON COLUMN public.dm_index_ptd_files.difilesize IS '文件大小';


---------------------------------2016-1-4 将dm_index_ptd_files.diIsSpatial字段的意义修改为空间文件类型

COMMENT ON COLUMN public.dm_index_ptd_files.diIsSpatial IS '空间文件类型';


---------------------------------2016-1-15 在dm_index中增加字段 diAllowDeployToWAN 描述特定数据是否允许被发布到外网
ALTER TABLE public.dm_index
    ADD COLUMN diAllowDeployToWAN integer DEFAULT 0;
COMMENT ON COLUMN public.dm_index.diAllowDeployToWAN IS '是否允许被发布至外网';



---------------------------------2016-1-15 增加ro_file_deleted 表，记录被删除的文件实体
-- Table: public.ro_file_deleted

-- DROP TABLE public.ro_file_deleted;

CREATE TABLE public.ro_file_deleted
(
    fid             character varying(100) NOT NULL,                        -- 标示
    ftitle          character varying(2000),                                -- 标题
    fsource         character varying(2000),                                -- 源目录名
    ftype           character varying(100),                                 -- 数据类型
    fmodifytime     timestamp with time zone,                               -- 最后修改时间
    fparentid       character varying(100) DEFAULT '-1'::character varying, -- 父标示
    fisgroup        bigint,                                                 -- 是否是目录
    ftreecode       character varying(2000),                                -- 树编码
    ftreelevel      bigint,                                                 -- 树级别
    fserverid       character varying(100),                                 -- 服务器标示
    fsize           bigint,                                                 -- 大小
    fattr           bigint,                                                 -- 属性
    fcatalog        character varying(200),                                 -- 业务分类
    flastmodifydate timestamp with time zone,                               -- 最后修改日期
    fsourcepath     character varying(2000),                                -- 数据存储路径
    flocation       character varying(2000),                                -- 数据存储位置，bj北京，sg新加坡
    fmd5code        character varying(200),                                 -- 文件MD5码
    fDeleteTime     timestamp with time zone,                               -- 删除时间
    fDeleteUserName character varying(100),                                 -- 删除人
    CONSTRAINT "ro_file_deleted_PK" PRIMARY KEY (fid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.ro_file_deleted
    OWNER TO postgres;
COMMENT ON COLUMN public.ro_file_deleted.fid IS '标示';
COMMENT ON COLUMN public.ro_file_deleted.ftitle IS '标题';
COMMENT ON COLUMN public.ro_file_deleted.fsource IS '源目录名';
COMMENT ON COLUMN public.ro_file_deleted.ftype IS '数据类型';
COMMENT ON COLUMN public.ro_file_deleted.fmodifytime IS '最后修改时间';
COMMENT ON COLUMN public.ro_file_deleted.fparentid IS '父标示';
COMMENT ON COLUMN public.ro_file_deleted.fisgroup IS '是否是目录';
COMMENT ON COLUMN public.ro_file_deleted.ftreecode IS '树编码';
COMMENT ON COLUMN public.ro_file_deleted.ftreelevel IS '树级别';
COMMENT ON COLUMN public.ro_file_deleted.fserverid IS '服务器标示';
COMMENT ON COLUMN public.ro_file_deleted.fsize IS '大小';
COMMENT ON COLUMN public.ro_file_deleted.fattr IS '属性';
COMMENT ON COLUMN public.ro_file_deleted.fcatalog IS '业务分类';
COMMENT ON COLUMN public.ro_file_deleted.flastmodifydate IS '最后修改日期';
COMMENT ON COLUMN public.ro_file_deleted.fsourcepath IS '数据存储路径';
COMMENT ON COLUMN public.ro_file_deleted.flocation IS '数据存储位置，bj北京，sg新加坡';
COMMENT ON COLUMN public.ro_file_deleted.fmd5code IS '文件MD5码';
COMMENT ON COLUMN public.ro_file_deleted.fDeleteTime IS '删除时间';
COMMENT ON COLUMN public.ro_file_deleted.fDeleteUserName IS '删除人';


-- Index: public.fcatalog_idx_ro_file_deleted

-- DROP INDEX public.fcatalog_idx_ro_file_deleted;

CREATE INDEX fcatalog_idx_ro_file_deleted
    ON public.ro_file_deleted
        USING btree
        (fcatalog COLLATE pg_catalog."default");

-- Index: public.fid_idx_ro_file_deleted

-- DROP INDEX public.fid_idx_ro_file_deleted;

CREATE INDEX fid_idx_ro_file_deleted
    ON public.ro_file_deleted
        USING btree
        (fid COLLATE pg_catalog."default");

-- Index: public.fserverid_idx_ro_file_deleted

-- DROP INDEX public.fserverid_idx_ro_file_deleted;

CREATE INDEX fserverid_idx_ro_file_deleted
    ON public.ro_file_deleted
        USING btree
        (fserverid COLLATE pg_catalog."default");

--------------------------------- 2016-1-18 dm_index_ndi中增加 无云geometry和云geometry

ALTER TABLE public.dm_index_ndi
    ADD COLUMN diNoCloudGeometry Geometry;
COMMENT ON COLUMN public.dm_index_ndi.diNoCloudGeometry IS '无云几何对象';

ALTER TABLE public.dm_index_ndi
    ADD COLUMN diCloudGeometry Geometry;
COMMENT ON COLUMN public.dm_index_ndi.diCloudGeometry IS '云几何对象';


--------------------------------- 2016-1-21 支持BJ2号编目同步进行了设计扩展
ALTER TABLE public.dm_index_sync
    ADD COLUMN diaudited integer DEFAULT 0;
COMMENT ON COLUMN public.dm_index_sync.diaudited IS '通过审核';

ALTER TABLE public.dm_index
    RENAME diallowdeploytowan TO diallowdeploy;
COMMENT ON COLUMN public.dm_index.diallowdeploy IS '允许发布';

ALTER TABLE public.dm_index_sync
    RENAME diaudited TO diallowdeploy;
COMMENT ON COLUMN public.dm_index_sync.diallowdeploy IS '允许发布';

--------------------------------- 发现待处理的问题


---------------------------------- 2016-2-26 添加存储全文检索分词表 dm_index_ftsearch

-- DROP TABLE public.dm_index_ftsearch;

CREATE TABLE public.dm_index_ftsearch
(
    difid           bigserial               not null,
    difTitle        character varying(3000) NOT NULL,

    difIndexId      character varying(100)  NOT NULL,
    difFileId       character varying(1000) NOT NULL,

    difclass        character varying(50)   NOT NULL,
    diftype         character varying(50)   NOT NULL,

    difFilename     character varying(4000) NOT NULL,
    difDescription  Text,

    difFileType     integer                 NOT NULL,

    difFileSize     bigint,
    difFileDate     timestamp with time zone,
    difFileExt      character varying(100),

    difFileMetaData xml,

    difSearch       tsvector,

    CONSTRAINT dm_index_ftsearch_pkey PRIMARY KEY (difid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_ftsearch
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_ftsearch
    IS '产品编目-全文检索分词表';

COMMENT ON COLUMN public.dm_index_ftsearch.difid IS '标示';
COMMENT ON COLUMN public.dm_index_ftsearch.difTitle IS '标题';
COMMENT ON COLUMN public.dm_index_ftsearch.difIndexId IS '编目标示';
COMMENT ON COLUMN public.dm_index_ftsearch.difFileId IS '文件标示';
COMMENT ON COLUMN public.dm_index_ftsearch.difclass IS '编目大类';
COMMENT ON COLUMN public.dm_index_ftsearch.diftype IS '编目小类';
COMMENT ON COLUMN public.dm_index_ftsearch.difFilename IS '文件全名';
COMMENT ON COLUMN public.dm_index_ftsearch.difDescription IS '备注';

COMMENT ON COLUMN public.dm_index_ftsearch.difFileType IS '数据类型';

COMMENT ON COLUMN public.dm_index_ftsearch.difFileSize IS '文件大小';
COMMENT ON COLUMN public.dm_index_ftsearch.difFileDate IS '文件日期';
COMMENT ON COLUMN public.dm_index_ftsearch.difFileExt IS '文件扩展名';

COMMENT ON COLUMN public.dm_index_ftsearch.difFileMetaData IS '文件元数据';
COMMENT ON COLUMN public.dm_index_ftsearch.difSearch IS '检索';

-- Index: public.idx_dm_index_ftsearch_class

-- DROP INDEX public.idx_dm_index_ftsearch_class;

CREATE INDEX idx_dm_index_ftsearch_search ON public.dm_index_ftsearch USING gin (difSearch);

CREATE INDEX idx_dm_index_ftsearch_class ON public.dm_index_ftsearch (difclass);
CREATE INDEX idx_dm_index_ftsearch_type ON public.dm_index_ftsearch (diftype);
CREATE INDEX idx_dm_index_ftsearch_filetype ON public.dm_index_ftsearch (difFileType);

CREATE INDEX idx_dm_index_ftsearch_filesize ON public.dm_index_ftsearch (difFileSize);
CREATE INDEX idx_dm_index_ftsearch_filedate ON public.dm_index_ftsearch (difFileDate);
CREATE INDEX idx_dm_index_ftsearch_fileext ON public.dm_index_ftsearch (difFileExt);

---------------------------------- 2016-2-26 添加子字符串统计个数的函数

create or replace function at_get_txt_count(p_source_txt character varying, p_count_txt character varying)
    returns integer
as
$at_get_txt_count$
declare
    v_idx        integer                 := 1;
    v_cnt        integer                 := 0;
    v_source_txt character varying(2000) := p_source_txt;
    v_len        integer                 := length(p_count_txt);
begin
    while v_idx > 0
        loop
            v_idx := position(p_count_txt in v_source_txt);
            if v_idx > 0 then
                v_cnt := v_cnt + 1;
                v_source_txt := right(v_source_txt, length(v_source_txt) - v_idx - v_len + 1);
            end if;
        end loop;
    return v_cnt;
end;
$at_get_txt_count$ language plpgsql;


---------------------------------- 2016-2-26 dm_index_ptd_files表增加唯一标示

ALTER TABLE public.dm_index_ptd_files
    ADD COLUMN diseqid bigserial;
COMMENT ON COLUMN public.dm_index_ptd_files.diseqid IS '序号';

ALTER TABLE public.dm_index_ptd_files
    ADD COLUMN dipfid character varying(200);
COMMENT ON COLUMN public.dm_index_ptd_files.dipfid IS '标示';

update dm_index_ptd_files
set dipfid = diid || '_' || diseqid;

--ALTER TABLE public.dm_index_ptd_files DROP COLUMN diseqid;


---------------------------------- 2016-2-26 dm_index_ftsearch 测试数据入库 记得将其中的\\改为\!!!!!!!!!!!!!!!!!!!!!!!!!!!1

delete
from dm_index_ftsearch;

insert into dm_index_ftsearch(diftitle, difindexid, diffileid, difclass, diftype, diffilename, difdescription,
                              diffiletype,
                              diffilesize, diffiledate, diffileext, diffilemetadata, difsearch)
select split_part(dm_index_ptd_files.difilename, '\\',
                  at_get_txt_count(dm_index_ptd_files.difilename, '\\') + 1)                   as diftitle,
       dm_index_ptd.diid                                                                       as difindexid,
       dm_index_ptd_files.dipfid                                                               as diffileid,
       dm_index_ptd.diclass                                                                    as difclass,
       dm_index_ptd.ditype                                                                     as diftype,
       Coalesce(dm_index_ptd.didescription, '') || Coalesce(dm_index_ptd_files.difilename, '') as difFilename,
       dm_index_ptd.dimemo                                                                     as difDescription,
       Coalesce(dm_index_ptd_files.diisspatial, 0)                                             as difFileType,
       dm_index_ptd_files.difilesize                                                           as difFileSize,
       dm_index_ptd_files.difiledate                                                           as difFileDate,
       dm_index_ptd_files.difileext                                                            as difFileExt,
       dm_index_ptd_files.dispatialmetadata                                                    as difFileMetaData,
       setweight(to_tsvector('zhparsercfg',
                             Coalesce(dm_index_ptd.didescription, '') || Coalesce(dm_index_ptd_files.difilename, '')),
                 'A')
           ||
       setweight(to_tsvector('zhparsercfg', Coalesce(dm_index_ptd.dimemo, '')), 'B')           as difSearch
from dm_index_ptd,
     dm_index_ptd_files
where dm_index_ptd.diid = dm_index_ptd_files.diid

ALTER TABLE public.dm_index
    ADD COLUMN diversion integer not null default 1;
COMMENT ON COLUMN public.dm_index.diversion IS '版本';


/*
select to_tsvector('zhParserCFG',diDescription), diDescription from dm_index_ptd 

ALTER TEXT SEARCH CONFIGURATION zhParserCFG ADD MAPPING FOR j WITH simple;


SELECT to_tsvector('zhParserCFG', '\001.国土项目\2015年\2015年鸡西市土地利用动态遥感监测\最终成果\2015年9月鸡西市土地利用动态遥感监测成果')
 @@to_tsquery('zhParserCFG', replace('国土 鸡西 动态遥感监测', ' ', '&'));

select diDescription from dm_index_ptd
where to_tsvector('zhParserCFG', diDescription) @@ to_tsquery('zhParserCFG', replace('2015 沙漠化', ' ', '&'));

*/

------------------------------2016-3-2 ，增加sch_mission表的索引

-- DROP INDEX public.smStatus_idx_sch_mission;

CREATE INDEX smStatus_idx_sch_mission ON public.sch_mission (smStatus);

------------------------------2016-3-3 ，梳理dm_index_catalog，增加对产品编目体系和产品实体的定义
ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicIsIndex integer not null default 0;
COMMENT ON COLUMN public.dm_index_catalog.dicIsIndex IS '是否是编目';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicIndexTitle character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dicIndexTitle IS '编目标题';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicIndexCode character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dicIndexCode IS '编目代码';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicIsData integer not null default 0;
COMMENT ON COLUMN public.dm_index_catalog.dicIsData IS '是否是数据';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicDataTitle character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dicDataTitle IS '数据标题';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicDataCode character varying(200);
COMMENT ON COLUMN public.dm_index_catalog.dicDataCode IS '数据代码';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicSearchCodes character varying(1000);
COMMENT ON COLUMN public.dm_index_catalog.dicSearchCodes IS '检索系统产品代码';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicCompareWithLanSearch integer not null default 0;
COMMENT ON COLUMN public.dm_index_catalog.dicSearchCodes IS '是否与内网检索实时对比';

ALTER TABLE public.dm_index_catalog
    ADD COLUMN dicCompareWithWanSearch integer not null default 0;
COMMENT ON COLUMN public.dm_index_catalog.dicSearchCodes IS '是否与外网检索实时对比';


--2016年3月2日 数据管理-删除--lwq

CREATE TABLE dm_index_manager_delete
(
    diid          character varying(3000) NOT NULL, -- 编目标示
    diversion     integer                 NOT NULL, -- 数据版本
    ditype        character varying(100),           -- 数据类型
    diprotype     integer                 NOT NULL,--操作类型，1覆盖，2手动删除
    diuserchnname character varying(200),           -- 操作人
    diprotime     timestamp with time zone,         -- 处理时间
    dipromemo     text,                             -- 备注信息

    CONSTRAINT "dm_index_manager_delete_PK" PRIMARY KEY (diid, diversion)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE dm_index_manager_delete
    OWNER TO postgres;
COMMENT ON TABLE dm_index_manager_delete
    IS '产品管理-删除';
COMMENT ON COLUMN dm_index_manager_delete.diid IS '编目标示';
COMMENT ON COLUMN dm_index_manager_delete.diversion IS '数据版本';
COMMENT ON COLUMN dm_index_manager_delete.ditype IS '数据类型';
COMMENT ON COLUMN dm_index_manager_delete.diprotype IS '操作类型，1覆盖，2手动删除';
COMMENT ON COLUMN dm_index_manager_delete.diuserchnname IS '操作人';
COMMENT ON COLUMN dm_index_manager_delete.diprotime IS '处理时间';
COMMENT ON COLUMN dm_index_manager_delete.dipromemo IS '备注信息';


CREATE INDEX idx_dm_index_manager_delete_id
    ON public.dm_index_manager_delete
        USING btree
        (diid COLLATE pg_catalog."default");


CREATE INDEX idx_dm_index_manager_delete_diversion
    ON public.dm_index_manager_delete
        USING btree
        (diversion);

CREATE INDEX idx_dm_index_manager_delete_protype
    ON public.dm_index_manager_delete
        USING btree
        (diprotype);


--2016年3月4日  数据入库-异常日志表--lwq

CREATE TABLE log_index_importtime
(
    limid      character varying(100) NOT NULL, -- 编目标识
    limversion integer                NOT NULL, --数据版本
    limtype    character varying(50),           --数据类型
    limtime    timestamp with time zone,        -- 时间
    limmemo    text,                            -- 详细信息
    CONSTRAINT "log_index_importtime_PK" PRIMARY KEY (limid, limversion)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE log_index_importtime
    OWNER TO postgres;
COMMENT ON TABLE log_index_importtime
    IS '日志-数据入库-异常记录表';
COMMENT ON COLUMN log_index_importtime.limid IS '编目标识';
COMMENT ON COLUMN log_index_importtime.limversion IS '数据版本';
COMMENT ON COLUMN log_index_importtime.limtype IS '数据类型';
COMMENT ON COLUMN log_index_importtime.limtime IS '时间';
COMMENT ON COLUMN log_index_importtime.limmemo IS '详细信息';

--2016-5-23 提高检索效率

CREATE INDEX idx_dm_index_ndi_taskid
    ON public.dm_index_ndi (ditaskid);

CREATE INDEX idx_dm_index_ndi_date
    ON public.dm_index_ndi (diDate);


-- 2016-5-23 IMIPAF-数据预处理明细表
CREATE TABLE public.ip_preprocess_log
(
    imid             character varying(100) NOT NULL, -- guid
    imfilename       character varying(200),          -- 文件名称 如D1000001VI_001-1.IMI
    imsrcfilepath    character varying(4000),         -- 扫描路径
    imworktime       character varying(50),           -- 扫描批次 如20160501001
    imtaskid         character varying(20),           -- 产品名称 如D1000001VI
    imtaskchild      character varying(100),          -- 产品子目录 如D1000001VI_001_005
    imlastmodifytime timestamp with time zone,        -- 最后修改时间
    imdownload       integer,                         -- 下载状态：...
    imstate          integer,                         -- 任务状态：...
    imdail           integer,                         -- 迁移情况：...
    imimiintegrity   integer,                         -- IMI完整性
    impafintegrity   integer,                         -- PAF完整性
    imgddail         integer,                         -- 归档处理...
    CONSTRAINT ip_preprocess_log_pkey PRIMARY KEY (imid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.ip_preprocess_log
    OWNER TO postgres;
COMMENT ON TABLE public.ip_preprocess_log
    IS '迁移日志表';
COMMENT ON COLUMN public.ip_preprocess_log.imid IS 'guid';
COMMENT ON COLUMN public.ip_preprocess_log.imfilename IS '文件名称-无路径';
COMMENT ON COLUMN public.ip_preprocess_log.imsrcfilepath IS '扫描路径';
COMMENT ON COLUMN public.ip_preprocess_log.imworktime IS '扫描批次';
COMMENT ON COLUMN public.ip_preprocess_log.imtaskid IS '任务号';
COMMENT ON COLUMN public.ip_preprocess_log.imtaskchild IS '产品子目录';
COMMENT ON COLUMN public.ip_preprocess_log.imlastmodifytime IS '最后修改时间';
COMMENT ON COLUMN public.ip_preprocess_log.imdownload IS '下载状态';
COMMENT ON COLUMN public.ip_preprocess_log.imstate IS '任务状态：1-常规;2-紧急';
COMMENT ON COLUMN public.ip_preprocess_log.imdail IS '迁移情况：0：未迁移;1：已经迁移;2：迁移失败;3：强制迁移';
COMMENT ON COLUMN public.ip_preprocess_log.imimiintegrity IS 'IMI完整';
COMMENT ON COLUMN public.ip_preprocess_log.impafintegrity IS 'PAF完整';
COMMENT ON COLUMN public.ip_preprocess_log.imgddail IS '归档处理: 0：未归档;1：已经归档;2：归档失败;3：已经存在';


CREATE INDEX idx_ip_preprocess_log_taskid
    ON public.ip_preprocess_log (imtaskid);

CREATE INDEX idx_ip_preprocess_log_ddail
    ON public.ip_preprocess_log (imgddail);
CREATE INDEX idx_ip_preprocess_log_dail
    ON public.ip_preprocess_log (imdail);
CREATE INDEX idx_ip_preprocess_log_imiintegrity
    ON public.ip_preprocess_log (imimiintegrity);
CREATE INDEX idx_ip_preprocess_log_pafintegrity
    ON public.ip_preprocess_log (impafintegrity);

truncate table ip_preprocess_log;

insert into ip_preprocess_log(imid, imfilename, imsrcfilepath, imworktime, imtaskid, imtaskchild,
                              imdownload, imdail, imstate, imimiintegrity, impafintegrity)
select imid,
       imfilename,
       imsrcfilepath,
       imworktime,
       imtaskid,
       imtaskchild,
       case imdownload::text when 'True' then -1 else 0 end   as imdownload,
       imdail::integer,
       case imstate::text when '紧急' then 2 else 1 end         as imstate,
       case imimiintegrity::text when '完整' then -1 else 0 end as imimiintegrity,
       case impafintegrity::text when '完整' then -1 else 0 end as impafintegrity
from ip_move_log
where imdail = '1'
   or imdail = '3';

--2016-5-24 增加IMIPAF-归档日志表
CREATE TABLE public.ip_archive_log
(
    iaid             character varying(100) NOT NULL, -- guid
    iataskid         character varying(20),           -- 任务号 如D1000001
    iasceneid        character varying(20),           -- 景序号 如001
    iatype           integer,                         -- 类型：1-imi；2-paf
    iaResult         integer,                         -- 归档交付是否成功
    ialastmodifytime timestamp with time zone,        -- 最后修改时间
    iamemo           text,
    CONSTRAINT ip_archive_log_pkey PRIMARY KEY (iaid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.ip_archive_log
    OWNER TO postgres;
COMMENT ON TABLE public.ip_archive_log
    IS '迁移日志表';
COMMENT ON COLUMN public.ip_archive_log.iaid IS 'guid';
COMMENT ON COLUMN public.ip_archive_log.iataskid IS '任务号';
COMMENT ON COLUMN public.ip_archive_log.iasceneid IS '景序号';
COMMENT ON COLUMN public.ip_archive_log.iatype IS '类型：1-imi；2-paf';
COMMENT ON COLUMN public.ip_archive_log.iaResult IS '归档交付情况：0：未迁移;1：已经迁移;2：迁移失败';
COMMENT ON COLUMN public.ip_archive_log.ialastmodifytime IS '最后修改时间';
COMMENT ON COLUMN public.ip_archive_log.iamemo IS '备注';


CREATE INDEX idx_ip_archive_log_taskid
    ON public.ip_archive_log (iataskid);
CREATE INDEX idx_ip_archive_log_sceneid
    ON public.ip_archive_log (iasceneid);
CREATE INDEX idx_ip_archive_log_type
    ON public.ip_archive_log (iatype);
CREATE INDEX idx_ip_archive_log_Result
    ON public.ip_archive_log (iaResult);


-- 2016-5-26 完善dm_order的处理逻辑，改为从dm_order_delevery表更新

CREATE OR REPLACE FUNCTION public.dm_afterdatastatuschanged()
    RETURNS trigger AS
$BODY$
DECLARE
    --dm_order_delivery表数据状态改变时，更新as_order_delivery表相应数据状态
    tmp_ordersourcetype integer;
    i_allDataDelivery   integer;
BEGIN
    select ordersourcetype from dm_order where orderid = NEW.orderid INTO STRICT tmp_ordersourcetype;
    IF (tmp_ordersourcetype = 1 and NEW.datastatus = -1) THEN -- -1数据分发完成
        update as_order_delivery
        set state     = '1',
            address=NEW.distributepath,
            submittime=current_timestamp
        where orderid = NEW.orderid
          and dataid = NEW.dataid;
    ELSEIF (tmp_ordersourcetype = 1 and NEW.datastatus = 0) THEN -- 0数据分发失败
        update as_order_delivery
        set state     = '2',
            address=NEW.distributepath,
            submittime=current_timestamp
        where orderid = NEW.orderid
          and dataid = NEW.dataid;
    END IF;

    select count(*)
    from dm_order_delivery
    where orderid = NEW.orderid
      and datastatus != -1
    INTO STRICT i_allDataDelivery;
    IF (i_allDataDelivery = 0) THEN -- 如果所有数据均分发完成，则将数据管理订单标记为完成
        update dm_order set orderstate = -1, lastmodifytime = current_timestamp where orderid = NEW.orderid;
    END IF;

    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.dm_afterdatastatuschanged()
    OWNER TO postgres;

/*
select * from dm_order where orderid = 'vb9c2ed18750f4e50b5041adab3269d4b'


select count(*) from dm_order_delivery where orderid = 'vb9c2ed18750f4e50b5041adab3269d4b' and datastatus != -1


select * from dm_order_delivery where datastatus != -1 order by orderid desc limit 100

*/


-- 2016-5-31 测试从dm_index_ndi中分离出BJ2号编目的可能性

create table dm_index_ndi_bak as
select *
from dm_index_ndi;

CREATE INDEX dm_index_ndi_bak_class
    ON dm_index_ndi_bak (diclass);

CREATE INDEX dm_index_ndi_bak_type
    ON dm_index_ndi_bak (ditype);


delete
from dm_index_ndi
where ditype = 'BJ2_L1';


CREATE TABLE dm_index_ndi_BJ2
(
    ditaskid  character varying(50),
    disceneid character varying(50),
    CONSTRAINT dm_index_ndi_BJ2_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_ndi_BJ2_ditype_check CHECK (diType::text = 'BJ2_L1'::text),
    CONSTRAINT dm_index_ndi_diclass_check CHECK (diclass::text = 'ndi'::text),
    CONSTRAINT dm_index_spatial_diclass_check CHECK (diclass::text = 'ndi'::text OR diclass::text = 'zz'::text OR
                                                     diclass::text = 'geo'::text)
)
    INHERITS (dm_index_ndi)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE dm_index_ndi_bj2
    OWNER TO postgres;
COMMENT ON TABLE dm_index_ndi_bj2
    IS '产品编目-标准产品';
COMMENT ON COLUMN dm_index_ndi_bj2.diid IS '编目标示';
COMMENT ON COLUMN dm_index_ndi_bj2.dixmlmeta IS 'XML元数据';
COMMENT ON COLUMN dm_index_ndi_bj2.dixmlversion IS 'XML版本号';
COMMENT ON COLUMN dm_index_ndi_bj2.dizipfilelist IS '数据包文件列表';
COMMENT ON COLUMN dm_index_ndi_bj2.diclass IS '大类';
COMMENT ON COLUMN dm_index_ndi_bj2.ditype IS '数据类型';
COMMENT ON COLUMN dm_index_ndi_bj2.didate IS '影像拍摄或者数据下载时间';
COMMENT ON COLUMN dm_index_ndi_bj2.diimporttime IS '入库时间';
COMMENT ON COLUMN dm_index_ndi_bj2.didatasource IS '数据来源';
COMMENT ON COLUMN dm_index_ndi_bj2.dixmlfile IS '元数据文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.digeometry IS '编目空间范围';
COMMENT ON COLUMN dm_index_ndi_bj2.diserverid IS '编目服务器标示';
COMMENT ON COLUMN dm_index_ndi_bj2.dipanbrowserimg IS '全色缩略图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dipantransformimg IS '全色斜视图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dipanthumbimg IS '全色拇指图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dipantifimg IS 'GeoTiff格式全色浏览图';
COMMENT ON COLUMN dm_index_ndi_bj2.dipankmzimg IS 'KMZ格式全色浏览图';
COMMENT ON COLUMN dm_index_ndi_bj2.dimuxbrowserimg IS '多光谱缩略图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dimuxtransformimg IS '多光谱斜视图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dimuxthumbimg IS '多光谱拇指图文件路径';
COMMENT ON COLUMN dm_index_ndi_bj2.dimuxtifimg IS 'GeoTiff格式多光谱浏览图';
COMMENT ON COLUMN dm_index_ndi_bj2.dimuxkmzimg IS 'KMZ格式多光谱浏览图';
COMMENT ON COLUMN dm_index_ndi_bj2.dititle IS '产品标题';
COMMENT ON COLUMN dm_index_ndi_bj2.dimemo IS '产品备注';
COMMENT ON COLUMN dm_index_ndi_bj2.dideleted IS '产品已删除';
COMMENT ON COLUMN dm_index_ndi_bj2.dideletedtime IS '产品删除时间';

COMMENT ON COLUMN dm_index_ndi_bj2.ditaskid IS '产品任务号';
COMMENT ON COLUMN dm_index_ndi_bj2.disceneid IS '产品景编号';

-- Index: idx_dm_index_ndi_bj2_class

-- DROP INDEX idx_dm_index_ndi_bj2_class;

CREATE INDEX idx_dm_index_ndi_bj2_class
    ON dm_index_ndi_bj2 (diclass);

CREATE INDEX idx_dm_index_ndi_bj2_type
    ON dm_index_ndi_bj2 (ditype);

CREATE INDEX idx_dm_index_ndi_bj2_taskid
    ON dm_index_ndi_bj2 (ditaskid);

CREATE INDEX idx_dm_index_ndi_bj2_sceneid
    ON dm_index_ndi_bj2 (disceneid);

insert into dm_index_ndi_bj2 (select * from dm_index_ndi_bak where ditype = 'BJ2_L1');


--2016-5-31 优化数据表dm_order_delivery
CREATE INDEX idx_dm_order_delivery_DataStatus
    ON dm_order_delivery (datastatus);

CREATE INDEX idx_dm_order_delivery_datatype
    ON dm_order_delivery (datatype);

CREATE INDEX idx_dm_order_delivery_lastmodifytime
    ON dm_order_delivery (lastmodifytime);

CREATE INDEX idx_dm_order_delivery_createtime
    ON dm_order_delivery (createtime);

--完善订单处理触发器，解决订单不能从处理中 正常改为处理完毕的bug

CREATE OR REPLACE FUNCTION public.dm_afterdatastatuschanged()
    RETURNS trigger AS
$BODY$
DECLARE
    --dm_order_delivery表数据状态改变时，更新as_order_delivery表相应数据状态
    tmp_ordersourcetype   integer;
    i_SomeDataNotSuccess  integer;
    i_SomeDataNotFinished integer;
BEGIN
    select ordersourcetype from dm_order where orderid = NEW.orderid INTO STRICT tmp_ordersourcetype;
    IF (tmp_ordersourcetype = 1 and NEW.datastatus = -1) THEN -- -1数据分发完成
        update as_order_delivery
        set state     = '1',
            address=NEW.distributepath,
            submittime=current_timestamp
        where orderid = NEW.orderid
          and dataid = NEW.dataid;
    ELSEIF (tmp_ordersourcetype = 1 and NEW.datastatus = 0) THEN -- 0数据分发失败
        update as_order_delivery
        set state     = '2',
            address=NEW.distributepath,
            submittime=current_timestamp
        where orderid = NEW.orderid
          and dataid = NEW.dataid;
    END IF;

    select count(*)
    from dm_order_delivery
    where orderid = NEW.orderid
      and datastatus != -1
    INTO STRICT i_SomeDataNotSuccess;
    select count(*)
    from dm_order_delivery
    where orderid = NEW.orderid
      and datastatus not in (-1, 0)
    INTO STRICT i_SomeDataNotFinished;
    IF (i_SomeDataNotSuccess = 0) THEN
        -- 如果所有数据均分发完成且成功，则i_SomeDataNotSuccess为0，则将数据管理订单标记为-1
        update dm_order set orderstate = -1, lastmodifytime = current_timestamp where orderid = NEW.orderid;
    ELSEIF (i_SomeDataNotFinished = 0) THEN
        -- 如果所有数据均已经处理，不管成功或失败，则i_SomeDataNotFinished为0，则将数据管理订单标记为0
        update dm_order set orderstate = 0, lastmodifytime = current_timestamp where orderid = NEW.orderid;
    END IF;

    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.dm_afterdatastatuschanged()
    OWNER TO postgres;


ALTER TABLE public.dm_order_delivery
    ALTER COLUMN memo TYPE text;
COMMENT ON COLUMN public.dm_order_delivery.memo IS '备注';



CREATE INDEX idx_dmc3_imagefile_sat
    ON public.dmc3_imagefile (sat);

CREATE INDEX idx_dmc3_imagefile_imagefileid
    ON public.dmc3_imagefile (imagefileid);

CREATE INDEX idx_dmc3_imagefile_filenameinitialpart
    ON public.dmc3_imagefile (filenameinitialpart);

CREATE INDEX idx_dmc3_imagefile_filenameuniquepart
    ON public.dmc3_imagefile (filenameuniquepart);


select getView.ditaskid,
       getView.dmcTaskCount,
       process.produce_instore_Count,
       YS.ys_instore_Count,
       process.produce_instore_Count - YS.ys_instore_Count as bad_YS_count,
       L1.l1_instore_Count,
       YS.ys_instore_Count - L1.l1_instore_Count           as bad_l1_count
from (
         select FileNameInitialPart as diTaskID, count(*) as dmcTaskCount
         from dmc3_imagefile
         group by Sat, FileNameInitialPart
     ) getView
         left join (
    select substring(iptaskid, 0, 9) as ditaskid, count(*) / 4 as produce_instore_Count
    from ip_preprocess_log
    where ipimiintegrity = -1
      and ippafintegrity = -1
    group by iptaskid
) process on getView.diTaskID = process.ditaskid
         left join (
    select ditaskid, count(*) as ys_instore_Count
    from dm_index_ys
    where ditype = 'BJ2_YS'
    group by ditaskid
) YS on getView.diTaskID = YS.ditaskid
         left join (
    select ditaskid, count(*) as l1_instore_Count
    from dm_index_ndi
    where ditype = 'BJ2_L1'
    group by ditaskid
) L1 on getView.diTaskID = L1.ditaskid
order by getView.ditaskid

---2016-07-13  内外网增加编目来源字段  吕伟强

ALTER TABLE public.dm_index_ndi
    ADD COLUMN character varying(100);
COMMENT ON COLUMN public.dm_index_ndi.diindexsource IS '编目来源：bj表示北京，sg新加坡';


--2016-07-15  数管系统数据库增加表 log_index_sync_sg 用来记录新加坡编目在内网入库监控  吕伟强
CREATE TABLE public.log_index_sync_sg
(
    lisid        character varying(100) NOT NULL, -- 同步标示
    listype      integer DEFAULT 1,               -- 同步类型；1-新加坡编目同步至主中心;2-......
    lisindexid   character varying(100) NOT NULL, -- 同步产品编目标示
    lissuccess   integer DEFAULT 0,               -- 同步是否成功;0-否;-1-是
    lisstarttime timestamp with time zone,        -- 同步开始时间
    lisendtime   timestamp with time zone,        -- 同步结束时间
    lismemo      text,                            -- 同步备注
    CONSTRAINT "log_index_syncsg_PK" PRIMARY KEY (lisid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.log_index_sync_sg
    OWNER TO postgres;
COMMENT ON TABLE public.log_index_sync_sg
    IS '日志-产品编目-新加坡编目同步记录';
COMMENT ON COLUMN public.log_index_sync_sg.lisid IS '同步标示';
COMMENT ON COLUMN public.log_index_sync_sg.listype IS '同步类型；1-新加坡编目同步至主中心;2-......';
COMMENT ON COLUMN public.log_index_sync_sg.lisindexid IS '同步产品编目标示';
COMMENT ON COLUMN public.log_index_sync_sg.lissuccess IS '同步是否成功;0-否;-1-是';
COMMENT ON COLUMN public.log_index_sync_sg.lisstarttime IS '同步开始时间';
COMMENT ON COLUMN public.log_index_sync_sg.lisendtime IS '同步结束时间';
COMMENT ON COLUMN public.log_index_sync_sg.lismemo IS '同步备注';



--2016-8-15 设计三农普的编目表结构

-- Table: public.dm_index_proj

-- DROP TABLE public.dm_index_proj;

CREATE TABLE public.dm_index_proj
(
-- 继承 from table dm_index:  diid character varying(3000) NOT NULL, -- 编目标示
-- 继承 from table dm_index:  dixmlmeta xml, -- XML元数据
-- 继承 from table dm_index:  dixmlversion character varying(50), -- XML版本号
-- 继承 from table dm_index:  dizipfilelist text, -- 数据包文件列表
-- 继承 from table dm_index:  diclass character varying(50) NOT NULL, -- 大类
-- 继承 from table dm_index:  ditype character varying(50), -- 数据类型
-- 继承 from table dm_index:  didate timestamp without time zone, -- 影像拍摄或者数据下载时间
-- 继承 from table dm_index:  diimporttime timestamp without time zone, -- 入库时间
-- 继承 from table dm_index:  didatasource character varying(200), -- 数据来源
-- 继承 from table dm_index:  dititle character varying(4000), -- 产品标题
-- 继承 from table dm_index:  dimemo text, -- 产品备注
-- 继承 from table dm_index:  dideleted integer DEFAULT 0, -- 产品已删除
-- 继承 from table dm_index:  dideletedtime timestamp with time zone, -- 产品删除时间
-- 继承 from table dm_index:  diallowdeploy integer DEFAULT 0,
-- 继承 from table dm_index:  diversion integer NOT NULL DEFAULT 1,
-- 继承 from table dm_index:  diserverid character varying(100),
-- 继承 from table dm_index:  dimetadatapath character varying(4000),
-- 继承 from table dm_index:  dimetadatafilename character varying(1000),
-- 继承 from table dm_index:  dideleteduserid character varying(100),
    diprojectid character varying(200), -- 项目标示
    CONSTRAINT dm_index_proj_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_proj_diclass_check CHECK (diclass::text = 'project'::text)
)
    INHERITS (public.dm_index)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_proj
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_proj
    IS '产品编目-项目-成果';
COMMENT ON COLUMN public.dm_index_proj.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index_proj.dixmlmeta IS 'XML元数据';
COMMENT ON COLUMN public.dm_index_proj.dixmlversion IS 'XML版本号';
COMMENT ON COLUMN public.dm_index_proj.dizipfilelist IS '数据包文件列表';
COMMENT ON COLUMN public.dm_index_proj.diclass IS '大类';
COMMENT ON COLUMN public.dm_index_proj.ditype IS '数据类型';
COMMENT ON COLUMN public.dm_index_proj.didate IS '影像拍摄或者数据下载时间';
COMMENT ON COLUMN public.dm_index_proj.diimporttime IS '入库时间';
COMMENT ON COLUMN public.dm_index_proj.didatasource IS '数据来源';
COMMENT ON COLUMN public.dm_index_proj.dititle IS '产品标题';
COMMENT ON COLUMN public.dm_index_proj.dimemo IS '产品备注';
COMMENT ON COLUMN public.dm_index_proj.dideleted IS '产品已删除';
COMMENT ON COLUMN public.dm_index_proj.dideletedtime IS '产品删除时间';
COMMENT ON COLUMN public.dm_index_proj.diprojectid IS '项目标示';


-- Index: public.idx_dm_index_proj_class

-- DROP INDEX public.idx_dm_index_proj_class;

CREATE INDEX idx_dm_index_proj_class
    ON public.dm_index_proj
        USING btree
        (diclass COLLATE pg_catalog."default");

-- Index: public.idx_dm_index_proj_projectid

-- DROP INDEX public.idx_dm_index_proj_projectid;

CREATE INDEX idx_dm_index_proj_projectid
    ON public.dm_index_proj
        USING btree
        (diprojectid COLLATE pg_catalog."default");

-- Table: public.dm_index_proj_nongpu_3

-- DROP TABLE public.dm_index_proj_nongpu_3;

CREATE TABLE public.dm_index_proj_nongpu_3
(
-- 继承 from table dm_index_proj:  diid character varying(3000) NOT NULL, -- 编目标示
-- 继承 from table dm_index_proj:  dixmlmeta xml, -- XML元数据
-- 继承 from table dm_index_proj:  dixmlversion character varying(50), -- XML版本号
-- 继承 from table dm_index_proj:  dizipfilelist text, -- 数据包文件列表
-- 继承 from table dm_index_proj:  diclass character varying(50) NOT NULL, -- 大类
-- 继承 from table dm_index_proj:  ditype character varying(50), -- 数据类型
-- 继承 from table dm_index_proj:  didate timestamp without time zone, -- 影像拍摄或者数据下载时间
-- 继承 from table dm_index_proj:  diimporttime timestamp without time zone, -- 入库时间
-- 继承 from table dm_index_proj:  didatasource character varying(200), -- 数据来源
-- 继承 from table dm_index_proj:  dititle character varying(4000), -- 产品标题
-- 继承 from table dm_index_proj:  dimemo text, -- 产品备注
-- 继承 from table dm_index_proj:  dideleted integer DEFAULT 0, -- 产品已删除
-- 继承 from table dm_index_proj:  dideletedtime timestamp with time zone, -- 产品删除时间
-- 继承 from table dm_index_proj:  diallowdeploy integer DEFAULT 0,
-- 继承 from table dm_index_proj:  diversion integer NOT NULL DEFAULT 1,
-- 继承 from table dm_index_proj:  diserverid character varying(100),
-- 继承 from table dm_index_proj:  dimetadatapath character varying(4000),
-- 继承 from table dm_index_proj:  dimetadatafilename character varying(1000),
-- 继承 from table dm_index_proj:  dideleteduserid character varying(100),
-- 继承 from table dm_index_proj:  diprojectid character varying(200), -- 项目标示
    dicatalog    character varying(200),  -- 成果类型
    diresolution character varying(10),   -- 分辨率
    disrid       character varying(50),   -- 坐标系
    digeometry   geometry,                -- 空间范围
    dibrowserimg character varying(1000), -- 快视图
    dithumbimg   character varying(1000), -- 拇指图
    CONSTRAINT dm_index_proj_nongpu_3_pkey PRIMARY KEY (diid),
    CONSTRAINT dm_index_proj_diclass_check CHECK (diclass::text = 'project'::text),
    CONSTRAINT dm_index_proj_nongpu_3_diprojectid_check CHECK (diprojectid::text = 'proj_nongpu_3'::text)
)
    INHERITS (public.dm_index_proj)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_index_proj_nongpu_3
    OWNER TO postgres;
COMMENT ON TABLE public.dm_index_proj_nongpu_3
    IS '产品编目-项目-三农普';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.diid IS '编目标示';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dixmlmeta IS 'XML元数据';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dixmlversion IS 'XML版本号';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dizipfilelist IS '数据包文件列表';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.diclass IS '大类';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.ditype IS '数据类型';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.didate IS '影像拍摄或者数据下载时间';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.diimporttime IS '入库时间';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.didatasource IS '数据来源';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dititle IS '产品标题';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dimemo IS '产品备注';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dideleted IS '产品已删除';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dideletedtime IS '产品删除时间';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.diprojectid IS '项目标示';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dicatalog IS '成果类型';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.diresolution IS '分辨率';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.disrid IS '坐标系';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.digeometry IS '空间范围';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dibrowserimg IS '快视图';
COMMENT ON COLUMN public.dm_index_proj_nongpu_3.dithumbimg IS '拇指图';

-- Index: public.idx_dm_index_proj_nongpu_3_class

-- DROP INDEX public.idx_dm_index_proj_nongpu_3_class;

CREATE INDEX idx_dm_index_proj_nongpu_3_class
    ON public.dm_index_proj_nongpu_3
        USING btree
        (diclass COLLATE pg_catalog."default");

-- Index: public.idx_dm_index_proj_nongpu_3_projectid

-- DROP INDEX public.idx_dm_index_proj_nongpu_3_projectid;

CREATE INDEX idx_dm_index_proj_nongpu_3_projectid
    ON public.dm_index_proj_nongpu_3
        USING btree
        (diprojectid COLLATE pg_catalog."default");


------------------------2016-8-22 发现一个bug！！！在回迁失败时，订单的交付状态仍然会被改为成功，而备注中却写着回迁失败。今天已经修正。
-- Function: public.dm_afterrestoretaskstatuschanged()

-- DROP FUNCTION public.dm_afterrestoretaskstatuschanged();

CREATE OR REPLACE FUNCTION public.dm_afterrestoretaskstatuschanged()
    RETURNS trigger AS
$BODY$
DECLARE
    --dm_restore_task表恢复任务状态改变时，更新dm_order_delivery表相应数据状态
    DECLARE
    --定义变量
    tmp_orderid      character varying(200);
    tmp_dataid       character varying(200);
    tmp_destfilename character varying(2000);
BEGIN
    IF (NEW.taskstatus = -1) THEN -- -1数据回迁完成
    --执行查询，将查询结果写入变量
        select t2.orderid, t2.dataid, t2.destfilename
        from dm_restore_task t1,
             dm_plan_task t2
        where t1.taskid = NEW.taskid
          and t1.plantaskid = t2.plantaskid
        INTO STRICT tmp_orderid,tmp_dataid,tmp_destfilename;
        update dm_order_delivery t1
        set datastatus    = -1,
            distributepath=tmp_destfilename,
            lastmodifytime=current_timestamp,
            memo=null
        where t1.orderid = tmp_orderid
          and t1.dataid = tmp_dataid;
    ELSEIF (NEW.taskstatus = 0) THEN -- 0数据分发失败
        select t2.orderid, t2.dataid, t2.destfilename
        from dm_restore_task t1,
             dm_plan_task t2
        where t1.taskid = NEW.taskid
          and t1.plantaskid = t2.plantaskid
        INTO STRICT tmp_orderid,tmp_dataid,tmp_destfilename;
        update dm_order_delivery t1
        set datastatus    = 0,
            distributepath=null,
            lastmodifytime=current_timestamp,
            memo='数据回迁失败'
        where t1.orderid = tmp_orderid
          and t1.dataid = tmp_dataid;
    END IF;
    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.dm_afterrestoretaskstatuschanged()
    OWNER TO postgres;


----------------2016-8-29 增加回迁任务失败重试统计表，以控制在预定的重试次数内，对回迁任务进行重试
DROP TABLE public.dm_restore_task_retry;

CREATE TABLE public.dm_restore_task_retry
(
    taskid         character varying(100) NOT NULL, -- 恢复任务ID
    retrycount     integer default 0,
    lastmodifytime timestamp with time zone,        -- 最后修改时间
    memo           text,                            -- 备注
    CONSTRAINT "dm_restore_task_retry_PK" PRIMARY KEY (taskid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.dm_restore_task_retry
    OWNER TO postgres;
COMMENT ON TABLE public.dm_restore_task_retry
    IS '产品回迁-任务-重试';
COMMENT ON COLUMN public.dm_restore_task_retry.taskid IS '恢复任务ID';
COMMENT ON COLUMN public.dm_restore_task_retry.retrycount IS '重试累计次数';
COMMENT ON COLUMN public.dm_restore_task_retry.lastmodifytime IS '最后修改时间';
COMMENT ON COLUMN public.dm_restore_task_retry.memo IS '备注';



ALTER TABLE dm_index_ndi_bj2
    ADD COLUMN diSatID character varying(10);
ALTER TABLE dm_index_ndi_bj2
    ADD COLUMN diSatTaskID character varying(10);
ALTER TABLE dm_index_ndi_bj2
    ADD COLUMN diSatSceneID character varying(10);
COMMENT ON COLUMN dm_index_ndi_bj2.diSatID IS '卫星编号';
COMMENT ON COLUMN dm_index_ndi_bj2.diSatTaskID IS '卫星观测任务号';
COMMENT ON COLUMN dm_index_ndi_bj2.diSatSceneID IS '卫星观测景编号';
update dm_index_ndi_bj2
set diSatID = substr(diid, 11, 1);
update dm_index_ndi_bj2
set diSatTaskID = substr(diid, 32, 6);
update dm_index_ndi_bj2
set diSatSceneID = substr(diid, 41, 3);

CREATE INDEX idx_dm_index_ndi_bj2_SatInfo
    ON public.dm_index_ndi_bj2 (diSatID, diSatTaskID, diSatSceneID);


---------------------2016-11-7 优化数据库检索统计效率
ALTER TABLE ro_file
    ADD COLUMN fInstoreDate timestamp without time zone;
COMMENT ON COLUMN ro_file.fInstoreDate IS '入库日期';

update ro_file
set fInstoreDate = flastmodifydate::date;

CREATE INDEX idx_ro_file_InstoreDate ON public.ro_file (fInstoreDate);


ALTER TABLE dm_archive_object
    ADD COLUMN daoArchiveDate timestamp without time zone;
COMMENT ON COLUMN dm_archive_object.daoArchiveDate IS '归档成功日期';

update dm_archive_object
set daoArchiveDate = lastmodifydate::date;

CREATE INDEX idx_dm_archive_object_ArchiveDate ON public.dm_archive_object (daoArchiveDate);


ALTER TABLE dm_archive_clear
    ADD COLUMN dacClearDate timestamp without time zone;
COMMENT ON COLUMN dm_archive_clear.dacClearDate IS '清理日期';

update dm_archive_clear
set dacClearDate = cleartime::date;

CREATE INDEX idx_dm_archive_clear_ClearDate ON public.dm_archive_clear (dacClearDate);



CREATE OR REPLACE FUNCTION public.dm_after_dm_archive_object_inserted()
    RETURNS trigger AS
$BODY$
BEGIN
    update dm_archive_object set daoarchivedate = lastmodifydate::date where fileid = NEW.fileid;
    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.dm_afterdatastatuschanged()
    OWNER TO postgres;


CREATE TRIGGER trigger_after_dm_archive_object_inserted
    AFTER insert
    ON public.dm_archive_object
    FOR EACH ROW
EXECUTE PROCEDURE public.dm_after_dm_archive_object_inserted();



-- Function: public.dm_afterdatastatuschanged()

-- DROP FUNCTION public.dm_afterdatastatuschanged();

CREATE OR REPLACE FUNCTION public.dm_afterdatastatuschanged()
    RETURNS trigger AS
$BODY$
DECLARE
    --dm_order_delivery表数据状态改变时，更新as_order_delivery表相应数据状态
    tmp_ordersourcetype   integer;
    i_SomeDataNotSuccess  integer;
    i_SomeDataNotFinished integer;
BEGIN
    IF (OLD.datastatus != NEW.datastatus) THEN
        select ordersourcetype from dm_order where orderid = NEW.orderid INTO STRICT tmp_ordersourcetype;
        IF (tmp_ordersourcetype = 1 and NEW.datastatus = -1) THEN -- -1数据分发完成
            update as_order_delivery
            set state      = '1',
                address    = NEW.distributepath,
                submittime = current_timestamp
            where orderid = NEW.orderid
              and dataid = NEW.dataid;
        ELSEIF (tmp_ordersourcetype = 1 and (NEW.datastatus = 0 or NEW.datastatus = 3)) THEN -- 0数据分发失败
            update as_order_delivery
            set state      = '2',
                address    = NEW.distributepath,
                submittime = current_timestamp
            where orderid = NEW.orderid
              and dataid = NEW.dataid;
        END IF;
    END IF;
    RETURN NULL;
END;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;
ALTER FUNCTION public.dm_afterdatastatuschanged()
    OWNER TO postgres;


/*
    此部分业务，已经移动至系统中执行。
    select count(*) from dm_order_delivery where orderid = NEW.orderid and datastatus != -1  INTO STRICT i_SomeDataNotSuccess ;
    select count(*) from dm_order_delivery where orderid = NEW.orderid and datastatus in (1, 2) INTO STRICT i_SomeDataNotFinished ;
    IF (i_SomeDataNotSuccess = 0) THEN 
      -- 如果所有数据均分发完成且成功，则i_SomeDataNotSuccess为0，则将数据管理订单标记为-1
      update dm_order set orderstate  = -1, lastmodifytime = current_timestamp where orderid = NEW.orderid;
    ELSEIF (i_SomeDataNotFinished = 0) THEN 
      -- 如果所有数据均已经处理，不管成功或失败，则i_SomeDataNotFinished为0，则将数据管理订单标记为0;如果是取消的订单，则订单状态就不变了。
      update dm_order set orderstate  = 0, lastmodifytime = current_timestamp where orderid = NEW.orderid and orderstate != 3;
    END IF;
    
*/


ALTER TABLE ro_file
    ADD COLUMN fSHACode character varying(400);
COMMENT ON COLUMN ro_file.fSHACode IS 'SHA码';


-- 更新数据到新的数据表结构中

truncate table ro_file_object;

insert into ro_file_object(foid, fotitle, fogroup)
select fid, ftitle, 1
from ro_file


-------支持v2.0入库模式 
         ALTER TABLE public.dm_index_catalog
   ADD COLUMN dicInstorePriority integer default 0;
COMMENT ON COLUMN public.dm_index_catalog.dicInstorePriority IS '入库优先级';
