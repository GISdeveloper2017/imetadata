/*
    数据分析数据库设计
    . da2_tools: 算法
*/
-- Table: public.da2_tools

-- DROP TABLE public.da2_tools;

CREATE TABLE public.da2_tools
(
    dat_id         character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dat_name       character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dat_title      character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dat_path       character varying(2000) COLLATE pg_catalog."default",
    dat_type       character varying(50) COLLATE pg_catalog."default",
    dat_remark     text COLLATE pg_catalog."default",
    dat_createtime timestamp with time zone                            NOT NULL DEFAULT now(),
    CONSTRAINT da2_tools_pkey PRIMARY KEY (dat_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_tools
    OWNER to postgres;

COMMENT ON COLUMN public.da2_tools.dat_id
    IS '主键';

COMMENT ON COLUMN public.da2_tools.dat_name
    IS '名称';

COMMENT ON COLUMN public.da2_tools.dat_title
    IS '标题';

COMMENT ON COLUMN public.da2_tools.dat_path
    IS '路径';

COMMENT ON COLUMN public.da2_tools.dat_type
    IS '类型';

COMMENT ON COLUMN public.da2_tools.dat_remark
    IS '描述';

COMMENT ON COLUMN public.da2_tools.dat_createtime
    IS '创建时间';

INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('1', 'AnalysisIntersect', '占压分析', 'AnalysisIntersect.py', null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('2', 'AnalysisCrossBound', '越界分析', null, null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('3', 'AnalysisOutOfScope', '范围外分析', null, null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('4', 'AnalysisChanged', '地类变化分析', null, null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('5', 'AnalysisIntersectDL', '占压地类分析', 'AnalysisIntersectDL.py', null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('6', 'AnalysisIntersectBuffer', '缓冲分析', 'AnalysisIntersectBuffer.py', null, null, now());
INSERT INTO public.da2_tools (dat_id, dat_name, dat_title, dat_path, dat_type, dat_remark, dat_createtime)
VALUES ('7', 'VectorImportDB', '矢量入库', 'VectorImportDB.py', null, null, now());


-- Table: public.da2_model

-- DROP TABLE public.da2_model;

CREATE TABLE public.da2_model
(
    dam_id         character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dam_catalog_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dam_name       character varying(200) COLLATE pg_catalog."default",
    dam_title      character varying(200) COLLATE pg_catalog."default",
    dam_type       character varying(20) COLLATE pg_catalog."default",
    dam_tool_id    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dam_createtime timestamp with time zone                            NOT NULL DEFAULT now(),
    dam_updatetime timestamp with time zone                                     DEFAULT now(),
    dam_remark     text COLLATE pg_catalog."default",
    dam_params     jsonb,
    CONSTRAINT da2_model_pkey PRIMARY KEY (dam_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_model
    OWNER to postgres;

COMMENT ON COLUMN public.da2_model.dam_id
    IS '主键';

COMMENT ON COLUMN public.da2_model.dam_catalog_id
    IS '分类主键';

COMMENT ON COLUMN public.da2_model.dam_name
    IS '名称';

COMMENT ON COLUMN public.da2_model.dam_title
    IS '标题';

COMMENT ON COLUMN public.da2_model.dam_tool_id
    IS '算法主键';

COMMENT ON COLUMN public.da2_model.dam_type
    IS '类型';

COMMENT ON COLUMN public.da2_model.dam_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_model.dam_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_model.dam_remark
    IS '描述';

COMMENT ON COLUMN public.da2_model.dam_params
    IS '模型参数模板';


INSERT INTO public.da2_model (dam_id, dam_catalog_id, dam_name, dam_title, dam_type, dam_tool_id, dam_createtime,
                              dam_updatetime, dam_remark, dam_params)
VALUES ('1', '1', 'ksyjfx', '矿山越界分析', 'busi_gettime_getspac', '2', '2021-03-03 09:39:09.285381', null, '越界分析算法', null);
INSERT INTO public.da2_model (dam_id, dam_catalog_id, dam_name, dam_title, dam_type, dam_tool_id, dam_createtime,
                              dam_updatetime, dam_remark, dam_params)
VALUES ('2', '1', 'jsydzygdfw', '建设用地占压耕地范围', 'busi_gettime_getspac', '1', '2021-03-03 09:40:42.228145', null, '占压分析算法',
        null);
INSERT INTO public.da2_model (dam_id, dam_catalog_id, dam_name, dam_title, dam_type, dam_tool_id, dam_createtime,
                              dam_updatetime, dam_remark, dam_params)
VALUES ('3', '1', 'jsydwgfx', '新增建设用地违规分析', 'busi_gettime_getspac', '3', '2021-03-03 09:41:39.465902', null, '范围外分析算法',
        null);


-- Table: public.da2_model_data

-- DROP TABLE public.da2_model_data;

CREATE TABLE public.da2_model_data
(
    damd_aid        character varying(100) COLLATE pg_catalog."default" NOT NULL,
    damd_model_id   character varying(100) COLLATE pg_catalog."default" NOT NULL,
    damd_dataname   character varying(200) COLLATE pg_catalog."default",
    damd_busid      jsonb,
    damd_createtime timestamp with time zone                            NOT NULL DEFAULT now(),
    damd_remark     text COLLATE pg_catalog."default",
    damd_style      jsonb,
    CONSTRAINT da2_model_data_pkey PRIMARY KEY (damd_aid)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_model_data
    OWNER to postgres;

COMMENT ON COLUMN public.da2_model_data.damd_aid
    IS '主键';

COMMENT ON COLUMN public.da2_model_data.damd_model_id
    IS '模型标识';

COMMENT ON COLUMN public.da2_model_data.damd_dataname
    IS '数据名称';

COMMENT ON COLUMN public.da2_model_data.damd_busid
    IS '业务id';

COMMENT ON COLUMN public.da2_model_data.damd_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_model_data.damd_remark
    IS '描述';

COMMENT ON COLUMN public.da2_model_data.damd_style
    IS '样式描述';

INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('1', '1', '变化监测-矿产资源开发', '{
  "busid": "kczykf",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);
INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('2', '1', '审批后-已审批矿山范围', '{
  "busid": "yspksfw",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);
INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('3', '2', '变化监测-新增建设用地', '{
  "busid": "xzjsyd",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);
INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('4', '2', '审批后-耕地范围数据', '{
  "busid": "gdfwsj",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);
INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('5', '3', '变化监测-新增建设用地', '{
  "busid": "xzjsyd",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);
INSERT INTO public.da2_model_data (damd_aid, damd_model_id, damd_dataname, damd_busid, damd_createtime, damd_remark,
                                   damd_style)
VALUES ('6', '3', '审批后-批后监管项目', '{
  "busid": "phjgxm",
  "datatype": "shp"
}', '2021-03-03 09:52:23.736827', null, null);


-- Table: public.da2_model_catalog

-- DROP TABLE public.da2_model_catalog;

CREATE TABLE public.da2_model_catalog
(
    damc_id         character varying(100) COLLATE pg_catalog."default" NOT NULL,
    damc_pid        character varying(100) COLLATE pg_catalog."default" NOT NULL,
    damc_name       character varying(200) COLLATE pg_catalog."default",
    damc_title      character varying(200) COLLATE pg_catalog."default",
    damc_type       character varying(100) COLLATE pg_catalog."default",
    damc_createtime timestamp with time zone                            NOT NULL DEFAULT now(),
    damc_updatetime timestamp with time zone,
    damc_remark     text COLLATE pg_catalog."default",
    damc_isgroup    smallint,
    damc_orderidx   smallint,
    CONSTRAINT da2_model_catalog_pkey PRIMARY KEY (damc_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_model_catalog
    OWNER to postgres;

COMMENT ON COLUMN public.da2_model_catalog.damc_id
    IS '主键';

COMMENT ON COLUMN public.da2_model_catalog.damc_pid
    IS '父主键';

COMMENT ON COLUMN public.da2_model_catalog.damc_name
    IS '名称';

COMMENT ON COLUMN public.da2_model_catalog.damc_title
    IS '标题';

COMMENT ON COLUMN public.da2_model_catalog.damc_type
    IS '类型';

COMMENT ON COLUMN public.da2_model_catalog.damc_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_model_catalog.damc_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_model_catalog.damc_remark
    IS '描述';

COMMENT ON COLUMN public.da2_model_catalog.damc_isgroup
    IS '是否目录';

COMMENT ON COLUMN public.da2_model_catalog.damc_orderidx
    IS '排序';

INSERT INTO public.da2_model_catalog (damc_id, damc_pid, damc_name, damc_title, damc_type, damc_createtime,
                                      damc_updatetime, damc_remark, damc_isgroup, damc_orderidx)
VALUES ('1', '-1', '忻州项目分析模型', '忻州项目分析模型', null, '2021-03-03 10:53:40.570353', null, null, -1, null);


-- Table: public.da2_task

-- DROP TABLE public.da2_task;

CREATE TABLE public.da2_task
(
    dat_id          character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dat_name        character varying(200) COLLATE pg_catalog."default",
    dat_title       character varying(200) COLLATE pg_catalog."default",
    dat_server_id   character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dat_model_id    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dat_time_code   character varying(100) COLLATE pg_catalog."default",
    dat_region_code character varying(100) COLLATE pg_catalog."default",

    dat_status      smallint,
    dat_proc_id     character varying(100) COLLATE pg_catalog."default",
    dat_proc_memo   text COLLATE pg_catalog."default",

    dat_process     numeric,
    dat_createtime  timestamp with time zone                            NOT NULL DEFAULT now(),
    dat_updatetime  timestamp with time zone                                     DEFAULT now(),
    dat_remark      text COLLATE pg_catalog."default",
    dat_isactive    smallint,
    dat_params      jsonb,
    dat_createuser  character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT da2_task_pkey PRIMARY KEY (dat_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_task
    OWNER to postgres;

COMMENT ON COLUMN public.da2_task.dat_id
    IS '主键';

COMMENT ON COLUMN public.da2_task.dat_name
    IS '名称';

COMMENT ON COLUMN public.da2_task.dat_title
    IS '标题';

COMMENT ON COLUMN public.da2_task.dat_server_id
    IS '服务器主键';

COMMENT ON COLUMN public.da2_task.dat_model_id
    IS '模型主键';

COMMENT ON COLUMN public.da2_task.dat_time_code
    IS '时间维度';

COMMENT ON COLUMN public.da2_task.dat_region_code
    IS '空间维度';

COMMENT ON COLUMN public.da2_task.dat_status
    IS '任务状态
（1：待执行；2：运行中；0：成功；FAIL：3）
';

COMMENT ON COLUMN public.da2_task.dat_proc_memo
    IS '任务执行描述';

COMMENT ON COLUMN public.da2_task.dat_process
    IS '任务进度';

COMMENT ON COLUMN public.da2_task.dat_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_task.dat_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_task.dat_remark
    IS '描述';

COMMENT ON COLUMN public.da2_task.dat_isactive
    IS '是否启用（0：否；1：是），default:0';

COMMENT ON COLUMN public.da2_task.dat_params
    IS '参数jsonb';

INSERT INTO public.da2_task (dat_id, dat_name, dat_title, dat_server_id, dat_model_id, dat_time_code, dat_region_code,
                             dat_status, dat_proc_memo, dat_process, dat_createtime, dat_updatetime, dat_remark,
                             dat_isactive, dat_params, dat_proc_id, dat_createuser)
VALUES ('1', '昆明市-2019-矿山越界分析', '昆明市-2019-矿山越界分析', -1, '1', '2019', '5301', 1, null, 50, '2021-03-03 11:11:01.283373',
        null,
        null, null, '{
    "inputa": "D:\\生态审计数据存储目录\\03样例数据-昆明\\23现状矿山\\现状矿山范围.shp",
    "inputb": "D:\\生态审计数据存储目录\\03样例数据-昆明\\19已审批矿山范围\\已审批矿山范围_昆明市_2019.shp"
  }', null, 'robot');


-- Table: public.da2_server

-- DROP TABLE public.da2_server;

CREATE TABLE public.da2_server
(
    das_id          character varying(100) COLLATE pg_catalog."default" NOT NULL,
    das_name        character varying(200) COLLATE pg_catalog."default",
    das_title       character varying(200) COLLATE pg_catalog."default",
    das_ipaddr      character varying(100) COLLATE pg_catalog."default",
    das_icreatetime timestamp with time zone                            NOT NULL DEFAULT now(),
    das_iupdatetime timestamp with time zone                                     DEFAULT now(),
    das_status      character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT da2_server_pkey PRIMARY KEY (das_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_server
    OWNER to postgres;

COMMENT ON COLUMN public.da2_server.das_id
    IS '主键';

COMMENT ON COLUMN public.da2_server.das_name
    IS '名称';

COMMENT ON COLUMN public.da2_server.das_title
    IS '标题';

COMMENT ON COLUMN public.da2_server.das_ipaddr
    IS 'ip地址';

COMMENT ON COLUMN public.da2_server.das_icreatetime
    IS '创建时间';

COMMENT ON COLUMN public.da2_server.das_iupdatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_server.das_status
    IS '状态（0：正常；1：异常），default：0';



-- Table: public.da2_task_result_file

-- DROP TABLE public.da2_task_result_file;

CREATE TABLE public.da2_task_result_file
(
    daf_id         character varying(100) COLLATE pg_catalog."default" NOT NULL,
    daf_name       character varying(500) COLLATE pg_catalog."default",
    daf_resultfile character varying(2000) COLLATE pg_catalog."default",
    daf_createtime timestamp with time zone                            NOT NULL DEFAULT now(),
    daf_updatetime timestamp with time zone                                     DEFAULT now(),
    daf_processid  character varying(100) COLLATE pg_catalog."default",
    daf_status     character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT da2_task_result_file_pkey PRIMARY KEY (daf_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_task_result_file
    OWNER to postgres;

COMMENT ON COLUMN public.da2_task_result_file.daf_name
    IS '结果名称';

COMMENT ON COLUMN public.da2_task_result_file.daf_resultfile
    IS '结果文件';

COMMENT ON COLUMN public.da2_task_result_file.daf_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_task_result_file.daf_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_task_result_file.daf_processid
    IS '进程任务号';

COMMENT ON COLUMN public.da2_task_result_file.daf_status
    IS '0,1';



-- Table: public.da2_task_result

-- DROP TABLE public.da2_task_result;

CREATE TABLE public.da2_task_result
(
    dar_id           character varying(100) COLLATE pg_catalog."default" not null,
    dar_name         character varying(200) COLLATE pg_catalog."default",
    dar_title        character varying(200) COLLATE pg_catalog."default",
    dar_task_id      character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dar_model_id     character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dar_timecode     character varying(100) COLLATE pg_catalog."default",
    dar_regioncode   character varying(100) COLLATE pg_catalog."default",
    dar_resultdata   jsonb,
    dar_resultlength numeric,
    dar_resultarea   numeric,
    dar_lon          numeric,
    dar_lat          numeric,
    dar_createtime   timestamp with time zone                            NOT NULL DEFAULT now(),
    dar_updatetime   timestamp with time zone,
    dar_resultgeom   geometry,
    dar_rgdsids      character varying[] COLLATE pg_catalog."default",
    CONSTRAINT da2_task_result_pkey PRIMARY KEY (dar_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_task_result
    OWNER to postgres;

COMMENT ON COLUMN public.da2_task_result.dar_name
    IS '结果名称';

COMMENT ON COLUMN public.da2_task_result.dar_title
    IS '结果标题';

COMMENT ON COLUMN public.da2_task_result.dar_task_id
    IS '任务主键';

COMMENT ON COLUMN public.da2_task_result.dar_model_id
    IS '模型主键';

COMMENT ON COLUMN public.da2_task_result.dar_timecode
    IS '时间维度';

COMMENT ON COLUMN public.da2_task_result.dar_regioncode
    IS '空间维度';

COMMENT ON COLUMN public.da2_task_result.dar_resultdata
    IS '结果jsonb';

COMMENT ON COLUMN public.da2_task_result.dar_resultarea
    IS '结果面积';

COMMENT ON COLUMN public.da2_task_result.dar_resultlength
    IS '结果长度';

COMMENT ON COLUMN public.da2_task_result.dar_lon
    IS '经度';

COMMENT ON COLUMN public.da2_task_result.dar_lat
    IS '维度';

COMMENT ON COLUMN public.da2_task_result.dar_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_task_result.dar_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_task_result.dar_resultgeom
    IS '空间字段';



-- Table: public.da2_task_result_source

-- DROP TABLE public.da2_task_result_source;

CREATE TABLE public.da2_task_result_source
(
    datrs_id          character varying(100) COLLATE pg_catalog."default" NOT NULL,
    datr_id           character varying(100) COLLATE pg_catalog."default" not null,
    datrs_sourcedata  jsonb,
    datrs_soourcegeom geometry,
    datrs_targetdata  jsonb,
    datrs_targetgeom  geometry,
    datrs_createtime  timestamp with time zone                            NOT NULL DEFAULT now(),
    datrs_sourceobjid character varying(100) COLLATE pg_catalog."default",
    datrs_targetobjid character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT da2_task_result_source_pkey PRIMARY KEY (datrs_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_task_result_source
    OWNER to postgres;

COMMENT ON COLUMN public.da2_task_result_source.datrs_id
    IS '主键';

COMMENT ON COLUMN public.da2_task_result_source.datr_id
    IS '任务结果主键';

COMMENT ON COLUMN public.da2_task_result_source.datrs_sourcedata
    IS '分析源业务属性';

COMMENT ON COLUMN public.da2_task_result_source.datrs_soourcegeom
    IS '分析源数据';

COMMENT ON COLUMN public.da2_task_result_source.datrs_targetdata
    IS '分析源业务属性';

COMMENT ON COLUMN public.da2_task_result_source.datrs_targetgeom
    IS '分析源数据';

COMMENT ON COLUMN public.da2_task_result_source.datrs_sourceobjid
    IS '分析源数据ID';

COMMENT ON COLUMN public.da2_task_result_source.datrs_targetobjid
    IS '分析源数据ID';

COMMENT ON COLUMN public.da2_task_result_source.datrs_createtime
    IS '创建时间';


-- Table: public.da2_result_dlzyfx

-- DROP TABLE public.da2_result_dlzyfx;

CREATE TABLE public.da2_result_dlzyfx
(
    dard_id         character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dar_id          character varying(100) COLLATE pg_catalog."default" not null,
    dar_task_id     character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dar_model_id    character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dar_timecode    character varying(100) COLLATE pg_catalog."default",
    dar_regioncode  character varying(100) COLLATE pg_catalog."default",
    dard_tbbm       character varying(100) COLLATE pg_catalog."default",
    dard_tbmc       character varying(100) COLLATE pg_catalog."default",
    dard_dlmc       character varying(100) COLLATE pg_catalog."default",
    dard_dlbm       character varying(100) COLLATE pg_catalog."default",
    dard_zygeom     geometry,
    dard_zyarea     numeric,
    dard_createtime timestamp with time zone,
    dard_updatetime timestamp with time zone,
    dard_level      smallint,
    dard_xzqhcode   character varying(20) COLLATE pg_catalog."default",
    dard_province   character varying(20) COLLATE pg_catalog."default",
    dard_city       character varying(50) COLLATE pg_catalog."default",
    dard_county     character varying(50) COLLATE pg_catalog."default",
    dard_town       character varying(50) COLLATE pg_catalog."default",
    dard_villages   character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT da2_result_dlzyfx_pkey PRIMARY KEY (dard_id)
)
    TABLESPACE pg_default;

ALTER TABLE public.da2_result_dlzyfx
    OWNER to postgres;

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_id
    IS '主键';
COMMENT ON COLUMN public.da2_task_result.dar_id
    IS '结果主键';

COMMENT ON COLUMN public.da2_task_result.dar_task_id
    IS '任务主键';

COMMENT ON COLUMN public.da2_task_result.dar_model_id
    IS '模型主键';

COMMENT ON COLUMN public.da2_task_result.dar_timecode
    IS '时间维度';

COMMENT ON COLUMN public.da2_task_result.dar_regioncode
    IS '空间维度';


COMMENT ON COLUMN public.da2_result_dlzyfx.dard_tbbm
    IS '图斑编号';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_tbmc
    IS '图斑名称';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_dlmc
    IS '地类名称';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_dlbm
    IS '地类编码';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_zygeom
    IS '占地范围';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_zyarea
    IS '占地面积';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_createtime
    IS '创建时间';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_updatetime
    IS '更新时间';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_level
    IS '违规级别：
0：不违规；1：关注；2：重点关注';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_xzqhcode
    IS '行政区划代码';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_province
    IS '省';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_city
    IS '市';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_county
    IS '县';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_town
    IS '乡镇';

COMMENT ON COLUMN public.da2_result_dlzyfx.dard_villages
    IS '村';