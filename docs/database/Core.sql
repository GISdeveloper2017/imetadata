-- 2017-1-13 创建内核数据库

/*

-- 元数据表
ro_datacenter
ro_dbserver
ro_dict_codetable
ro_dict_codetabledata
ro_dict_field
ro_dict_table

-- 全局数据定义表
ro_global_calendar
ro_global_config
ro_global_keywords
ro_global_sequence
ro_global_sequence_recycle
ro_global_treehelp
ro_global_version

-- 权限管理表
ta_functions
ta_fungrid_field
ta_grid_field
ta_login
ta_operation
ta_org2power
ta_pvg_relation
ta_resoperate
ta_resources
ta_restype2data
ta_role2user
ta_roles
ta_table_field
ta_table_view
ta_token
ta_tokenspace
ta_users
ta_users_spatial

*/

-- Table: public.ro_global_calendar 日历，控制具体数据更新的问题，初始化至2020年

-- DROP TABLE public.ro_global_calendar;

CREATE TABLE public.ro_global_calendar
(
  gcdate date NOT NULL, -- 日期
  gcyear integer, -- 年
  gcmonth integer, -- 月
  gcdayinmonth integer, -- 一月中第几天
  gcdayinyear integer, -- 一年中第几天
  gcyearmonth character varying(200), -- 年月
  CONSTRAINT "ro_global_calendar_PK" PRIMARY KEY (gcdate)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_calendar
  OWNER TO postgres;
COMMENT ON COLUMN public.ro_global_calendar.gcdate IS '日期';
COMMENT ON COLUMN public.ro_global_calendar.gcyear IS '年';
COMMENT ON COLUMN public.ro_global_calendar.gcmonth IS '月';
COMMENT ON COLUMN public.ro_global_calendar.gcdayinmonth IS '一月中第几天';
COMMENT ON COLUMN public.ro_global_calendar.gcdayinyear IS '一年中第几天';
COMMENT ON COLUMN public.ro_global_calendar.gcyearmonth IS '年月';

-- Table: public.ro_global_config

-- DROP TABLE public.ro_global_config;

CREATE TABLE public.ro_global_config
(
  gcfgid bigint NOT NULL, -- 标示
  gcfgcode character varying(100), -- 名称
  gcfgtitle character varying(100), -- 标题
  gcfgvalue text, -- 值
  gcfgmemo character varying(1000), -- 备注
  CONSTRAINT "ro_global_config_PK" PRIMARY KEY (gcfgid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_config
  OWNER TO postgres;
COMMENT ON COLUMN public.ro_global_config.gcfgid IS '标示';
COMMENT ON COLUMN public.ro_global_config.gcfgcode IS '名称';
COMMENT ON COLUMN public.ro_global_config.gcfgtitle IS '标题';
COMMENT ON COLUMN public.ro_global_config.gcfgvalue IS '值';
COMMENT ON COLUMN public.ro_global_config.gcfgmemo IS '备注';

-- Table: public.ro_global_keywords

-- DROP TABLE public.ro_global_keywords;

CREATE TABLE public.ro_global_keywords
(
  gkid character varying(100) NOT NULL,
  gktitle character varying(2000),
  gkparentid character varying(100) NOT NULL DEFAULT '-1'::character varying,
  gkisgroup bigint NOT NULL DEFAULT 0,
  gktreecode character varying(2000),
  gktreeindex bigint NOT NULL DEFAULT 0,
  gktreelevel bigint NOT NULL DEFAULT 0,
  CONSTRAINT "ro_global_keywords_PK" PRIMARY KEY (gkid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_keywords
  OWNER TO postgres;


-- Table: public.ro_global_sequence

-- DROP TABLE public.ro_global_sequence;

CREATE TABLE public.ro_global_sequence
(
  gsid character varying(100) NOT NULL,
  gstitle character varying(100) NOT NULL,
  gsseqdatatype bigint NOT NULL DEFAULT 1,
  gsstartnumber bigint NOT NULL DEFAULT 0,
  gsendnumber bigint,
  gsposition bigint NOT NULL DEFAULT 1,
  gsprefix character varying(100),
  gssuffix character varying(100),
  gslength bigint,
  gsmemo character varying(2000),
  gsreserved bigint DEFAULT (-1),
  gssequencename character varying(200),
  gssequenceserverid character varying(100),
  CONSTRAINT "ro_global_sequence_PK" PRIMARY KEY (gsid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_sequence
  OWNER TO postgres;


-- Table: public.ro_global_sequence_recycle

-- DROP TABLE public.ro_global_sequence_recycle;

CREATE TABLE public.ro_global_sequence_recycle
(
  gsid character varying(100) NOT NULL,
  gsnumber character varying(200) NOT NULL,
  CONSTRAINT "ro_global_sequence_recycle_PK" PRIMARY KEY (gsid, gsnumber)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_sequence_recycle
  OWNER TO postgres;

-- Table: public.ro_global_treehelp

-- DROP TABLE public.ro_global_treehelp;

CREATE TABLE public.ro_global_treehelp
(
  t_tablename character varying(50) NOT NULL,
  t_idfield character varying(50),
  t_pidfield character varying(50),
  t_wbsfield character varying(50),
  t_levelfield character varying(50),
  t_orderindexfield character varying(50),
  t_orderindexenable bigint,
  CONSTRAINT "ro_global_treehelp_PK" PRIMARY KEY (t_tablename)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_treehelp
  OWNER TO postgres;

-- Table: public.ro_global_version

-- DROP TABLE public.ro_global_version;

CREATE TABLE public.ro_global_version
(
  gvid character varying(50) NOT NULL, -- 版本号
  gvdate date NOT NULL, -- 更新日期
  gvtitle character varying(200), -- 版本标题
  gvdetail text, -- 详细日志
  gvsuccess bigint, -- 更新是否成功
  CONSTRAINT "ro_global_version_PK" PRIMARY KEY (gvid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_global_version
  OWNER TO postgres;
COMMENT ON COLUMN public.ro_global_version.gvid IS '版本号';
COMMENT ON COLUMN public.ro_global_version.gvdate IS '更新日期';
COMMENT ON COLUMN public.ro_global_version.gvtitle IS '版本标题';
COMMENT ON COLUMN public.ro_global_version.gvdetail IS '详细日志';
COMMENT ON COLUMN public.ro_global_version.gvsuccess IS '更新是否成功';

-- Table: public.ro_datacenter

-- DROP TABLE public.ro_datacenter;

CREATE TABLE public.ro_datacenter
(
  dcid character varying(100) NOT NULL,
  dctitle character varying(1000),
  dcip character varying(100) NOT NULL,
  dcport numeric(22,0) NOT NULL DEFAULT 0,
  dcstatus bigint,
  dctype bigint,
  dcmemo character varying(2000),
  dclastmodifydate timestamp with time zone,
  CONSTRAINT "ro_datacenter_PK" PRIMARY KEY (dcid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_datacenter
  OWNER TO postgres;

-- Table: public.ro_dbserver

-- DROP TABLE public.ro_dbserver;

CREATE TABLE public.ro_dbserver
(
  rsid character varying(100) NOT NULL, -- 关系数据服务器标示
  rstitle character varying(100) NOT NULL, -- 关系数据服务器标题
  rsdb character varying(100) NOT NULL, -- 关系数据库database，或者oracle：sid
  rsmemo character varying(1000), -- 备注
  rsdbtype bigint NOT NULL DEFAULT 1, -- 数据库类型
  rsip character varying(100), -- 服务器ip地址
  rsport bigint, -- 端口
  rsusername character varying(100), -- 用户名
  rspassword character varying(100), -- 密码
  rsoptions character varying(2000), -- 其他链接配置
  rsminconnection bigint NOT NULL DEFAULT 1, -- 最小连接数
  rsmaxconnection bigint NOT NULL DEFAULT 1, -- 最大连接数
  rsschema character varying(100), -- 数据库schema，oracle：用户名；sqlserver：dbo；其他：databasename
  rsdcid character varying(100), -- 关系数据中心标示
  rsdesignparams text, -- 设计参数
  CONSTRAINT "ro_dbserver_PK" PRIMARY KEY (rsid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_dbserver
  OWNER TO postgres;
COMMENT ON COLUMN public.ro_dbserver.rsid IS '关系数据服务器标示';
COMMENT ON COLUMN public.ro_dbserver.rstitle IS '关系数据服务器标题';
COMMENT ON COLUMN public.ro_dbserver.rsdb IS '关系数据库database，或者oracle：sid';
COMMENT ON COLUMN public.ro_dbserver.rsmemo IS '备注';
COMMENT ON COLUMN public.ro_dbserver.rsdbtype IS '数据库类型';
COMMENT ON COLUMN public.ro_dbserver.rsip IS '服务器ip地址';
COMMENT ON COLUMN public.ro_dbserver.rsport IS '端口';
COMMENT ON COLUMN public.ro_dbserver.rsusername IS '用户名';
COMMENT ON COLUMN public.ro_dbserver.rspassword IS '密码';
COMMENT ON COLUMN public.ro_dbserver.rsoptions IS '其他链接配置';
COMMENT ON COLUMN public.ro_dbserver.rsminconnection IS '最小连接数';
COMMENT ON COLUMN public.ro_dbserver.rsmaxconnection IS '最大连接数';
COMMENT ON COLUMN public.ro_dbserver.rsschema IS '数据库schema，oracle：用户名；sqlserver：dbo；其他：databasename';
COMMENT ON COLUMN public.ro_dbserver.rsdcid IS '关系数据中心标示';
COMMENT ON COLUMN public.ro_dbserver.rsdesignparams IS '设计参数';

-- Table: public.ro_dict_codetable

-- DROP TABLE public.ro_dict_codetable;

CREATE TABLE public.ro_dict_codetable
(
  codetableid character varying(100) NOT NULL,
  codetabletitle character varying(100),
  codetabletype bigint NOT NULL DEFAULT 1,
  codetablesql text,
  codetablememo character varying(1000),
  codetableistree bigint NOT NULL DEFAULT 0,
  codetableclass bigint NOT NULL DEFAULT 0,
  codetableserverid character varying(100) NOT NULL DEFAULT '-1'::character varying,
  CONSTRAINT "ro_dict_codetable_PK" PRIMARY KEY (codetableid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_dict_codetable
  OWNER TO postgres;

-- Table: public.ro_dict_codetabledata

-- DROP TABLE public.ro_dict_codetabledata;

CREATE TABLE public.ro_dict_codetabledata
(
  codetableid character varying(100) NOT NULL,
  code character varying(100) NOT NULL,
  chnname character varying(100),
  isdefault bigint NOT NULL DEFAULT 0,
  isreserved bigint NOT NULL DEFAULT 0,
  parentcode character varying(100) DEFAULT '-1'::character varying,
  isgroup bigint NOT NULL DEFAULT 0,
  codeallowselect bigint NOT NULL DEFAULT (-1),
  wbscode character varying(2000),
  CONSTRAINT "ro_dict_codetabledata_PK" PRIMARY KEY (codetableid, code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_dict_codetabledata
  OWNER TO postgres;

-- Table: public.ro_dict_field

-- DROP TABLE public.ro_dict_field;

CREATE TABLE public.ro_dict_field
(
  fieldid character varying(100) NOT NULL,
  tableserverid character varying(100) NOT NULL,
  tablename character varying(100) NOT NULL,
  fieldname character varying(100) NOT NULL,
  fieldchnname character varying(100),
  fieldsize bigint NOT NULL DEFAULT 15,
  fieldtype bigint NOT NULL DEFAULT 1,
  codetableid character varying(100),
  fieldmemo character varying(1000),
  fieldscale bigint NOT NULL DEFAULT 2,
  fieldformat character varying(100),
  fieldcreateverid bigint NOT NULL DEFAULT 0,
  fieldrequired bigint NOT NULL DEFAULT 0,
  fieldiskey bigint NOT NULL DEFAULT 0,
  multicodetable bigint NOT NULL DEFAULT 0,
  fieldseqid character varying(100),
  fieldrule bigint NOT NULL DEFAULT 0,
  fieldposition bigint NOT NULL DEFAULT 0,
  fielddefaultvalue character varying(1000),
  fielddbtype character varying(100),
  CONSTRAINT "ro_dict_field_PK" PRIMARY KEY (fieldid, tableserverid, tablename)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_dict_field
  OWNER TO postgres;

-- Table: public.ro_dict_table

-- DROP TABLE public.ro_dict_table;

CREATE TABLE public.ro_dict_table
(
  tableid character varying(100) NOT NULL, -- 主键id
  tablechnname character varying(100) NOT NULL, -- 表中文名
  tablename character varying(100) NOT NULL, -- 表名称
  tablesql text, -- 表sql
  tabletype bigint NOT NULL DEFAULT 1, -- 表类型
  tableclass bigint NOT NULL DEFAULT 1, -- 表样式
  tablekind bigint, -- 数据表风格
  tablecreateverid bigint NOT NULL DEFAULT 0, -- 表版本
  tableserverid character varying(100) NOT NULL DEFAULT '-1'::character varying, -- 表服务器id
  tablememo character varying(1000), -- 表描述
  CONSTRAINT "ro_dict_table_PK" PRIMARY KEY (tableid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ro_dict_table
  OWNER TO postgres;
COMMENT ON COLUMN public.ro_dict_table.tableid IS '主键id';
COMMENT ON COLUMN public.ro_dict_table.tablechnname IS '表中文名';
COMMENT ON COLUMN public.ro_dict_table.tablename IS '表名称';
COMMENT ON COLUMN public.ro_dict_table.tablesql IS '表sql';
COMMENT ON COLUMN public.ro_dict_table.tabletype IS '表类型';
COMMENT ON COLUMN public.ro_dict_table.tableclass IS '表样式';
COMMENT ON COLUMN public.ro_dict_table.tablekind IS '数据表风格';
COMMENT ON COLUMN public.ro_dict_table.tablecreateverid IS '表版本';
COMMENT ON COLUMN public.ro_dict_table.tableserverid IS '表服务器id';
COMMENT ON COLUMN public.ro_dict_table.tablememo IS '表描述';

-- Table: public.ta_functions

-- DROP TABLE public.ta_functions;

CREATE TABLE public.ta_functions
(
  fid bigint NOT NULL,
  ftitle character varying(1000),
  fparentid bigint NOT NULL,
  fisgroup bigint NOT NULL,
  fwbscode character varying(1000),
  furl character varying(1000),
  fresoperatetype bigint,
  ftype bigint NOT NULL DEFAULT 1,
  frestype bigint,
  fsql text,
  fimage character varying(600),
  forderindex bigint,
  ftreelevel bigint,
  CONSTRAINT ta_functions_pk PRIMARY KEY (fid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_functions
  OWNER TO postgres;


-- Table: public.ta_fungrid_field

-- DROP TABLE public.ta_fungrid_field;

CREATE TABLE public.ta_fungrid_field
(
  id character varying(64) NOT NULL, -- 主键
  funcid character varying(100) NOT NULL, -- 功能主键
  fieldchname character varying(100), -- 字段中文名
  fieldwidth bigint, -- 字段宽度
  fieldtype character varying(20), -- 字段类型
  sortable character varying(20), -- 是否排序
  allowblank character varying(20), -- 是否为空
  renderer character varying(64), -- 方法名
  showable character varying(20), -- 是否显示
  fieldname character varying(100), -- 字段名
  fieldsql character varying(500), -- 字段查询sql
  fieldindex bigint, -- 字段排序
  CONSTRAINT ta_fungrid_field_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_fungrid_field
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_fungrid_field.id IS '主键';
COMMENT ON COLUMN public.ta_fungrid_field.funcid IS '功能主键';
COMMENT ON COLUMN public.ta_fungrid_field.fieldchname IS '字段中文名';
COMMENT ON COLUMN public.ta_fungrid_field.fieldwidth IS '字段宽度';
COMMENT ON COLUMN public.ta_fungrid_field.fieldtype IS '字段类型';
COMMENT ON COLUMN public.ta_fungrid_field.sortable IS '是否排序';
COMMENT ON COLUMN public.ta_fungrid_field.allowblank IS '是否为空';
COMMENT ON COLUMN public.ta_fungrid_field.renderer IS '方法名';
COMMENT ON COLUMN public.ta_fungrid_field.showable IS '是否显示';
COMMENT ON COLUMN public.ta_fungrid_field.fieldname IS '字段名';
COMMENT ON COLUMN public.ta_fungrid_field.fieldsql IS '字段查询sql';
COMMENT ON COLUMN public.ta_fungrid_field.fieldindex IS '字段排序';


-- Table: public.ta_grid_field

-- DROP TABLE public.ta_grid_field;

CREATE TABLE public.ta_grid_field
(
  id character varying(64) NOT NULL, -- 主键
  fieldname character varying(100) NOT NULL, -- 字段名称
  fieldchname character varying(100), -- 字段中文名
  tablename character varying(100) NOT NULL, -- 表名
  dbserverid character varying(64), -- 数据库服务器主键
  fieldwidth bigint, -- 字段宽度
  fieldtype character varying(20), -- 字段类型
  sortable character varying(20), -- 是否可排序
  allowblank character varying(20), -- 是否可以为空
  renderer character varying(64), -- 方法名
  showable character varying(20), -- 是否显示
  funcid character varying(100),
  CONSTRAINT ta_grid_field_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_grid_field
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_grid_field.id IS '主键';
COMMENT ON COLUMN public.ta_grid_field.fieldname IS '字段名称';
COMMENT ON COLUMN public.ta_grid_field.fieldchname IS '字段中文名';
COMMENT ON COLUMN public.ta_grid_field.tablename IS '表名';
COMMENT ON COLUMN public.ta_grid_field.dbserverid IS '数据库服务器主键';
COMMENT ON COLUMN public.ta_grid_field.fieldwidth IS '字段宽度';
COMMENT ON COLUMN public.ta_grid_field.fieldtype IS '字段类型';
COMMENT ON COLUMN public.ta_grid_field.sortable IS '是否可排序';
COMMENT ON COLUMN public.ta_grid_field.allowblank IS '是否可以为空';
COMMENT ON COLUMN public.ta_grid_field.renderer IS '方法名';
COMMENT ON COLUMN public.ta_grid_field.showable IS '是否显示';


-- Table: public.ta_login

-- DROP TABLE public.ta_login;

CREATE TABLE public.ta_login
(
  lid character varying(100) NOT NULL,
  luserid character varying(100) NOT NULL,
  loginname character varying(100) NOT NULL,
  password character varying(100),
  logintitle character varying(1000),
  ltype bigint DEFAULT 0,
  lmobilephone character varying(20), -- 移动电话
  lphone character varying(20), -- 固定电话
  lemail character varying(512), -- 电子邮件
  loginflag character varying(64), -- 登录标示
  loginwrongtimes bigint, -- 登录错误次数
  loginwrongdate character varying(100), -- 登录错误日期
  lsex character varying(2), -- 性别
  lidcard character varying(20),
  laddress character varying(100),
  CONSTRAINT "ta_login_PK" PRIMARY KEY (lid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_login
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_login.lmobilephone IS '移动电话';
COMMENT ON COLUMN public.ta_login.lphone IS '固定电话';
COMMENT ON COLUMN public.ta_login.lemail IS '电子邮件';
COMMENT ON COLUMN public.ta_login.loginflag IS '登录标示';
COMMENT ON COLUMN public.ta_login.loginwrongtimes IS '登录错误次数';
COMMENT ON COLUMN public.ta_login.loginwrongdate IS '登录错误日期';
COMMENT ON COLUMN public.ta_login.lsex IS '性别';

-- Table: public.ta_operation

-- DROP TABLE public.ta_operation;

CREATE TABLE public.ta_operation
(
  optid character varying(64) NOT NULL, -- 主键
  opttitle character varying(512) NOT NULL, -- 按钮中文名
  optname character varying(256) NOT NULL, -- 按钮英文名
  opticon character varying(256), -- 图标名
  opthandler character varying(256), -- 按钮调用方法名
  optdescription character varying(1000), -- 描述
  optfuncid character varying(64), -- 功能主键
  optservername character varying(256), -- 服务器名称
  optlastmodifytime character varying(100), -- 最后修改时间
  optindex character varying(64), -- 按键排序
  optstatus bigint DEFAULT (-1), -- 功能状态
  CONSTRAINT ta_operation_pk PRIMARY KEY (optid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_operation
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_operation.optid IS '主键';
COMMENT ON COLUMN public.ta_operation.opttitle IS '按钮中文名';
COMMENT ON COLUMN public.ta_operation.optname IS '按钮英文名';
COMMENT ON COLUMN public.ta_operation.opticon IS '图标名';
COMMENT ON COLUMN public.ta_operation.opthandler IS '按钮调用方法名';
COMMENT ON COLUMN public.ta_operation.optdescription IS '描述';
COMMENT ON COLUMN public.ta_operation.optfuncid IS '功能主键';
COMMENT ON COLUMN public.ta_operation.optservername IS '服务器名称';
COMMENT ON COLUMN public.ta_operation.optlastmodifytime IS '最后修改时间';
COMMENT ON COLUMN public.ta_operation.optindex IS '按键排序';
COMMENT ON COLUMN public.ta_operation.optstatus IS '功能状态';

-- Table: public.ta_org2power

-- DROP TABLE public.ta_org2power;

CREATE TABLE public.ta_org2power
(
  uroid character varying(100) NOT NULL,
  urotype bigint NOT NULL,
  urpid bigint NOT NULL,
  urptype bigint NOT NULL,
  uroperatetype bigint NOT NULL,
  urcount bigint NOT NULL DEFAULT 1,
  urrecursive character varying(1)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_org2power
  OWNER TO postgres;


-- Table: public.ta_pvg_relation

-- DROP TABLE public.ta_pvg_relation;

CREATE TABLE public.ta_pvg_relation
(
  roleid character varying(100) NOT NULL,
  userid character varying(100) NOT NULL,
  rtype bigint NOT NULL,
  rucount bigint,
  rurecursive character varying(1),
  CONSTRAINT "ta_pvg_relation_PK" PRIMARY KEY (roleid, userid, rtype)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_pvg_relation
  OWNER TO postgres;

-- Table: public.ta_resoperate

-- DROP TABLE public.ta_resoperate;

CREATE TABLE public.ta_resoperate
(
  roid bigint NOT NULL,
  rotitle character varying(100),
  rourl character varying(1000),
  rortype bigint,
  CONSTRAINT ta_resoperate_pk PRIMARY KEY (roid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_resoperate
  OWNER TO postgres;

-- Table: public.ta_resources

-- DROP TABLE public.ta_resources;

CREATE TABLE public.ta_resources
(
  rid character varying(100) NOT NULL,
  rtitle character varying(1000) NOT NULL,
  rparentid character varying(100) NOT NULL,
  risgroup bigint NOT NULL,
  rtreecode character varying(2000),
  rtype bigint NOT NULL,
  robjectid character varying(2000) NOT NULL,
  rtreelevel bigint,
  rimage character varying(200),
  rversion bigint,
  rextension character varying(4000),
  CONSTRAINT ta_resources_pk PRIMARY KEY (rid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_resources
  OWNER TO postgres;

-- Table: public.ta_restype2data

-- DROP TABLE public.ta_restype2data;

CREATE TABLE public.ta_restype2data
(
  rdtypeid bigint NOT NULL,
  rdtypetitle character varying(100),
  rdtreecode character varying(20),
  rdtypeversion bigint,
  rdtypeaddrtype bigint,
  rdtypeaddr text,
  CONSTRAINT ta_restype2data_pk PRIMARY KEY (rdtypeid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_restype2data
  OWNER TO postgres;


-- Table: public.ta_role2user

-- DROP TABLE public.ta_role2user;

CREATE TABLE public.ta_role2user
(
  roleid character varying(100) NOT NULL,
  userid character varying(100) NOT NULL,
  rtype bigint NOT NULL, -- null:usergroup,1:user
  rucount bigint,
  rurecursive character varying(1),
  CONSTRAINT "ta_role2user_PK" PRIMARY KEY (roleid, userid, rtype)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_role2user
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_role2user.rtype IS 'null:usergroup,1:user';

-- Table: public.ta_roles

-- DROP TABLE public.ta_roles;

CREATE TABLE public.ta_roles
(
  roleid character varying(100) NOT NULL,
  roletitle character varying(100),
  roletype bigint DEFAULT 0,
  roledesc character varying(1000),
  CONSTRAINT "ta_roles_PK" PRIMARY KEY (roleid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_roles
  OWNER TO postgres;

-- Table: public.ta_table_field

-- DROP TABLE public.ta_table_field;

CREATE TABLE public.ta_table_field
(
  tablefieldid character varying(200),
  tablefieldwidth bigint DEFAULT 200, -- 显示宽度
  tablefieldshowable bigint -- 是否显示
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_table_field
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_table_field.tablefieldwidth IS '显示宽度';
COMMENT ON COLUMN public.ta_table_field.tablefieldshowable IS '是否显示';


-- Table: public.ta_table_view

-- DROP TABLE public.ta_table_view;

CREATE TABLE public.ta_table_view
(
  tvid bigserial NOT NULL , -- 主键
  tblname character varying(100), -- 表名称
  vidname character varying(100), -- 视图id字段名
  vtitlename character varying(100), -- 视图title字段名
  vxname character varying(100), -- 视图x字段名
  vyname character varying(100), -- 视图y字段名
  vshpname character varying(100), -- 视图shape字段名
  tblchnname character varying(100), -- 表中文名，即视图type字段值
  tvremark character varying(1000), -- 备注信息
  tvmodifytime timestamp without time zone, -- 更新时间
  CONSTRAINT ta_table_view_pk PRIMARY KEY (tvid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_table_view
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_table_view.tvid IS '主键';
COMMENT ON COLUMN public.ta_table_view.tblname IS '表名称';
COMMENT ON COLUMN public.ta_table_view.vidname IS '视图id字段名';
COMMENT ON COLUMN public.ta_table_view.vtitlename IS '视图title字段名';
COMMENT ON COLUMN public.ta_table_view.vxname IS '视图x字段名';
COMMENT ON COLUMN public.ta_table_view.vyname IS '视图y字段名';
COMMENT ON COLUMN public.ta_table_view.vshpname IS '视图shape字段名';
COMMENT ON COLUMN public.ta_table_view.tblchnname IS '表中文名，即视图type字段值';
COMMENT ON COLUMN public.ta_table_view.tvremark IS '备注信息';
COMMENT ON COLUMN public.ta_table_view.tvmodifytime IS '更新时间';


-- Table: public.ta_token

-- DROP TABLE public.ta_token;

CREATE TABLE public.ta_token
(
  tid character varying(100) NOT NULL, -- token标识
  tname character varying(100), -- token名称
  tstartdate character varying(50), -- 开始时间
  tenddate character varying(50), -- 结束时间
  tstatus bigint DEFAULT 0, -- token状态
  tip character varying(15), -- 访问地址
  gid character varying(100), -- 用户组标示
  ttype character varying(50), -- token类型
  thttprefer character varying(50), -- token http refer
  tapplicant character varying(50), -- Token申请人
  ttitle character varying(50),
  CONSTRAINT "ta_token_PK" PRIMARY KEY (tid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_token
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_token.tid IS 'token标识';
COMMENT ON COLUMN public.ta_token.tname IS 'token名称';
COMMENT ON COLUMN public.ta_token.tstartdate IS '开始时间';
COMMENT ON COLUMN public.ta_token.tenddate IS '结束时间';
COMMENT ON COLUMN public.ta_token.tstatus IS 'token状态';
COMMENT ON COLUMN public.ta_token.tip IS '访问地址';
COMMENT ON COLUMN public.ta_token.gid IS '用户组标示';
COMMENT ON COLUMN public.ta_token.ttype IS 'token类型';
COMMENT ON COLUMN public.ta_token.thttprefer IS 'token http refer';
COMMENT ON COLUMN public.ta_token.tapplicant IS 'Token申请人';


-- Table: public.ta_tokenspace

-- DROP TABLE public.ta_tokenspace;

CREATE TABLE public.ta_tokenspace
(
  tsid character varying(100) NOT NULL,
  tid character varying(100), -- token标识
  gdsid character varying(50), -- 空间维度id
  CONSTRAINT ta_tokenspace_pk PRIMARY KEY (tsid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_tokenspace
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_tokenspace.tid IS 'token标识';
COMMENT ON COLUMN public.ta_tokenspace.gdsid IS '空间维度id';

-- Table: public.ta_users

-- DROP TABLE public.ta_users;

CREATE TABLE public.ta_users
(
  userid character varying(100) NOT NULL, -- 组织机构标示
  userparentid character varying(100) NOT NULL DEFAULT '-1'::character varying, -- 组织机构父标示
  userisgroup bigint NOT NULL DEFAULT 0, -- 是否分组
  userwbscode character varying(1000), -- 组织机构树编码
  usertitle character varying(100), -- 组织机构名称
  usermemo character varying(1000), -- 组织机构备注
  usertype bigint NOT NULL DEFAULT 0, -- 组织机构类型
  userimage character varying(600), -- 节点图标
  userorderindex bigint, -- 排序编号
  usertreelevel bigint, -- 组织机构树层级
  userbuildintype bigint DEFAULT 0, -- 组织机构内置类型
  usercode character varying(50), -- 组织机构编码
  userips character varying(50), -- ip地址段
  CONSTRAINT "ta_users_PK" PRIMARY KEY (userid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_users
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_users.userid IS '组织机构标示';
COMMENT ON COLUMN public.ta_users.userparentid IS '组织机构父标示';
COMMENT ON COLUMN public.ta_users.userisgroup IS '是否分组';
COMMENT ON COLUMN public.ta_users.userwbscode IS '组织机构树编码';
COMMENT ON COLUMN public.ta_users.usertitle IS '组织机构名称';
COMMENT ON COLUMN public.ta_users.usermemo IS '组织机构备注';
COMMENT ON COLUMN public.ta_users.usertype IS '组织机构类型';
COMMENT ON COLUMN public.ta_users.userimage IS '节点图标';
COMMENT ON COLUMN public.ta_users.userorderindex IS '排序编号';
COMMENT ON COLUMN public.ta_users.usertreelevel IS '组织机构树层级';
COMMENT ON COLUMN public.ta_users.userbuildintype IS '组织机构内置类型';
COMMENT ON COLUMN public.ta_users.usercode IS '组织机构编码';
COMMENT ON COLUMN public.ta_users.userips IS 'ip地址段';


-- Table: public.ta_users_spatial

-- DROP TABLE public.ta_users_spatial;

CREATE TABLE public.ta_users_spatial
(
  user_id character varying(100) NOT NULL, -- 组织机构主键
  gds_id character varying(100) NOT NULL, -- 空间对象主键
  CONSTRAINT "ta_users_spatial_PK" PRIMARY KEY (user_id, gds_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.ta_users_spatial
  OWNER TO postgres;
COMMENT ON COLUMN public.ta_users_spatial.user_id IS '组织机构主键';
COMMENT ON COLUMN public.ta_users_spatial.gds_id IS '空间对象主键';

