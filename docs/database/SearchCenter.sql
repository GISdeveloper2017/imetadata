-- 2017-1-13 创建核心数据资产检索数据库

/*
-- 数据资产-检索表
da_search

*/

-- Table: public.da_search 数据资产-检索基础表

-- DROP TABLE public.da_search;

CREATE TABLE public.da_search
(
    daid           bigSerial               NOT NULL, -- 标示
    daType         character varying(100)  NOT NULL, -- 检索内容类型
    datitle        character varying(4000) NOT NULL, -- 标题
    daindexid      character varying(100)  NOT NULL, -- 编目标示
    daindexclass   character varying(100)  NOT NULL, -- 编目大类
    daindextype    character varying(100)  NOT NULL, -- 编目小类
    dafileid       character varying(100)  NOT NULL, -- 文件标示
    dadescription  text,                             -- 备注
    dafiletype     integer                 NOT NULL, -- 文件类型
    dafilemetadata xml,                              -- 文件元数据
    daImportDate   timestamp without time zone DEFAULT current_date,
    daImportTime   timestamp with time zone    DEFAULT now(),
    dasearch       tsvector,                         -- 检索
    CONSTRAINT da_search_pkey PRIMARY KEY (daid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.da_search
    OWNER TO postgres;
COMMENT ON TABLE public.da_search
    IS '产品编目-全文检索分词表';
COMMENT ON COLUMN public.da_search.daid IS '标示';
COMMENT ON COLUMN public.da_search.daType IS '检索内容类型';
COMMENT ON COLUMN public.da_search.datitle IS '标题';
COMMENT ON COLUMN public.da_search.daindexid IS '编目标示';
COMMENT ON COLUMN public.da_search.daindexclass IS '编目大类';
COMMENT ON COLUMN public.da_search.daindextype IS '编目小类';
COMMENT ON COLUMN public.da_search.dafileid IS '文件标示';
COMMENT ON COLUMN public.da_search.dadescription IS '备注';
COMMENT ON COLUMN public.da_search.dafiletype IS '文件类型';
COMMENT ON COLUMN public.da_search.dafilemetadata IS '文件元数据';
COMMENT ON COLUMN public.da_search.daImportDate IS '入库日期';
COMMENT ON COLUMN public.da_search.daImportTime IS '入库时间';
COMMENT ON COLUMN public.da_search.dasearch IS '检索关键词';

-- Index: public.idx_da_search_type

-- DROP INDEX public.idx_da_search_type;

CREATE INDEX idx_da_search_type
    ON public.da_search
        USING btree
        (daType COLLATE pg_catalog."default");

-- Index: public.idx_da_search_indexid

-- DROP INDEX public.idx_da_search_indexid;

CREATE INDEX idx_da_search_indexid
    ON public.da_search
        USING btree
        (daindexid COLLATE pg_catalog."default");

-- Index: public.idx_da_search_indexclass

-- DROP INDEX public.idx_da_search_indexclass;

CREATE INDEX idx_da_search_indexclass
    ON public.da_search
        USING btree
        (daIndexClass COLLATE pg_catalog."default");

-- Index: public.idx_da_search_indextype

-- DROP INDEX public.idx_da_search_indextype;

CREATE INDEX idx_da_search_indextype
    ON public.da_search
        USING btree
        (daindextype COLLATE pg_catalog."default");

-- Index: public.idx_da_search_fileid

-- DROP INDEX public.idx_da_search_fileid;

CREATE INDEX idx_da_search_fileid
    ON public.da_search
        USING btree
        (dafileid COLLATE pg_catalog."default");

-- Index: public.idx_da_search_filetype

-- DROP INDEX public.idx_da_search_filetype;

CREATE INDEX idx_da_search_filetype
    ON public.da_search
        USING btree
        (dafiletype COLLATE pg_catalog."default");


-- Index: public.idx_da_search_importdate

-- DROP INDEX public.idx_da_search_importdate;

CREATE INDEX idx_da_search_importdate
    ON public.da_search
        USING btree
        (daImportDate COLLATE pg_catalog."default");


-- Index: public.idx_da_search_search

-- DROP INDEX public.idx_da_search_search;

CREATE INDEX idx_da_search_search
    ON public.da_search
        USING gin
        (dasearch);


-- Table: public.da_search_package

-- DROP TABLE public.da_search_package;

CREATE TABLE public.da_search_package
(
    dafileseqid    bigint                  not null, -- 包内文件索引号
    dafilename     character varying(4000) NOT NULL, -- 文件全名
    dafilemainname character varying(400)  NOT NULL, -- 文件主名
    dafileext      character varying(100),           -- 文件扩展名
    dafilesize     bigint,                           -- 文件大小
    dafiledate     timestamp with time zone,         -- 文件日期
    CONSTRAINT da_search_package_pkey PRIMARY KEY (daid),
    CONSTRAINT da_search_package_type_check CHECK (datype::text = 'package'::text)
)
    INHERITS (public.da_search)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.da_search_package
    OWNER TO postgres;
COMMENT ON TABLE public.da_search_package
    IS '数据资产-数据包';

COMMENT ON COLUMN public.da_search_package.daid IS '标示';
COMMENT ON COLUMN public.da_search_package.daType IS '检索内容类型';
COMMENT ON COLUMN public.da_search_package.datitle IS '标题';
COMMENT ON COLUMN public.da_search_package.daindexid IS '编目标示';
COMMENT ON COLUMN public.da_search_package.daindexclass IS '编目大类';
COMMENT ON COLUMN public.da_search_package.daindextype IS '编目小类';
COMMENT ON COLUMN public.da_search_package.dafileid IS '文件标示';
COMMENT ON COLUMN public.da_search_package.dadescription IS '备注';
COMMENT ON COLUMN public.da_search_package.dafiletype IS '文件类型';
COMMENT ON COLUMN public.da_search_package.dafilemetadata IS '文件元数据';
COMMENT ON COLUMN public.da_search_package.daImportDate IS '入库日期';
COMMENT ON COLUMN public.da_search_package.daImportTime IS '入库时间';
COMMENT ON COLUMN public.da_search_package.dasearch IS '检索关键词';

COMMENT ON COLUMN public.da_search_package.dafileseqid IS '包内文件索引号';
COMMENT ON COLUMN public.da_search_package.dafilename IS '包内文件全名';
COMMENT ON COLUMN public.da_search_package.dafilemainname IS '包内文件主名';
COMMENT ON COLUMN public.da_search_package.dafileext IS '包内文件扩展名';
COMMENT ON COLUMN public.da_search_package.dafiletype IS '包内文件类型';
COMMENT ON COLUMN public.da_search_package.dafilesize IS '包内文件大小';
COMMENT ON COLUMN public.da_search_package.dafiledate IS '包内文件日期';

-- Index: public.idx_da_search_package_type

-- DROP INDEX public.idx_da_search_package_type;

CREATE INDEX idx_da_search_package_type
    ON public.da_search_package
        USING btree
        (daType COLLATE pg_catalog."default");

-- Index: public.idx_da_search_package_filedate

-- DROP INDEX public.idx_da_search_package_filedate;

CREATE INDEX idx_da_search_package_filedate
    ON public.da_search_package
        USING btree
        (dafiledate);

-- Index: public.idx_da_search_package_fileext

-- DROP INDEX public.idx_da_search_package_fileext;

CREATE INDEX idx_da_search_package_fileext
    ON public.da_search_package
        USING btree
        (dafileext COLLATE pg_catalog."default");

-- Index: public.idx_da_search_package_filesize

-- DROP INDEX public.idx_da_search_package_filesize;

CREATE INDEX idx_da_search_package_filesize
    ON public.da_search_package
        USING btree
        (dafilesize);

-- Index: public.idx_da_search_package_filetype

-- DROP INDEX public.idx_da_search_package_filetype;

CREATE INDEX idx_da_search_package_filetype
    ON public.da_search_package
        USING btree
        (dafiletype);


-- 查询方法：
select dm_index_ptd.diDescription,
       dm_index_ptd_files.diFileName,
       dm_index_ptd.diMemo,
       dm_index_ptd_files.diFileSize,
       dm_index_ptd_files.diFileDate,
       dm_index_ptd_files.diIsSpatial,
       dm_index_ptd_files.diSpatialMetaData,
       dm_index_ptd.diDeptID,
       dm_index_ptd.diAudited,
       dm_index_ptd.diImportTime,
       dm_index_ptd.diClass,
       dm_index_ptd.diType,
       ro_file.fid
from dm_index_ptd
         left join dm_index_ptd_files on dm_index_ptd.diid = dm_index_ptd_files.diid
         left join dm_index_file on dm_index_ptd.diid = dm_index_file.indexid
         left join ro_file on dm_index_file.fileid = ro_file.fid
where dm_index_ptd.diid = 'v2117ab6c5cf64befa0e15c7c46b5ae20'
limit 100


SELECT daFileName, daTitle, daDescription, *
FROM dm_index_ftsearch
WHERE dasearch @@ to_tsquery('zhParserCFG', replace('北京 环保 航片', ' ', '&'))
ORDER BY daid ASC
LIMIT 10;

grant all on all tables in schema public to user_datacube

select daSearch
from da_search_package
WHERE daSearch @@ replace('2011年 外业', ' ', '&')::tsquery
ORDER BY daid ASC


select to_tsquery('zhParserCFG', replace('2011年外业', ' ', '&'))
select replace('2011年 外业', ' ', '&')::tsquery
           update da_search set daSearch = to_tsVector(dadescription)

select daSearch
from da_search_package
ORDER BY daid ASC



truncate table da_search_package;

insert into da_search_package(datype, daTitle, daIndexID, daIndexClass, daIndexType, daFileID, daDescription,
                              dafiletype, dafilemetadata,
                              dafileseqid, dafilename, dafilemainname, dafileext, dafilesize, dafiledate, daSearch)

select *
from dblink(
             'hostaddr=172.172.5.194 port=5432 dbname=datamng user=postgres password=postgres',
             '
             select ''package'' as datype,
                 dm_index_ptd.diDescription as daTitle,
                 dm_index_ptd.diid as daIndexID,
                 dm_index_ptd.diClass as daIndexClass,
                 dm_index_ptd.diType as daIndexType,
                 ro_file.fid as daFileID,
                 COALESCE(dm_index_ptd.diDescription, '''') || ''|'' || COALESCE(dm_index_ptd_files.diFileName, '''') || ''|'' || COALESCE(dm_index_ptd.diMemo, '''') as daDescription,
                 COALESCE(dm_index_ptd_files.diIsSpatial, -1) as dafiletype,
                 dm_index_ptd_files.diSpatialMetaData as dafilemetadata,
                 dm_index_ptd_files.diSeqId as dafileseqid,
                 dm_index_ptd_files.diFileName as dafilename,
                 dm_index_ptd_files.diFileName as dafilemainname,
                 dm_index_ptd_files.diFileExt as dafileext,
                 dm_index_ptd_files.diFileSize as dafilesize,
                 dm_index_ptd_files.diFileDate as dafiledate,
                 to_tsVector(COALESCE(dm_index_ptd.diDescription, '''') || ''|'' || COALESCE(dm_index_ptd_files.diFileName, '''') || ''|'' || COALESCE(dm_index_ptd.diMemo, '''')) as dasearch
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