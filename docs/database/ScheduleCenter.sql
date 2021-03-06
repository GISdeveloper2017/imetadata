/*
    调度中心 v2
    。本版本的目标是基于Linux版本的调度中心
    。机制仍然是以数据库服务为中心，实现不同任务模式的处理
    。设计：
      。sch_center
        。调度中心表，处理服务的创建任务
      。sch_center_mission
        。调度的任务表
        。描述任务的运行状态，以及具体的执行要求
*/


-- Table: public.sch_center

-- DROP TABLE public.sch_center;

CREATE TABLE public.sch_center
(
    scid             character varying(100) COLLATE pg_catalog."default" NOT NULL,
    sctitle          character varying(200) COLLATE pg_catalog."default" NOT NULL,

    scstatus         integer DEFAULT 1,
    scprocessid      character varying(100) COLLATE pg_catalog."default",

    sclastmodifytime timestamp(6) without time zone,
    scmemo           text,
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

-- Index: idx_sch_center_processid

-- DROP INDEX public.idx_sch_center_processid;

CREATE INDEX idx_sch_center_processid
    ON public.sch_center USING btree
        (scprocessid COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_sch_center_scanstatus

-- DROP INDEX public.idx_sch_center_scanstatus;

CREATE INDEX idx_sch_center_status
    ON public.sch_center USING btree
        (scstatus ASC NULLS LAST)
    TABLESPACE pg_default;



-- Table: public.sch_center_mission

-- DROP TABLE public.sch_center_mission;

create table if not exists sch_center_mission
(
    scmid             varchar(100) not null
        constraint sch_center_mission_pkey
            primary key,
    scmtitle          varchar(200) not null,
    scmcommand        varchar(100),
    scmstatus         integer      default 1,
    scmprocessid      varchar(100),
    scmlastmodifytime timestamp(6) default now(),
    scmcenterid       varchar(100),
    scmtrigger        text,
    scmalgorithm      varchar(200) not null,
    scmparams         jsonb,
    scmmemo           text
);

comment on table sch_center_mission is '调度-中心';
comment on column sch_center_mission.scmid is '标识';
comment on column sch_center_mission.scmtitle is '标题';

comment on column sch_center_mission.scmcommand is '命令';
comment on column sch_center_mission.scmstatus is '状态 0：完成，1：待处理，2：处理中';
comment on column sch_center_mission.scmprocessid is '并行处理标识';

comment on column sch_center_mission.scmtrigger is '触发器';
comment on column sch_center_mission.scmalgorithm is '算法';
comment on column sch_center_mission.scmparams is '详细参数';

comment on column sch_center_mission.scmmemo is '备注';
comment on column sch_center_mission.scmcenterid is '所属组标示';
comment on column sch_center_mission.scmlastmodifytime is '最后修改时间';

alter table sch_center_mission
    owner to postgres;

create index if not exists idx_sch_center_mission_processid
    on sch_center_mission (scmprocessid);

create index if not exists idx_sch_center_mission_status
    on sch_center_mission (scmstatus);

/*
    测试任务
*/

delete
from sch_center_mission
where scmid = 'test';
insert into sch_center_mission( scmid, scmtitle, scmcommand, scmstatus, scmprocessid
                              , scmtrigger, scmalgorithm, scmParams
                              , scmlastmodifytime, scmmemo, scmcenterid)
values ( 'test', '测试', null, 0, null
       , 'db_queue', 'job_dm2_storage_parser', '{
    "process": {
      "parallel_count": 1
    }
  }'::json
       , now(), null, '1');


/*
    2020-09-01 王西亚
    .开始测试调度系统的运行情况, 增加对调度的启动, 停止, 加速, 减速等任务
*/


--启动所有调度
update sch_center_mission
set scmcommand = 'start',
    scmstatus  = 1;

--停止所有调度
update sch_center_mission
set scmcommand = 'shutdown',
    scmstatus  = 0;

update sch_center_mission
set scmcommand   = 'stop',
    scmstatus    = 1,
    scmprocessid = null
where scmid = 'test';

--退出服务
update sch_center_mission
set scmstatus  = 0,
    scmcommand = 'shutdown';
