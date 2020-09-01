/*
	数据入库、识别
	2019-11-24
	v1.0
	王西亚
	
	。数据库及插件要求
	[x] postgresql 9.4
	[x] postgis
	[x] uuid-ossp
	
	日志：
	。初始版本
		。如果需要进行标签识别，则需要将本文件后半部分的Global表添加。
	。2019-11-24
		。扩展对目录的黑名单支持
		。扩展对文件的黑白名单支持
		。在dm2_storage中增加黑白名单字段，多个过滤使用分号分隔
	。2019-11-24-2
		。发现文件扫描，还不能仅仅通过黑白名单进行管理，还需要增加文件扩展名
    。2020-6-22
        。思考对gdb、mdb等数据集的支持
        。这类数据集，需要将元数据进行进一步解析

    。2020-6-23  王西亚
        。对dm2_storage_object_def进行说明：
            。dsodid  对象标识
            。dsodname    对象名称
            。dsodtitle   对象标题
            。dsodtype    大类
            。dsod_metadata_engine    元数据解析引擎
                。vector
                    。矢量数据的元数据抽取，采用GDAL的ogrInfo元数据解析算法
                。raster
                    。影像数据的元数据抽取，采用GDAL的gdalInfo元数据解析算法
                。picture
                    。采用自有的算法提取图片的Exif信息，暂不使用！！！
                。21at_mbtiles
                    。支持提取21at公司的切片格式
                。bzff
                    。标准分幅的元数据抽取，暂不使用！！！
                。sat
                    。支持对各类卫星元数据的抽取，暂不使用！！！
            。dsod_detail_engine  对象明细提取引擎
                。same_file_mainname
                    。与被识别为对象，在同一个目录下，文件主名都相同的，将作为对象的明细记录
                。file_of_samedir
                    。与被识别为对象，在同一个目录下的文件（不包含子目录），将作为对象的明细记录
                。all_file_of_samedir
                    。与被识别为对象，在同一个目录下的所有文件（包含子目录），将作为对象的明细记录
                。file_of_dir
                    。被识别的对象是子目录，在对象子目录下的文件（不包含子目录），将作为对象的明细记录
                。all_file_of_dir
                    。被识别的对象是子目录，在对象子目录下的所有文件（包含子目录），将作为对象的明细记录
            。dsod_tags_engine    对象标签挂接引擎
                。global_dim
                    。标签根据全局定义的词库，与文件主名匹配
                。global_dim_in_relationname
                    。标签根据全局定义的词库，与文件相对路径名称匹配
            。dsod_ext_whitelist  对象扩展名白名单
                。扩展名白名单，是针对卫星数据进行专用的适配
                。部分卫星数据的关键字，在普通文件数据中也存在，因此，针对卫星数据文件的扩展名进行扩展，只有在白名单中的扩展名列表中的，才被确认为
                    卫星数据
                。多个扩展名，使用分号分隔
            。dsod_browserimg 对象图标
            。dsod_thumbimg   对象缩略图
            。dsod_check_engine_type  对象验证引擎类型
            。dsod_check_engine   对象验证引擎
            。dsod_check_engine_workdir   对象验证引擎工作路径
            。dsod_deploy_engine_type 对象发布引擎类型
            。dsod_deploy_engine  对象发布引擎
            。dsod_deploy_engine_workdir  对象发布引擎工作路径
            。dsodtype_title  大类标题
            。dsod_last_process_engine    对象入库后处理引擎
                。后处理引擎采用的机制，和前面的几个引擎不同
                。考虑到后处理可能有多个动作，后处理引擎采用数组模式
                。metadata_vectordataset_parser
                    。矢量数据集的元数据解析，如对gdb、mdb，系统将自动将gdb中的图层解析出来。

    。2020-6-24
        。部分时间、空间和业务维度下没有数据，建议不生成对应的空图层
    。2020-7-15
        。思考业务数据集的数据管理技术方案
        。业务数据集是根据业务分类规划的一种特殊的数据集，它不同于GDBFile这类技术体系形成的数据集，后者是不可分割的、归属关系明确的数据集
          前者是业务属性定义的，可分割的数据集。在后者中，单个数据仍然有效，且需要独立体现，同时，还需要体现单个数据与数据集之间的所属关系
        。业务数据集对数据的整理有特定要求，每个数据的命名、存储结构、相互的关系，都有标准，本次考虑实现的是：
            。国情影像-整景纠正
            。国情影像-分幅数据
            。三调影像
            。镶嵌影像
        。需要建立一个新的业务模式：
            。在Object_Def表中，对数据类型增加busDataSet，标识业务数据集，这是业务格式规范下的数据集类型
            。将gdb类型对应的vector类型，更改为dataset_vector矢量数据集，这是技术格式规范下的数据集类型
            。业务数据集在解析时，会根据确定命名的Business业务进行匹配识别，如有，则按特定的业务流程进行识别；如没有，则按传统的模式进行识别
        

*/

-- Table: public.dm2_storage

-- DROP TABLE public.dm2_storage;   

CREATE TABLE public.dm2_storage
(
    dstid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsttitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dstunipath character varying(4000) COLLATE pg_catalog."default",
    dstwatch integer,
    dstwatchperiod character varying(50) COLLATE pg_catalog."default",
    dstscanlasttime timestamp(6) without time zone,
    dstscanstatus integer DEFAULT 1,
    dstprocessid character varying(100) COLLATE pg_catalog."default",
    dstaddtime timestamp(6) without time zone DEFAULT now(),
    dstlastmodifytime timestamp(6) without time zone,
    dstmemo character varying(200) COLLATE pg_catalog."default",
    dstwhitelist character varying(1000) COLLATE pg_catalog."default",
    dstblacklist character varying(1000) COLLATE pg_catalog."default",
    dstfileext character varying(1000) COLLATE pg_catalog."default",
    dstotheroption character varying(2000) COLLATE pg_catalog."default",
    CONSTRAINT dm2_storage_pkey PRIMARY KEY (dstid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage
    IS '数管-存储目录';

COMMENT ON COLUMN public.dm2_storage.dstid
    IS '标识，guid';

COMMENT ON COLUMN public.dm2_storage.dsttitle
    IS '数据管理员当前电脑数据目录 Z:\\data';

COMMENT ON COLUMN public.dm2_storage.dstunipath
    IS '网络盘符的ip地址路径\\000.000.000.000\data';

COMMENT ON COLUMN public.dm2_storage.dstwatch
    IS '是否自动监控本目录编号，0：不是  1：是 默认为1';

COMMENT ON COLUMN public.dm2_storage.dstwatchperiod
    IS '监控扫描周期，1.一周；2.一月';

COMMENT ON COLUMN public.dm2_storage.dstscanlasttime
    IS '上次扫描时间';

COMMENT ON COLUMN public.dm2_storage.dstscanstatus
    IS '0：已扫描完毕；1：立刻扫描；2：扫描中';

COMMENT ON COLUMN public.dm2_storage.dstprocessid
    IS '并行处理标识';

COMMENT ON COLUMN public.dm2_storage.dstaddtime
    IS '添加时间';

COMMENT ON COLUMN public.dm2_storage.dstlastmodifytime
    IS '最后修改时间';

COMMENT ON COLUMN public.dm2_storage.dstmemo
    IS '备注';

COMMENT ON COLUMN public.dm2_storage.dstwhitelist
    IS '白名单';

COMMENT ON COLUMN public.dm2_storage.dstblacklist
    IS '黑名单';

COMMENT ON COLUMN public.dm2_storage.dstfileext
    IS '文件扩展名';

COMMENT ON COLUMN public.dm2_storage.dstotheroption
    IS '其他配置';

-- Index: idx_dm2_storage_processid

-- DROP INDEX public.idx_dm2_storage_processid;

CREATE INDEX idx_dm2_storage_processid
    ON public.dm2_storage USING btree
    (dstprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_scanstatus

-- DROP INDEX public.idx_dm2_storage_scanstatus;

CREATE INDEX idx_dm2_storage_scanstatus
    ON public.dm2_storage USING btree
    (dstscanstatus)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_title

-- DROP INDEX public.idx_dm2_storage_title;

CREATE INDEX idx_dm2_storage_title
    ON public.dm2_storage USING btree
    (dsttitle COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_watch

-- DROP INDEX public.idx_dm2_storage_watch;

CREATE INDEX idx_dm2_storage_watch
    ON public.dm2_storage USING btree
    (dstwatch)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_watchperiod

-- DROP INDEX public.idx_dm2_storage_watchperiod;

CREATE INDEX idx_dm2_storage_watchperiod
    ON public.dm2_storage USING btree
    (dstwatchperiod COLLATE pg_catalog."default")
    TABLESPACE pg_default;
    
-- Table: public.dm2_storage_directory

-- DROP TABLE public.dm2_storage_directory;

CREATE TABLE public.dm2_storage_directory
(
    dsdid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsdparentid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsdstorageid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsddirectory character varying(4000) COLLATE pg_catalog."default" NOT NULL,
    dsddirtype character varying(100) COLLATE pg_catalog."default",
    dsdscanstatus integer DEFAULT 1,
    dsdprocessid character varying(100) COLLATE pg_catalog."default",
    dsdaddtime timestamp(6) without time zone DEFAULT now(),
    dsdlastmodifytime timestamp(6) without time zone,
    dsddirectoryname character varying(1000) COLLATE pg_catalog."default",
    dsdmetadata json,
    dsd_object_type character varying(100) COLLATE pg_catalog."default",
    dsd_object_confirm integer DEFAULT 0,
    dsd_object_id character varying(200) COLLATE pg_catalog."default",
    dsd_directory_valid integer DEFAULT '-1'::integer,
    dsdscanfilestatus integer DEFAULT 1,
    dsdscanfileprocessid character varying(100) COLLATE pg_catalog."default",
    dsdscandirstatus integer DEFAULT 1,
    dsdscandirprocessid character varying(100) COLLATE pg_catalog."default",
    dsdpath character varying(4000) COLLATE pg_catalog."default",
    CONSTRAINT dm2_storage_directory_pkey PRIMARY KEY (dsdid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_directory
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_directory
    IS '数管-存储目录-子目录';

COMMENT ON COLUMN public.dm2_storage_directory.dsdid
    IS '标识，guid';

COMMENT ON COLUMN public.dm2_storage_directory.dsdparentid
    IS 'pid父目录编号';

COMMENT ON COLUMN public.dm2_storage_directory.dsdstorageid
    IS '存储盘编号，对应dm2_storage的dstid字段';

COMMENT ON COLUMN public.dm2_storage_directory.dsddirectory
    IS '文件的相对目录路径（不带工作区路径、不带文件名）\\dir1\\dir2\\';

COMMENT ON COLUMN public.dm2_storage_directory.dsddirtype
    IS '文件夹类型：1.普通目录；2.虚拟目录；3.根目录';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscanstatus
    IS '对象识别状态(处理完成是0，待处理是1，处理中是2)';

COMMENT ON COLUMN public.dm2_storage_directory.dsdprocessid
    IS '并行识别对象标识';

COMMENT ON COLUMN public.dm2_storage_directory.dsdaddtime
    IS '添加时间';

COMMENT ON COLUMN public.dm2_storage_directory.dsdlastmodifytime
    IS '最后修改时间';

COMMENT ON COLUMN public.dm2_storage_directory.dsddirectoryname
    IS '目录名称 dir2 ';

COMMENT ON COLUMN public.dm2_storage_directory.dsdmetadata
    IS '元数据图层格式化（gdb\mdb）';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_object_type
    IS '数据对象类型';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_object_confirm
    IS '数据对象识别概率;-1:确认是对象;0:不知道;1:有可能;2:确认不是对象';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_object_id
    IS '数据对象标识';

COMMENT ON COLUMN public.dm2_storage_directory.dsd_directory_valid
    IS '目录是否有效';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscanfilestatus
    IS '并行扫描文件状态(处理完成是0，待处理是1，处理中是2)';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscanfileprocessid
    IS '并行扫描文件进程';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscandirstatus
    IS '并行扫描子目录状态(处理完成是0，待处理是1，处理中是2)';

COMMENT ON COLUMN public.dm2_storage_directory.dsdscandirprocessid
    IS '并行扫描目录进程';

COMMENT ON COLUMN public.dm2_storage_directory.dsdpath
    IS '目录的上级路径';

-- Index: idx_dm2_storage_directory_directoryname

-- DROP INDEX public.idx_dm2_storage_directory_directoryname;

CREATE INDEX idx_dm2_storage_directory_directoryname
    ON public.dm2_storage_directory USING btree
    (dsddirectoryname COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dirtype

-- DROP INDEX public.idx_dm2_storage_directory_dirtype;

CREATE INDEX idx_dm2_storage_directory_dirtype
    ON public.dm2_storage_directory USING btree
    (dsddirtype COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dsddirectory

-- DROP INDEX public.idx_dm2_storage_directory_dsddirectory;

CREATE INDEX idx_dm2_storage_directory_dsddirectory
    ON public.dm2_storage_directory USING btree
    (dsddirectory COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dsdscandirprocessid

-- DROP INDEX public.idx_dm2_storage_directory_dsdscandirprocessid;

CREATE INDEX idx_dm2_storage_directory_dsdscandirprocessid
    ON public.dm2_storage_directory USING btree
    (dsdscandirprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dsdscandirstatus

-- DROP INDEX public.idx_dm2_storage_directory_dsdscandirstatus;

CREATE INDEX idx_dm2_storage_directory_dsdscandirstatus
    ON public.dm2_storage_directory USING btree
    (dsdscandirstatus)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dsdscanfileprocessid

-- DROP INDEX public.idx_dm2_storage_directory_dsdscanfileprocessid;

CREATE INDEX idx_dm2_storage_directory_dsdscanfileprocessid
    ON public.dm2_storage_directory USING btree
    (dsdscanfileprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_dsdscanfilestatus

-- DROP INDEX public.idx_dm2_storage_directory_dsdscanfilestatus;

CREATE INDEX idx_dm2_storage_directory_dsdscanfilestatus
    ON public.dm2_storage_directory USING btree
    (dsdscanfilestatus)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_id

-- DROP INDEX public.idx_dm2_storage_directory_id;

CREATE INDEX idx_dm2_storage_directory_id
    ON public.dm2_storage_directory USING btree
    (dsdid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_parentid

-- DROP INDEX public.idx_dm2_storage_directory_parentid;

CREATE INDEX idx_dm2_storage_directory_parentid
    ON public.dm2_storage_directory USING btree
    (dsdparentid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_processid

-- DROP INDEX public.idx_dm2_storage_directory_processid;

CREATE INDEX idx_dm2_storage_directory_processid
    ON public.dm2_storage_directory USING btree
    (dsdprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_scanfileprocessid

-- DROP INDEX public.idx_dm2_storage_directory_scanfileprocessid;

CREATE INDEX idx_dm2_storage_directory_scanfileprocessid
    ON public.dm2_storage_directory USING btree
    (dsdscanfileprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_directory_scanstatus

-- DROP INDEX public.idx_dm2_storage_directory_scanstatus;

CREATE INDEX idx_dm2_storage_directory_scanstatus
    ON public.dm2_storage_directory USING btree
    (dsdscanstatus)
    TABLESPACE pg_default;
    
-- Table: public.dm2_storage_file

-- DROP TABLE public.dm2_storage_file;

CREATE TABLE public.dm2_storage_file
(
    dsfid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsfstorageid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsfdirectoryid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsffilerelationname character varying(4000) COLLATE pg_catalog."default",
    dsffilename character varying(1000) COLLATE pg_catalog."default",
    dsffilemainname character varying(1000) COLLATE pg_catalog."default",
    dsfext character varying(100) COLLATE pg_catalog."default",
    dsffilecreatetime timestamp(6) without time zone,
    dsffilemodifytime timestamp(6) without time zone,
    dsfaddtime timestamp(6) without time zone DEFAULT now(),
    dsflastmodifytime timestamp(6) without time zone,
    dsffilevalid integer DEFAULT '-1'::integer,
    dsfscanstatus integer DEFAULT 1,
    dsfprocessid character varying(100) COLLATE pg_catalog."default",
    dsf_object_type character varying(100) COLLATE pg_catalog."default",
    dsf_object_confirm integer DEFAULT 0,
    dsf_object_id character varying(200) COLLATE pg_catalog."default",
    dsffileattr integer DEFAULT 0,
    dsffilesize bigint DEFAULT 0,
    CONSTRAINT dm2_storage_file_pkey PRIMARY KEY (dsfid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_file
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_file
    IS '数管-存储目录-文件';

COMMENT ON COLUMN public.dm2_storage_file.dsfid
    IS '标识，guid';

COMMENT ON COLUMN public.dm2_storage_file.dsfstorageid
    IS '存储盘编号';

COMMENT ON COLUMN public.dm2_storage_file.dsfdirectoryid
    IS '文件的目录标识';

COMMENT ON COLUMN public.dm2_storage_file.dsffilerelationname
    IS '文件相对名称';

COMMENT ON COLUMN public.dm2_storage_file.dsffilename
    IS '文件名称，无路径，含扩展名';

COMMENT ON COLUMN public.dm2_storage_file.dsffilemainname
    IS '文件主名，无扩展名';

COMMENT ON COLUMN public.dm2_storage_file.dsfext
    IS '扩展名，无点';

COMMENT ON COLUMN public.dm2_storage_file.dsffilecreatetime
    IS '文件创建时间';

COMMENT ON COLUMN public.dm2_storage_file.dsffilemodifytime
    IS '文件最后修改时间';

COMMENT ON COLUMN public.dm2_storage_file.dsfaddtime
    IS '记录添加时间';

COMMENT ON COLUMN public.dm2_storage_file.dsflastmodifytime
    IS '记录最后刷新时间';

COMMENT ON COLUMN public.dm2_storage_file.dsffilevalid
    IS '文件是否有效';

COMMENT ON COLUMN public.dm2_storage_file.dsfscanstatus
    IS '对象识别状态(处理完成是0，待处理是1，处理中是2)';

COMMENT ON COLUMN public.dm2_storage_file.dsfprocessid
    IS '并行处理标识';

COMMENT ON COLUMN public.dm2_storage_file.dsf_object_type
    IS '数据对象类型';

COMMENT ON COLUMN public.dm2_storage_file.dsf_object_confirm
    IS '数据对象识别概率;-1:确认是对象;0:不知道;1:有可能;2:确认不是对象';

COMMENT ON COLUMN public.dm2_storage_file.dsf_object_id
    IS '数据对象标识';

COMMENT ON COLUMN public.dm2_storage_file.dsffileattr
    IS '文件属性';

COMMENT ON COLUMN public.dm2_storage_file.dsffilesize
    IS '文件大小';

-- Index: idx_dm2_storage_file_dsf_object_type

-- DROP INDEX public.idx_dm2_storage_file_dsf_object_type;

CREATE INDEX idx_dm2_storage_file_dsf_object_type
    ON public.dm2_storage_file USING btree
    (dsf_object_type COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_file_dsfdirectoryid

-- DROP INDEX public.idx_dm2_storage_file_dsfdirectoryid;

CREATE INDEX idx_dm2_storage_file_dsfdirectoryid
    ON public.dm2_storage_file USING btree
    (dsfdirectoryid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_file_dsfstorageid

-- DROP INDEX public.idx_dm2_storage_file_dsfstorageid;

CREATE INDEX idx_dm2_storage_file_dsfstorageid
    ON public.dm2_storage_file USING btree
    (dsfstorageid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_file_processid

-- DROP INDEX public.idx_dm2_storage_file_processid;

CREATE INDEX idx_dm2_storage_file_processid
    ON public.dm2_storage_file USING btree
    (dsfprocessid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_file_scanstatus

-- DROP INDEX public.idx_dm2_storage_file_scanstatus;

CREATE INDEX idx_dm2_storage_file_scanstatus
    ON public.dm2_storage_file USING btree
    (dsfscanstatus)
    TABLESPACE pg_default;
    
-- Table: public.dm2_storage_obj_detail

-- DROP TABLE public.dm2_storage_obj_detail;

CREATE TABLE public.dm2_storage_obj_detail
(
    dodid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dodobjectid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dodfilename character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    dodfileext character varying(100) COLLATE pg_catalog."default",
    dodfilesize bigint DEFAULT 0,
    dodfileattr integer DEFAULT 0,
    dodfilecreatetime timestamp(6) without time zone,
    dodfilemodifytime timestamp(6) without time zone,
    dodlastmodifytime timestamp(6) without time zone DEFAULT now(),
    CONSTRAINT dm2_storage_obj_detail_pkey PRIMARY KEY (dodid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_obj_detail
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_obj_detail
    IS '数管-存储文件';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodid
    IS '标识guid';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodobjectid
    IS '外键，关联dm2_storage_object表中的oid字段';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfilename
    IS '文件名带扩展名 aaa.img';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfileext
    IS '文件扩展名, 带前缀点 .img';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfilesize
    IS '大小';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfileattr
    IS '属性';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfilecreatetime
    IS '文件的创建时间';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodfilemodifytime
    IS '文件的修改时间';

COMMENT ON COLUMN public.dm2_storage_obj_detail.dodlastmodifytime
    IS '记录的最后修改时间';
    
-- Table: public.dm2_storage_object

-- DROP TABLE public.dm2_storage_object;

CREATE TABLE public.dm2_storage_object
(
    dsoid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsoobjectname character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    dsoobjecttype character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsodatatype character varying(100) COLLATE pg_catalog."default",
    dsometadatatext text COLLATE pg_catalog."default",
    dsometadatajson jsonb,
    dsometadatajson_bus jsonb,
    dsometadataxml xml,
    dsometadatatype integer DEFAULT 0,
    dsometadataparsestatus integer DEFAULT 1,
    dsometadataparseprocid character varying(100) COLLATE pg_catalog."default",
    dsotags character varying[] COLLATE pg_catalog."default",
    dsolastmodifytime timestamp(6) without time zone,
    dsometadataparsememo text COLLATE pg_catalog."default",
    dsodetailparsememo text COLLATE pg_catalog."default",
    dsodetailparsestatus integer DEFAULT 1,
    dsodetailparseprocid character varying(100) COLLATE pg_catalog."default",
    dsotagsparsememo text COLLATE pg_catalog."default",
    dsotagsparsestatus integer DEFAULT 1,
    dsotagsparseprocid character varying(100) COLLATE pg_catalog."default",
    dsoalphacode character varying(100) COLLATE pg_catalog."default",
    dsoaliasname character varying(1000) COLLATE pg_catalog."default",
    CONSTRAINT dm2_storage_object_pkey PRIMARY KEY (dsoid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_object
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_object
    IS '数管-存储目录-对象';

COMMENT ON COLUMN public.dm2_storage_object.dsoid
    IS '标识';

COMMENT ON COLUMN public.dm2_storage_object.dsoobjectname
    IS '对象名称';

COMMENT ON COLUMN public.dm2_storage_object.dsoobjecttype
    IS '对象类型';

COMMENT ON COLUMN public.dm2_storage_object.dsodatatype
    IS '数据类型:dir-目录;file-文件';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatext
    IS '元数据text';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatajson
    IS '元数据json';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatajson_bus
    IS '业务元数据Json';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataxml
    IS '元数据xml';

COMMENT ON COLUMN public.dm2_storage_object.dsometadatatype
    IS '元数据类型;0-txt;1-json;2-xml';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparsestatus
    IS '元数据提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparseprocid
    IS '元数据提取进程标识';

COMMENT ON COLUMN public.dm2_storage_object.dsotags
    IS '标签';

COMMENT ON COLUMN public.dm2_storage_object.dsolastmodifytime
    IS '记录最后刷新时间';

COMMENT ON COLUMN public.dm2_storage_object.dsometadataparsememo
    IS '元数据提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparsememo
    IS '明细提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparsestatus
    IS '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dsodetailparseprocid
    IS '明细提取标识';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparsememo
    IS '明细提取说明';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparsestatus
    IS '明细提取状态;0-完成;1-待提取;2-提取中;3-提取有误';

COMMENT ON COLUMN public.dm2_storage_object.dsotagsparseprocid
    IS '明细提取标识';

COMMENT ON COLUMN public.dm2_storage_object.dsoalphacode
    IS '拼音';

COMMENT ON COLUMN public.dm2_storage_object.dsoaliasname
    IS '别名';

-- Index: idx_dm2_storage_object_id

-- DROP INDEX public.idx_dm2_storage_object_id;

CREATE INDEX idx_dm2_storage_object_id
    ON public.dm2_storage_object USING btree
    (dsoid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_json

-- DROP INDEX public.idx_dm2_storage_object_json;

CREATE INDEX idx_dm2_storage_object_json
    ON public.dm2_storage_object USING gin
    (dsometadatajson)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_json_bus

-- DROP INDEX public.idx_dm2_storage_object_json_bus;

CREATE INDEX idx_dm2_storage_object_json_bus
    ON public.dm2_storage_object USING gin
    (dsometadatajson_bus)
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_objecttype

-- DROP INDEX public.idx_dm2_storage_object_objecttype;

CREATE INDEX idx_dm2_storage_object_objecttype
    ON public.dm2_storage_object USING btree
    (dsoobjecttype COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_tag

-- DROP INDEX public.idx_dm2_storage_object_tag;

CREATE INDEX idx_dm2_storage_object_tag
    ON public.dm2_storage_object USING gin
    (dsotags COLLATE pg_catalog."default")
    TABLESPACE pg_default;
    
-- Table: public.dm2_storage_object_def

-- DROP TABLE public.dm2_storage_object_def;

CREATE TABLE public.dm2_storage_object_def
(
    dsodid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsodname character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsodtitle character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    dsodtype character varying(100) COLLATE pg_catalog."default",
    dsodtype_map character varying(100) COLLATE pg_catalog."default",
    dsodname_map character varying(100) COLLATE pg_catalog."default",
    dsodtitle_map character varying(1000) COLLATE pg_catalog."default",
    dsod_metadata_engine character varying(100) COLLATE pg_catalog."default",
    dsod_detail_engine character varying(100) COLLATE pg_catalog."default",
    dsod_tags_engine character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT dm2_storage_object_def_pkey PRIMARY KEY (dsodid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_object_def
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_object_def
    IS '数管-存储目录-对象-定义';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodid
    IS '对象标识';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodname
    IS '对象名称';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtitle
    IS '对象标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtype
    IS '对象类型';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtype_map
    IS '对象类型-映射';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodname_map
    IS '对象名称-映射';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtitle_map
    IS '对象标题-映射';

COMMENT ON COLUMN public.dm2_storage_object_def.dsod_metadata_engine
    IS '元数据解析引擎';

COMMENT ON COLUMN public.dm2_storage_object_def.dsod_detail_engine
    IS '对象明细提取引擎';

COMMENT ON COLUMN public.dm2_storage_object_def.dsod_tags_engine
    IS '对象标签挂接引擎';

-- Index: idx_dm2_storage_object_def_id

-- DROP INDEX public.idx_dm2_storage_object_def_id;

CREATE INDEX idx_dm2_storage_object_def_id
    ON public.dm2_storage_object_def USING btree
    (dsodid COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_def_name

-- DROP INDEX public.idx_dm2_storage_object_def_name;

CREATE INDEX idx_dm2_storage_object_def_name
    ON public.dm2_storage_object_def USING btree
    (dsodname COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_def_name_map

-- DROP INDEX public.idx_dm2_storage_object_def_name_map;

CREATE INDEX idx_dm2_storage_object_def_name_map
    ON public.dm2_storage_object_def USING btree
    (dsodname_map COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_def_type

-- DROP INDEX public.idx_dm2_storage_object_def_type;

CREATE INDEX idx_dm2_storage_object_def_type
    ON public.dm2_storage_object_def USING btree
    (dsodtype COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_dm2_storage_object_def_type_map

-- DROP INDEX public.idx_dm2_storage_object_def_type_map;

CREATE INDEX idx_dm2_storage_object_def_type_map
    ON public.dm2_storage_object_def USING btree
    (dsodtype_map COLLATE pg_catalog."default")
    TABLESPACE pg_default;
  
  
    
/*
	全局关键字表

*/

-- Table: public.ro_global_dim_custom

-- DROP TABLE public.ro_global_dim_custom;

CREATE TABLE public.ro_global_dim_custom
(
    gdcid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    gdctitle character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    gdcparentid character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT '-1'::character varying,
    gdctreecode character varying(2000) COLLATE pg_catalog."default" NOT NULL,
    gdcisgroup bigint NOT NULL DEFAULT 0,
    gdctreeindex bigint NOT NULL DEFAULT 0,
    gdctreelevel bigint NOT NULL DEFAULT 0,
    gdcsysdimid character varying(100) COLLATE pg_catalog."default",
    gdcsysdimtype bigint DEFAULT 3,
    gdcsysdimcount bigint DEFAULT 1,
    gdcsysdimrecursive character varying(1) COLLATE pg_catalog."default",
    CONSTRAINT "ro_global_dim_custom_PK" PRIMARY KEY (gdcid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ro_global_dim_custom
    OWNER to postgres;

COMMENT ON COLUMN public.ro_global_dim_custom.gdcid
    IS '业务维度id';

COMMENT ON COLUMN public.ro_global_dim_custom.gdctitle
    IS '业务维度标题';

COMMENT ON COLUMN public.ro_global_dim_custom.gdcparentid
    IS '业务维度父级id';

COMMENT ON COLUMN public.ro_global_dim_custom.gdctreecode
    IS '业务维度编码';

COMMENT ON COLUMN public.ro_global_dim_custom.gdcisgroup
    IS '是否组';

COMMENT ON COLUMN public.ro_global_dim_custom.gdctreeindex
    IS '树序号';

COMMENT ON COLUMN public.ro_global_dim_custom.gdctreelevel
    IS '树级别';
    
-- Table: public.ro_global_dim_custom_bus

-- DROP TABLE public.ro_global_dim_custom_bus;

CREATE TABLE public.ro_global_dim_custom_bus
(
    gdcbid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    gdcbtype character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT '3'::character varying,
    gdcbtitle character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    gdcbparentid character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT '-1'::character varying,
    gdcbtreecode character varying(2000) COLLATE pg_catalog."default" NOT NULL,
    gdcbisgroup bigint NOT NULL DEFAULT 0,
    gdcbtreeindex bigint NOT NULL DEFAULT 0,
    gdcbtreelevel bigint NOT NULL DEFAULT 0,
    gdcbsysdimid character varying(100) COLLATE pg_catalog."default",
    gdcbsysdimtype bigint DEFAULT 3,
    gdcbsysdimcount bigint DEFAULT 1,
    gdcbsysdimrecursive character varying(1) COLLATE pg_catalog."default",
    gdcbimageindex bigint,
    gdcbpublishjsontemplate text COLLATE pg_catalog."default",
    gdcbpublishrestype character varying(50) COLLATE pg_catalog."default",
    gdcbpublishrestitle character varying(200) COLLATE pg_catalog."default",
    gdcbpublishresexttemplate text COLLATE pg_catalog."default",
    gdcbpublishlabeltemplate character varying(200) COLLATE pg_catalog."default",
    gdcbpublishclassictemplate character varying(200) COLLATE pg_catalog."default",
    gdcbpublishgeometrytemplate character varying(200) COLLATE pg_catalog."default",
    gdcbpublishprojecttemplate character varying(200) COLLATE pg_catalog."default",
    gdcbpublishsridtemplate character varying(200) COLLATE pg_catalog."default",
    gdcbresfilepathtemplate character varying(2000) COLLATE pg_catalog."default",
    dm_deploy_enable integer DEFAULT '-1'::integer,
    dm_enable integer DEFAULT '-1'::integer,
    dm_deploy_dbserverid character varying(200) COLLATE pg_catalog."default" DEFAULT '-1'::character varying,
    gdcbpublishcodetemplate character varying(200) COLLATE pg_catalog."default",
    gdcb_filter_xz integer DEFAULT 0,
    gdcb_filter_gh integer DEFAULT 0,
    gdcb_filter_dw integer DEFAULT 0,
    gdcbname character varying(20) COLLATE pg_catalog."default",
    gdcbquickcode character varying(100) COLLATE pg_catalog."default",
    gdcb_rulexml text COLLATE pg_catalog."default",
    gdcb_isreserved integer DEFAULT '-1'::integer,
    CONSTRAINT "ro_global_dim_custom_bus_PK" PRIMARY KEY (gdcbid, gdcbtype)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ro_global_dim_custom_bus
    OWNER to postgres;

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbid
    IS '业务维度id';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbtype
    IS '业务维度类型';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbtitle
    IS '业务维度标题';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbparentid
    IS '业务维度父级id';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbtreecode
    IS '业务维度编码';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbisgroup
    IS '是否组';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbtreeindex
    IS '树序号';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbtreelevel
    IS '树级别';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbimageindex
    IS '图标索引';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishjsontemplate
    IS '发布Json模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishrestype
    IS '发布资源类型';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishrestitle
    IS '发布资源标题';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishresexttemplate
    IS '扩展信息模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishlabeltemplate
    IS '标签值模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishclassictemplate
    IS '分级渲染值模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishgeometrytemplate
    IS '空间几何对象模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishprojecttemplate
    IS '投影坐标模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishsridtemplate
    IS '坐标系模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbresfilepathtemplate
    IS '资源文件发布模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.dm_deploy_dbserverid
    IS '数据记录发布的目标数据库标识';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbpublishcodetemplate
    IS '编码模板';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcb_filter_xz
    IS '过滤-现状';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcb_filter_gh
    IS '过滤-规划';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcb_filter_dw
    IS '过滤-定位';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbname
    IS '业务维度英文名称';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcbquickcode
    IS '快捷码';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcb_rulexml
    IS '检查字段集，存储rule.xml中的字段信息';

COMMENT ON COLUMN public.ro_global_dim_custom_bus.gdcb_isreserved
    IS '系统保留';
    
-- Table: public.ro_global_dim_space

-- DROP TABLE public.ro_global_dim_space;

CREATE TABLE public.ro_global_dim_space
(
    gdsid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    gdstitle character varying(1000) COLLATE pg_catalog."default",
    gdsparentid character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT '-1  '::character varying,
    gdsisgroup bigint NOT NULL DEFAULT 0,
    gdstreecode character varying(1000) COLLATE pg_catalog."default",
    gdstreeindex bigint NOT NULL DEFAULT 0,
    gdstreelevel bigint NOT NULL DEFAULT 0,
    leftx character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    rightx character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    topy character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    bottomy character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    centerx character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    centery character varying(50) COLLATE pg_catalog."default" DEFAULT '0.000000000000000 '::character varying,
    gdsgeometry geometry,
    gdscode character varying(100) COLLATE pg_catalog."default",
    is_dm_dimension integer DEFAULT 1,
    instancetypes character varying(50)[] COLLATE pg_catalog."default",
    gdsdeployftpserver character varying(100) COLLATE pg_catalog."default",
    gdsdeployusername character varying(100) COLLATE pg_catalog."default",
    gdsdeploypassword character varying(100) COLLATE pg_catalog."default",
    gdsdeployservertype character varying(100) COLLATE pg_catalog."default" DEFAULT 'none'::character varying,
    gdsquickcode character varying(100) COLLATE pg_catalog."default",
    gdsdatasourcesrid character varying(100) COLLATE pg_catalog."default",
    dm_deploy_dbserverid character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT ro_global_dim_space_pkey PRIMARY KEY (gdsid),
    CONSTRAINT index_gdsquickcode UNIQUE (gdsquickcode)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ro_global_dim_space
    OWNER to postgres;
COMMENT ON TABLE public.ro_global_dim_space
    IS '全局配置空间维度';

COMMENT ON COLUMN public.ro_global_dim_space.gdsid
    IS '空间维度id';

COMMENT ON COLUMN public.ro_global_dim_space.gdstitle
    IS '空间维度标题';

COMMENT ON COLUMN public.ro_global_dim_space.gdsparentid
    IS '空间维度父级id';

COMMENT ON COLUMN public.ro_global_dim_space.gdsisgroup
    IS '是否组';

COMMENT ON COLUMN public.ro_global_dim_space.gdstreecode
    IS '空间维度编码';

COMMENT ON COLUMN public.ro_global_dim_space.gdstreeindex
    IS '序号';

COMMENT ON COLUMN public.ro_global_dim_space.gdstreelevel
    IS '区划级别，gdstreelevel::varchar 对应app_audit_busi_dict中dicttype=regionlevel的字典';

COMMENT ON COLUMN public.ro_global_dim_space.leftx
    IS '左x坐标';

COMMENT ON COLUMN public.ro_global_dim_space.rightx
    IS '右x坐标';

COMMENT ON COLUMN public.ro_global_dim_space.topy
    IS '上y坐标';

COMMENT ON COLUMN public.ro_global_dim_space.bottomy
    IS '下y坐标';

COMMENT ON COLUMN public.ro_global_dim_space.centerx
    IS '中心点x';

COMMENT ON COLUMN public.ro_global_dim_space.centery
    IS '中心点y';

COMMENT ON COLUMN public.ro_global_dim_space.gdsgeometry
    IS '空间字段';

COMMENT ON COLUMN public.ro_global_dim_space.gdscode
    IS '空间维度编码';

COMMENT ON COLUMN public.ro_global_dim_space.is_dm_dimension
    IS '数管-可用性; -1-是；0-否';

COMMENT ON COLUMN public.ro_global_dim_space.instancetypes
    IS '涉及到的时间相关场景，如疑点、数管等，关联app_audit_busi_dict中dicttype=spatialinstance的dictcode';

COMMENT ON COLUMN public.ro_global_dim_space.gdsdeployftpserver
    IS '资源文件发布服务器';

COMMENT ON COLUMN public.ro_global_dim_space.gdsdeployusername
    IS '资源文件发布用户名';

COMMENT ON COLUMN public.ro_global_dim_space.gdsdeploypassword
    IS '资源文件发布密码';

COMMENT ON COLUMN public.ro_global_dim_space.gdsdeployservertype
    IS '发布服务器类型none-ftp-dir';

COMMENT ON COLUMN public.ro_global_dim_space.gdsquickcode
    IS '快捷码';

COMMENT ON COLUMN public.ro_global_dim_space.gdsdatasourcesrid
    IS '源数据投影坐标srid';

COMMENT ON COLUMN public.ro_global_dim_space.dm_deploy_dbserverid
    IS '数据发布的目标数据库服务器标识';

-- Index: index_ro_global_dim_space_gdscode

-- DROP INDEX public.index_ro_global_dim_space_gdscode;

CREATE INDEX index_ro_global_dim_space_gdscode
    ON public.ro_global_dim_space USING btree
    (gdscode COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: index_ro_global_dim_space_gdsid

-- DROP INDEX public.index_ro_global_dim_space_gdsid;

CREATE INDEX index_ro_global_dim_space_gdsid
    ON public.ro_global_dim_space USING btree
    (gdsid COLLATE pg_catalog."default")
    TABLESPACE pg_default;
    
    
-- Table: public.ro_global_dim_time

-- DROP TABLE public.ro_global_dim_time;

CREATE TABLE public.ro_global_dim_time
(
    gdtid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    gdttitle character varying(1000) COLLATE pg_catalog."default",
    gdtparentid character varying(100) COLLATE pg_catalog."default" NOT NULL DEFAULT '-1'::character varying,
    gdtisgroup bigint NOT NULL DEFAULT 0,
    gdttreecode character varying(2000) COLLATE pg_catalog."default",
    gdttreeindex bigint NOT NULL DEFAULT 0,
    gdttreelevel bigint NOT NULL DEFAULT 0,
    gdtdatetime timestamp with time zone,
    gdtyear bigint,
    gdtseason bigint,
    gdtmonth bigint,
    gdtday bigint,
    gdttype character varying(50) COLLATE pg_catalog."default",
    instancetypes character varying(50)[] COLLATE pg_catalog."default",
    starttime timestamp without time zone,
    endtime timestamp without time zone,
    is_dm_dimension integer DEFAULT 0,
    gdtquickcode character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT "ro_global_dim_time_PK" PRIMARY KEY (gdtid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ro_global_dim_time
    OWNER to postgres;

COMMENT ON COLUMN public.ro_global_dim_time.gdtid
    IS '时间维度id';

COMMENT ON COLUMN public.ro_global_dim_time.gdttitle
    IS '时间维度标题';

COMMENT ON COLUMN public.ro_global_dim_time.gdtparentid
    IS '时间维度父级id';

COMMENT ON COLUMN public.ro_global_dim_time.gdtisgroup
    IS '是否组';

COMMENT ON COLUMN public.ro_global_dim_time.gdttreecode
    IS '时间维度编码';

COMMENT ON COLUMN public.ro_global_dim_time.gdttreeindex
    IS '序号';

COMMENT ON COLUMN public.ro_global_dim_time.gdttreelevel
    IS '级别';

COMMENT ON COLUMN public.ro_global_dim_time.gdtdatetime
    IS '时间';

COMMENT ON COLUMN public.ro_global_dim_time.gdtyear
    IS '年份';

COMMENT ON COLUMN public.ro_global_dim_time.gdtseason
    IS '季度';

COMMENT ON COLUMN public.ro_global_dim_time.gdtmonth
    IS '月度';

COMMENT ON COLUMN public.ro_global_dim_time.gdtday
    IS '天';

COMMENT ON COLUMN public.ro_global_dim_time.gdttype
    IS '时间维度类型，年度、季度、月度、日。关联app_audit_busi_dict中dicttype = gdttype的dictcode';

COMMENT ON COLUMN public.ro_global_dim_time.instancetypes
    IS '涉及到的时间相关场景，如疑点、数管、土地利用现状等，关联app_audit_busi_dict中dicttype=timeinstance的dictcode';

COMMENT ON COLUMN public.ro_global_dim_time.starttime
    IS '输入时间值的左区间';

COMMENT ON COLUMN public.ro_global_dim_time.endtime
    IS '输入时间值的右区间';

COMMENT ON COLUMN public.ro_global_dim_time.is_dm_dimension
    IS '数管可用性：-1：是，0：否';

COMMENT ON COLUMN public.ro_global_dim_time.gdtquickcode
    IS '快捷码';
    


/*
	初始化数据
	
*/

INSERT INTO public.dm2_storage_object_def VALUES ('gdb', 'gdb', 'gdb数据集', '矢量数据集', '矢量数据集', 'gdb', 'gdb数据集', 'vector', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('pix', 'pix', 'PIX影像', '遥感影像', '遥感影像', 'pix', 'PIX影像', 'raster', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('tiff', 'tiff', 'TIFF影像', '遥感影像', '遥感影像', 'tiff', 'TIFF影像', 'raster', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('tif', 'tif', 'TIF影像', '遥感影像', '遥感影像', 'tif', 'TIF影像', 'raster', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('docx', 'docx', 'Word2017', '文档', '文档', 'docx', 'Word2017', 'word', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('doc', 'doc', 'Word2013', '文档', '文档', 'doc', 'Word2013', 'word', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('xls', 'xls', 'Excel2013', '文档', '文档', 'xls', 'Excel2013', 'excel', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('xlsx', 'xlsx', 'Excel2017', '文档', '文档', 'xlsx', 'Excel2017', 'excel', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('bzff', 'bzff', '标准分幅', '生产成果数据', '生产成果数据', 'bzff', '标准分幅', 'bzff', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('21at_mbtiles', '21at_mbtiles', '二十一世纪公司切片', '服务数据', '服务数据', '21at_mbtiles', '二十一世纪公司切片', '21at_mbtiles', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('jpg', 'jpg', 'JPG图片', '图片', '图片', 'jpg', 'JPG图片', 'picture', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('png', 'png', 'PNG图片', '图片', '图片', 'png', 'PNG图片', 'picture', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('bmp', 'bmp', 'BMP图片', '图片', '图片', 'bmp', 'BMP图片', 'picture', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('gif', 'gif', 'GIF图片', '图片', '图片', 'gif', 'GIF图片', 'picture', NULL, 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('img', 'img', 'IMG影像', '遥感影像', '遥感影像', 'img', 'IMG影像', 'raster', 'same_file_mainname', 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('shp', 'shp', 'SHP矢量', '矢量', '矢量', 'shp', 'SHP矢量', 'vector', 'same_file_mainname', 'global_dim');
INSERT INTO public.dm2_storage_object_def VALUES ('bj2', 'bj2', '北京二号', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('cb04', 'cb04', '中巴地球资源卫星04星', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('de2', 'de2', 'DEIMOS-2', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy302', 'zy3-zy302', '资源一号01/02星-ZY302', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('hj', 'hj', '环境一号A/B/C星', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('jl1', 'jl1', '吉林一号', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('k2', 'k2', 'Kompsat-2', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('k3', 'k3', 'Kompsat-3', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('pl', 'pl', 'Pleiades1A/1B', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('rapideye', 'rapideye', 'RapidEye', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('spot', 'spot', 'SPOT', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('sv1', 'sv1', '高景一号', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('wv', 'wv', 'WordView01/02/03', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('yg', 'yg', '遥感卫星', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf1-pms', 'gf1-pms', '高分一号-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf1-wfv', 'gf1-wfv', '高分一号-WFV', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf2-pms', 'gf2-pms', '高分二号-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf2-wfv', 'gf2-wfv', '高分二号-WFV', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-hh', 'gf3-hh', '高分三号-HH', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-vhvv', 'gf3-vhvv', '高分三号-VHVV', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-dh', 'gf3-dh', '高分三号-DH', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-pms', 'gf4-pms', '高分四号-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-b1', 'gf4-b1', '高分四号-B1', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-pmi', 'gf4-pmi', '高分四号-PMI', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-irs', 'gf4-irs', '高分四号-IRS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-ahsi', 'gf5-ahsi', '高分五号-AHSI', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-vims', 'gf5-vims', '高分五号-VIMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-gmi', 'gf5-gmi', '高分五号-GMI', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-emi', 'gf5-emi', '高分五号-EMI', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf6-pms', 'gf6-pms', '高分六号-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('gf6-wfv', 'gf6-wfv', '高分六号-WFV', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('landsat-ld8', 'landsat-ld8', 'LandSat-ld8', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('landsat-le7', 'landsat-le7', 'LandSat-le7', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('sj9a-pmn', 'sj9a-pmn', '实践九号-PMN', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('sj9a-pms', 'sj9a-pms', '实践九号-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('th-th', 'th-th', '天绘一号-th', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('th-th01', 'th-th01', '天绘一号-th01', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy02c-pms', 'zy02c-pms', '资源三号02星-PMS', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy02c-hrc', 'zy02c-hrc', '资源三号02星-HRC', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy3', 'zy3-zy3', '资源一号01/02星-ZY3', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy3_01a', 'zy3-zy3_01a', '资源一号01/02星-ZY3_01a', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy301a', 'zy3-zy301a', '资源一号01/02星-zy301a', '卫星数据', NULL, NULL, NULL, NULL, NULL, NULL);


/*
	样例数据
	
*/

INSERT INTO public.dm2_storage VALUES ('1', 'C:\Data\产品样例数据-昆明矢量', 'C:\Data\产品样例数据-昆明矢量', 0, '1', NULL, 0, 'v49d4ffc5d4ed4e13bc97151d365b8ca6', '2019-10-17 18:58:30.36528', NULL, NULL, '*行业业务数据*', '*专题分析数据*;*土地资源专项*', NULL);



/*
    为解决目录量大，界面反复发送扫描目录的命令，使得一个大目录反复被扫描的问题：
    一、扫描子目录
    1.将界面扫描处理，从原来的递归扫描，改为当前目录扫描，具体逻辑如下：
      1.1.当用户从界面发送扫描命令时，系统做如下处理：
        1.1.1.仅仅扫描当前目录下的文件
        1.1.2.扫描当前目录在的子目录
          1.1.2.1.是新增的子目录，则对新增子目录递归扫描
          1.1.2.2.是已经存在的子目录：
            1.1.2.2.1.如果最后修改日期变化了，则对变化的子目录递归扫描
            1.1.2.2.2.如果子目录的信息没有变化，则不对子目录进行扫描
      1.2.每次用户从界面发送扫描命令时，子目录的扫描优先级将递增
      1.3.用户从界面发送的扫描命令，dsdScanDirStatus将使用专用状态标志
        1.3.1.=0，表示扫描完毕
        1.3.2.=1，表示请求扫描
        1.3.3.=2，表示在扫描中
    2.根目录的扫描，将使用最低优先级
      2.1.根目录扫描调度，dsdScanDirStatus将使用特定状态标识
        2.1.1.=0，表示扫描完毕
        2.1.2.=11，表示请求递归扫描
        2.1.3.=12，表示在递归扫描中
*/

alter table dm2_storage_directory add column dsdDirCreateTime timestamp(6) without time zone;
COMMENT ON COLUMN public.dm2_storage_directory.dsdDirCreateTime
    IS '目录创建时间';

alter table dm2_storage_directory add column dsdDirLastModifyTime timestamp(6) without time zone;
COMMENT ON COLUMN public.dm2_storage_directory.dsdDirLastModifyTime
    IS '目录最后修改时间';

alter table dm2_storage_directory add column dsdDirScanPriority integer default 0;
COMMENT ON COLUMN public.dm2_storage_directory.dsdDirScanPriority
    IS '目录扫描优先级';

update dm2_storage_directory set dsdDirScanPriority = 0;



/*
	2019-12-12 王西亚
  1、为文件扫描增加扩展名白名单功能，以解决部分文件携带卫星数据中的关键字，而被误认为是卫星数据的问题
*/

alter table dm2_storage_object_def add column dsod_ext_whitelist character varying(1000);
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_ext_whitelist IS '对象扩展名白名单';


/*
	2020-5-9合并dm2_storage_object_def和dm2_index_catalog
*/

alter table dm2_storage_object_def add column dsod_BrowserImg character varying(300);
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_BrowserImg IS '对象图标';

alter table dm2_storage_object_def add column dsod_ThumbImg character varying(300);
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_ThumbImg IS '对象缩略图';

alter table dm2_storage_object_def add column dsod_Check_Engine_Type character varying(100);
alter table dm2_storage_object_def add column dsod_Check_Engine character varying(2000);
alter table dm2_storage_object_def add column dsod_Check_Engine_WorkDir character varying(2000);
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Check_Engine_Type IS '对象验证引擎类型';
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Check_Engine IS '对象验证引擎';
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Check_Engine_WorkDir IS '对象验证引擎工作路径';

alter table dm2_storage_object_def add column dsod_Deploy_Engine_Type character varying(100);
alter table dm2_storage_object_def add column dsod_Deploy_Engine character varying(2000);
alter table dm2_storage_object_def add column dsod_Deploy_Engine_WorkDir character varying(2000);
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Deploy_Engine_Type IS '对象发布引擎类型';
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Deploy_Engine IS '对象发布引擎';
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_Deploy_Engine_WorkDir IS '对象发布引擎工作路径';

update dm2_storage_object_def 
set dsod_Check_Engine_Type = 'inner', dsod_Check_Engine = 'shp', dsod_Check_Engine_WorkDir = null 
  , dsod_Deploy_Engine_Type = 'inner', dsod_Deploy_Engine = 'shp', dsod_Deploy_Engine_WorkDir = null 
  , dsod_BrowserImg = 'vector_96x96.png', dsod_ThumbImg = 'vector_32x32.png'
where dsodid = 'shp';

update dm2_storage_object_def 
set dsod_Check_Engine_Type = 'inner', dsod_Check_Engine = 'excel', dsod_Check_Engine_WorkDir = null 
  , dsod_Deploy_Engine_Type = 'inner', dsod_Deploy_Engine = 'excel', dsod_Deploy_Engine_WorkDir = null 
  , dsod_BrowserImg = 'excel_96x96.png', dsod_ThumbImg = 'excel_32x32.png'
where dsodid in ('xls', 'xlsx');

alter table dm2_storage_object_def add column dsodtype_title character varying(300);
COMMENT ON COLUMN public.dm2_storage_object_def.dsodtype_title IS '大类标题';

COMMENT ON COLUMN public.dm2_storage_object_def.dsodtype IS '大类';

update dm2_storage_object_def
set dsodtype_title = dsodtype;

update dm2_storage_object_def
set dsodtype = dsod_metadata_engine;

alter table dm2_storage_object_def drop column dsodtype_map;
alter table dm2_storage_object_def drop column dsodname_map;
alter table dm2_storage_object_def drop column dsodtitle_map;



update dm2_storage_object_def
set dsod_detail_engine = 'same_file_mainname';

/*
	2020-5-10 王西亚
	系统更新了元数据引擎提取模式，数据库中也要同步更新
	初始化元数据提取引擎
*/


update dm2_storage_object_def
set dsod_metadata_engine = 'default'
where dsod_metadata_engine not in ('vector', 'raster', 'picture');



/*
	2020-5-21 王西亚
	调整图片文件的元数据引擎提取方式，改为使用GDAL读取元数据，并对其中的部分节点进行调整优化
*/

update dm2_storage_object_def
set dsod_metadata_engine = 'sat', dsodtype = 'sat', dsod_ext_whitelist = 'gz;tar.gz;zip;rar'
where dsodtype_title = '卫星数据';

update dm2_storage_object_def
set dsod_tags_engine = 'global_dim';

update dm2_storage_object_def
set dsod_metadata_engine = 'raster', dsodtype = 'picture'
where dsodtype = '图片';

update dm2_storage_object_def
set dsod_metadata_engine = 'default', dsodtype = 'document'
where dsodtype = '文档';


update dm2_storage_object_def
set dsod_metadata_engine = '21at_mbtiles', dsodtype = 'tiles'
where dsodtype = '服务数据';

update dm2_storage_object_def
set dsod_metadata_engine = 'bzff', dsodtype = 'bzff'
where dsodtype = '生产成果数据';

update dm2_storage_object_def
set dsod_metadata_engine = 'vector', dsodtype = 'vector'
where dsodtype = '矢量';

update dm2_storage_object_def
set dsod_metadata_engine = 'vector', dsodtype = 'vector'
where dsodtype = '矢量数据集';

update dm2_storage_object_def
set dsod_metadata_engine = 'raster', dsodtype = 'img'
where dsodtype = '遥感影像';

delete from public.dm2_storage_object_def;
INSERT INTO public.dm2_storage_object_def VALUES ('bj2', 'bj2', '北京二号', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('cb04', 'cb04', '中巴地球资源卫星04星', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('de2', 'de2', 'DEIMOS-2', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy302', 'zy3-zy302', '资源一号01/02星-ZY302', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('hj', 'hj', '环境一号A/B/C星', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('jl1', 'jl1', '吉林一号', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('zy02c-pms', 'zy02c-pms', '资源三号02星-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('zy02c-hrc', 'zy02c-hrc', '资源三号02星-HRC', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('docx', 'docx', 'Word2017', 'document', 'default', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '文档');
INSERT INTO public.dm2_storage_object_def VALUES ('doc', 'doc', 'Word2013', 'document', 'default', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '文档');
INSERT INTO public.dm2_storage_object_def VALUES ('21at_mbtiles', '21at_mbtiles', '二十一世纪公司切片', 'tiles', '21at_mbtiles', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '服务数据');
INSERT INTO public.dm2_storage_object_def VALUES ('bzff', 'bzff', '标准分幅', 'bzff', 'bzff', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '生产成果数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gdb', 'gdb', 'gdb数据集', 'vector', 'vector', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '矢量数据集');
INSERT INTO public.dm2_storage_object_def VALUES ('pix', 'pix', 'PIX影像', 'img', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '遥感影像');
INSERT INTO public.dm2_storage_object_def VALUES ('tiff', 'tiff', 'TIFF影像', 'img', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '遥感影像');
INSERT INTO public.dm2_storage_object_def VALUES ('tif', 'tif', 'TIF影像', 'img', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '遥感影像');
INSERT INTO public.dm2_storage_object_def VALUES ('xls', 'xls', 'Excel2013', 'document', 'default', 'same_file_mainname', 'global_dim', '', 'excel_96x96.png', 'excel_32x32.png', 'inner', 'excel', NULL, 'inner', 'excel', NULL, '文档');
INSERT INTO public.dm2_storage_object_def VALUES ('xlsx', 'xlsx', 'Excel2017', 'document', 'default', 'same_file_mainname', 'global_dim', '', 'excel_96x96.png', 'excel_32x32.png', 'inner', 'excel', NULL, 'inner', 'excel', NULL, '文档');
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy3', 'zy3-zy3', '资源一号01/02星-ZY3', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy3_01a', 'zy3-zy3_01a', '资源一号01/02星-ZY3_01a', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('zy3-zy301a', 'zy3-zy301a', '资源一号01/02星-zy301a', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('th-th01', 'th-th01', '天绘一号-th01', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('shp', 'shp', 'SHP矢量', 'vector', 'vector', 'same_file_mainname', 'global_dim', '', 'vector_96x96.png', 'vector_32x32.png', 'inner', 'shp', NULL, 'inner', 'shp', NULL, '矢量');
INSERT INTO public.dm2_storage_object_def VALUES ('k2', 'k2', 'Kompsat-2', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('k3', 'k3', 'Kompsat-3', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('pl', 'pl', 'Pleiades1A/1B', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('rapideye', 'rapideye', 'RapidEye', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('spot', 'spot', 'SPOT', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('sv1', 'sv1', '高景一号', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('wv', 'wv', 'WordView01/02/03', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('yg', 'yg', '遥感卫星', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf1-pms', 'gf1-pms', '高分一号-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf1-wfv', 'gf1-wfv', '高分一号-WFV', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf2-pms', 'gf2-pms', '高分二号-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf2-wfv', 'gf2-wfv', '高分二号-WFV', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-hh', 'gf3-hh', '高分三号-HH', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-vhvv', 'gf3-vhvv', '高分三号-VHVV', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf3-dh', 'gf3-dh', '高分三号-DH', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-pms', 'gf4-pms', '高分四号-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-b1', 'gf4-b1', '高分四号-B1', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-pmi', 'gf4-pmi', '高分四号-PMI', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf4-irs', 'gf4-irs', '高分四号-IRS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-ahsi', 'gf5-ahsi', '高分五号-AHSI', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-vims', 'gf5-vims', '高分五号-VIMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-gmi', 'gf5-gmi', '高分五号-GMI', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf5-emi', 'gf5-emi', '高分五号-EMI', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf6-pms', 'gf6-pms', '高分六号-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('gf6-wfv', 'gf6-wfv', '高分六号-WFV', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('landsat-ld8', 'landsat-ld8', 'LandSat-ld8', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('landsat-le7', 'landsat-le7', 'LandSat-le7', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('sj9a-pmn', 'sj9a-pmn', '实践九号-PMN', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('sj9a-pms', 'sj9a-pms', '实践九号-PMS', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('th-th', 'th-th', '天绘一号-th', 'sat', 'sat', 'same_file_mainname', 'global_dim', 'gz;tar.gz;zip;rar', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '卫星数据');
INSERT INTO public.dm2_storage_object_def VALUES ('jpg', 'jpg', 'JPG图片', 'picture', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '图片');
INSERT INTO public.dm2_storage_object_def VALUES ('png', 'png', 'PNG图片', 'picture', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '图片');
INSERT INTO public.dm2_storage_object_def VALUES ('bmp', 'bmp', 'BMP图片', 'picture', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '图片');
INSERT INTO public.dm2_storage_object_def VALUES ('gif', 'gif', 'GIF图片', 'picture', 'raster', 'same_file_mainname', 'global_dim', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '图片');
INSERT INTO public.dm2_storage_object_def VALUES ('img', 'img', 'IMG影像', 'img', 'raster', 'same_file_mainname', 'global_dim', '', '', '', NULL, NULL, NULL, NULL, NULL, NULL, '遥感影像');




/*
    将dm2_storage_object_check表，纳入storage体系中进行维护

*/

-- Table: public.dm2_storage_object_check

-- DROP TABLE public.dm2_storage_object_check;

CREATE TABLE public.dm2_storage_object_check
(
    dsoc_object_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dsoc_process_status integer DEFAULT 0,
    dsoc_process_procid character varying(100) COLLATE pg_catalog."default",
    dsoc_check_memo text COLLATE pg_catalog."default",
    dsoc_memo text COLLATE pg_catalog."default",
    dsoc_lastmodifytime timestamp(6) without time zone,
    CONSTRAINT dm2_storage_object_check_pkey PRIMARY KEY (dsoc_object_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.dm2_storage_object_check
    OWNER to postgres;
COMMENT ON TABLE public.dm2_storage_object_check
    IS '数管-存储目录-对象-检查';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_object_id
    IS '对象id';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_process_status
    IS '检查状态  0-待检查 1-检查中 2-通过检查 3-未通过检查 4-无需检查 ';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_process_procid
    IS '检查数据-提取标识';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_check_memo
    IS '检查数据日志';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_memo
    IS '简要说明';

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_lastmodifytime
    IS '记录最后刷新时间';








/*
    2020-6-22 扩展文件识别模式
    。对GDB、mdb等数据集，需要在元数据解析完毕后，进行进一步处理，解析并存储数据集中的图层信息
    。在对象定义表中，引入后处理引擎并行调度，对元数据解析后的操作进行抽象和封装
    。考虑到对象详情信息，需要进一步支持层级结构，对对象详情表，增加树节点
    。将图层加入到文件列表中后，会对目前的文件表产生影响
    。增加矢量数据集矢量图层类型对象
    。对数据检查验证表进行完善
*/

alter table dm2_storage_object_def add column dsod_last_process_engine character varying[];
COMMENT ON COLUMN public.dm2_storage_object_def.dsod_last_process_engine IS '对象入库后处理引擎';

alter table dm2_storage_obj_detail add column dod_parentid character varying(100) default '-1';
COMMENT ON COLUMN public.dm2_storage_obj_detail.dod_parentid IS '父节点';

update dm2_storage_obj_detail set dod_parentid = '-1';



alter table dm2_storage_object add column dsoLastProcessStatus integer DEFAULT 1;
COMMENT ON COLUMN public.dm2_storage_object.dsoLastProcessStatus IS '后处理状态';
alter table dm2_storage_object add column dsoLastProcessProcId character varying(100);
COMMENT ON COLUMN public.dm2_storage_object.dsoLastProcessProcId IS '后处理状态';
alter table dm2_storage_object add column dsoLastProcessMemo text;
COMMENT ON COLUMN public.dm2_storage_object.dsoLastProcessMemo IS '后处理结果';

-- Index: idx_dm2_storage_object_LastProcessStatus

-- DROP INDEX public.idx_dm2_storage_object_LastProcessStatus;

CREATE INDEX idx_dm2_storage_object_LastProcessStatus
    ON public.dm2_storage_object(dsoLastProcessStatus);

-- Index: idx_dm2_storage_object_LastProcessProcID

-- DROP INDEX public.idx_dm2_storage_object_LastProcessProcID;

CREATE INDEX idx_dm2_storage_object_LastProcessProcID
    ON public.dm2_storage_object(dsoLastProcessProcId);
    

alter table dm2_storage_file add column dsfType character varying(100) default 'file';
COMMENT ON COLUMN public.dm2_storage_file.dsfType IS '类型';




INSERT INTO public.dm2_storage_object_def VALUES (
    'vector_dataset_layer', 'vector_dataset_layer', '矢量数据集图层', 'vector_dataset_layer'
  , null, null, 'global_dim', null, 'vector_96x96.png', 'vector_32x32.png', NULL, NULL, NULL, NULL, NULL, NULL, '矢量数据集图层');

update dm2_storage_object_def set dsod_last_process_engine = '{metadata_vectordataset_parser}' where dsodid = 'gdb';

ALTER TABLE public.dm2_storage_object_check
    ADD COLUMN dsoc_process_status_field integer NOT NULL DEFAULT 4;

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_process_status_field
    IS '检查状态（字段）  2-通过检查 3-未通过检查 4-无需检查';


ALTER TABLE public.dm2_storage_object_check
    ADD COLUMN dsoc_process_status_feature integer NOT NULL DEFAULT 4;

COMMENT ON COLUMN public.dm2_storage_object_check.dsoc_process_status_feature
    IS '检查状态(图斑)  2-通过检查 3-未通过检查 4-无需检查';




/*
    2020-07-15 王西亚
    。为解决业务数据集，在数据对象表中扩展对象所属父对象标识
*/

alter table dm2_storage_object add column dsoParentObjId character varying(100);
COMMENT ON COLUMN public.dm2_storage_object.dsoParentObjId IS '父对象标识';

alter table dm2_storage_directory add column dsdParentObjId character varying(100);
COMMENT ON COLUMN public.dm2_storage_directory.dsdParentObjId IS '父对象标识';

alter table dm2_storage_file add column dsfParentObjId character varying(100);
COMMENT ON COLUMN public.dm2_storage_file.dsfParentObjId IS '父对象标识';

delete from ro_global_config where gcfgid between 4000 and 4999;
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(4001, 'dm2_storage.directory_object_fuzzy', '数管-目录识别-模糊识别', '0', null);
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(4002, 'dm2_storage.file_object_sat', '数管-文件识别-卫星数据识别', '0', null);
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(4003, 'dm2_storage.file_object_bus', '数管-文件识别-业务数据识别', '0', null);
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(4004, 'dm2_storage.tags.parser.seperator', '数管-标签-解析-分隔符', '_; ;/;\;-', '多个分隔符,使用分号分隔;允许使用空格做分隔');


/*
    2020-7-22 王西亚
    。为解决业务数据集，在数据对象表中扩展业务元数据的xml类型,文本类型等
*/

alter table dm2_storage_object add column dsometadataxml_bus xml;
COMMENT ON COLUMN public.dm2_storage_object.dsometadataxml_bus IS '业务元数据XML';

alter table dm2_storage_object add column dsometadatatext_bus text;
COMMENT ON COLUMN public.dm2_storage_object.dsometadatatext_bus IS '业务元数据文本';

alter table dm2_storage_object add column dsometadatatype_bus integer DEFAULT 1;
COMMENT ON COLUMN public.dm2_storage_object.dsometadatatype_bus IS '元数据类型;0-txt;1-json;2-xml';

alter table dm2_storage_object add column dsometadata_bus_parsememo text;
COMMENT ON COLUMN public.dm2_storage_object.dsometadata_bus_parsememo IS '业务元数据收割备注';

alter table dm2_storage_object add column dsometadata_bus_parsestatus integer DEFAULT 1;
COMMENT ON COLUMN public.dm2_storage_object.dsometadata_bus_parsestatus IS '元数据提取状态;0-完成;1-待提取;2-提取中;3-提取有误';
