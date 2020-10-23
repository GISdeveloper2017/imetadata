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

comment on table dm2_storage_inbound_log is '数管-入库';

comment on column dm2_storage_inbound_log.dsilid is '标识';
comment on column dm2_storage_inbound_log.dsilownerid is '所属入库记录标识';
comment on column dm2_storage_inbound_log.dsildirectory is '目录';
comment on column dm2_storage_inbound_log.dsilfilename is '文件名';
comment on column dm2_storage_inbound_log.dsilobjectname is '对象名';
comment on column dm2_storage_inbound_log.dsilobjecttype is '对象类型';
comment on column dm2_storage_inbound_log.dsiladdtime is '添加时间';
comment on column dm2_storage_inbound_log.dsilinbound is '是否允许入库';
alter table dm2_storage_inbound_log owner to postgres;

