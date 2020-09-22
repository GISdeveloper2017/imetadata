-- 2017-1-13 创建任务处理数据库

/*

-- 任务表
sch_event
sch_mission

*/

-- Table: public.sch_event

-- DROP TABLE public.sch_event;

CREATE TABLE public.sch_event
(
    seid         character varying(50) NOT NULL, -- 标识
    setitle      character varying(200),         -- 标题
    segroup      character varying(200),         -- 组名
    secreatedate timestamp with time zone,       -- 创建日期
    CONSTRAINT sch_event_pk PRIMARY KEY (seid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.sch_event
    OWNER TO postgres;
COMMENT ON COLUMN public.sch_event.seid IS '标识';
COMMENT ON COLUMN public.sch_event.setitle IS '标题';
COMMENT ON COLUMN public.sch_event.segroup IS '组名';
COMMENT ON COLUMN public.sch_event.secreatedate IS '创建日期';


-- Index: public.idx_sch_event_secreatedate

-- DROP INDEX public.idx_sch_event_secreatedate;

CREATE INDEX idx_sch_event_secreatedate
    ON public.sch_event
        USING btree
        (secreatedate);

-- Index: public.idx_sch_event_segroup

-- DROP INDEX public.idx_sch_event_segroup;

CREATE INDEX idx_sch_event_segroup
    ON public.sch_event
        USING btree
        (segroup COLLATE pg_catalog."default");


-- Table: public.sch_mission

-- DROP TABLE public.sch_mission;

CREATE TABLE public.sch_mission
(
    smid         bigserial NOT NULL,      -- 标识
    smtitle      character varying(4000), -- 标题
    smeventid    character varying(200),  -- 事件标识
    smtype       bigint,                  -- 类型
    smworkid     character varying(200),  -- 模型标识
    smworktitle  character varying(200),  -- 模型名称
    smparams     text,                    -- 参数
    smstatus     bigint,                  -- 状态
    smworkerid   character varying(200),  -- 执行者标识
    smmemo       text,                    -- 备注
    smreserved1  character varying(4000), -- 保留字段1
    smreserved2  character varying(4000), -- 保留字段2
    smreserved3  character varying(4000), -- 保留字段3
    smreserved4  character varying(4000), -- 保留字段4
    smreserved5  character varying(4000), -- 保留字段5
    smreserved6  character varying(4000), -- 保留字段6
    smreserved7  character varying(4000), -- 保留字段7
    smreserved8  character varying(4000), -- 保留字段8
    smreserved9  character varying(4000), -- 保留字段9
    smreserved10 character varying(4000), -- 保留字段10
    smcreatetime timestamp with time zone DEFAULT now(),
    smowner      character varying(100),  -- 任务所有者
    smexecuter   character varying(100),  -- 任务执行者
    CONSTRAINT sch_mission_pk PRIMARY KEY (smid)
)
    WITH (
        OIDS= FALSE
    );
ALTER TABLE public.sch_mission
    OWNER TO postgres;
COMMENT ON COLUMN public.sch_mission.smid IS '标识';
COMMENT ON COLUMN public.sch_mission.smtitle IS '标题';
COMMENT ON COLUMN public.sch_mission.smeventid IS '事件标识';
COMMENT ON COLUMN public.sch_mission.smtype IS '类型';
COMMENT ON COLUMN public.sch_mission.smworkid IS '模型标识';
COMMENT ON COLUMN public.sch_mission.smworktitle IS '模型名称';
COMMENT ON COLUMN public.sch_mission.smparams IS '参数';
COMMENT ON COLUMN public.sch_mission.smstatus IS '状态';
COMMENT ON COLUMN public.sch_mission.smworkerid IS '执行者标识';
COMMENT ON COLUMN public.sch_mission.smmemo IS '备注';
COMMENT ON COLUMN public.sch_mission.smreserved1 IS '保留字段1';
COMMENT ON COLUMN public.sch_mission.smreserved2 IS '保留字段2';
COMMENT ON COLUMN public.sch_mission.smreserved3 IS '保留字段3';
COMMENT ON COLUMN public.sch_mission.smreserved4 IS '保留字段4';
COMMENT ON COLUMN public.sch_mission.smreserved5 IS '保留字段5';
COMMENT ON COLUMN public.sch_mission.smreserved6 IS '保留字段6';
COMMENT ON COLUMN public.sch_mission.smreserved7 IS '保留字段7';
COMMENT ON COLUMN public.sch_mission.smreserved8 IS '保留字段8';
COMMENT ON COLUMN public.sch_mission.smreserved9 IS '保留字段9';
COMMENT ON COLUMN public.sch_mission.smreserved10 IS '保留字段10';
COMMENT ON COLUMN public.sch_mission.smowner IS '任务所有者';
COMMENT ON COLUMN public.sch_mission.smexecuter IS '任务执行者';


-- Index: public.eventid_title_idx_sch_mission

-- DROP INDEX public.eventid_title_idx_sch_mission;

CREATE INDEX eventid_title_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smeventid COLLATE pg_catalog."default", smtitle COLLATE pg_catalog."default");

-- Index: public.idx_sch_mission_smcreatetime_status

-- DROP INDEX public.idx_sch_mission_smcreatetime_status;

CREATE INDEX idx_sch_mission_smcreatetime_status
    ON public.sch_mission
        USING btree
        (smcreatetime, smstatus);

-- Index: public.smcreatetime_idx_sch_mission

-- DROP INDEX public.smcreatetime_idx_sch_mission;

CREATE INDEX smcreatetime_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smcreatetime);

-- Index: public.smeventid_idx_sch_mission

-- DROP INDEX public.smeventid_idx_sch_mission;

CREATE INDEX smeventid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smeventid COLLATE pg_catalog."default");

-- Index: public.smid_idx_sch_mission

-- DROP INDEX public.smid_idx_sch_mission;

CREATE INDEX smid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smid);

-- Index: public.smreserved1_idx_sch_mission

-- DROP INDEX public.smreserved1_idx_sch_mission;

CREATE INDEX smreserved1_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smreserved1 COLLATE pg_catalog."default");

-- Index: public.smstatus_idx_sch_mission

-- DROP INDEX public.smstatus_idx_sch_mission;

CREATE INDEX smstatus_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smstatus);

-- Index: public.smstatus_workid_idx_sch_mission

-- DROP INDEX public.smstatus_workid_idx_sch_mission;

CREATE INDEX smstatus_workid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smworkid COLLATE pg_catalog."default", smstatus);

-- Index: public.smworkerid_idx_sch_mission

-- DROP INDEX public.smworkerid_idx_sch_mission;

CREATE INDEX smworkerid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smworkerid COLLATE pg_catalog."default");

-- Index: public.stat_min_smid_idx_sch_mission

-- DROP INDEX public.stat_min_smid_idx_sch_mission;

CREATE INDEX stat_min_smid_idx_sch_mission
    ON public.sch_mission
        USING btree
        (smworkid COLLATE pg_catalog."default", smworkerid COLLATE pg_catalog."default" DESC, smid);
