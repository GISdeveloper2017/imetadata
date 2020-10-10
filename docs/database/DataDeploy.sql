/*
	数据发布
	2020-6-10
	v1.0
	王西亚
	
	。数据库及插件要求
	[x] postgresql 9.4
	[x] postgis
	[x] uuid-ossp
	
日志：
。2020-6-10  
	。初始版本
       。数据发布服务基本模型：
         。数据发布模板_xxx_Schema
           。定义数据发布的配置
           。由数据发布研发工程师配置
         。数据发布定义_xxx_Define
           。数据发布的任务的定义
           。由系统自动扫描获取
         。数据发布定义_xxx_Define_files
           。数据发布搜索适配的文件
           。由系统自动扫描获取
         。数据发布实例_xxx
           。数据发布的具体实例
           。由系统自动生成
         。数据发布数据明细_xxx_Detail
           。数据发布所需要的各类数据
           。由系统自动生成
	。第一个服务
      。全覆盖矢量数据展示服务
        。解决全覆盖数据，按地类进行自动分割，并发布单个服务
        。数据发布模板：
          。dp_v_qfg_schema：服务模板，描述每一个服务的创建方法
          。dp_v_qfg_schema_Layer：服务图层模板，描述服务的每一个图层对应的数据对象和处理办法
        。数据发布定义：
          。dp_v_qfg
        。数据发布定义的文件：
          。dp_v_qfg_layer
        。数据发布实例：
          。dp_v_qfg
        。数据发布数据明细：
          。dp_v_qfg_detail
        。数据发布算法：
          。在数据发布数据库服务中的at_tasks和at_subtasks
		。并行处理设计
		  。并行调度一：
		    。根据schema的状态，更新dp_v_qfg表，并对上次已经发布的记录，进行更新，标记其中的
              增、删和修改
            。并行处理（1）：并行处理状态为1的schema，根据配置，修正dp_v_qfg中的记录，最后将dp_v_qfg记录的状态改为1，启动并行调度二；
              成功完成后，将自己的状态改为0；
              失败改为21，等待人员手工处理；
              如果人工修正后，请将状态恢复为1，等待系统自动检查修正重启；
		  。并行调度二：
		    。根据dp_v_qfg的状态，进行发布前预处理，结合schema_layer表中的定义，检查并修正dp_v_qfg_layer记录
        。并行处理（n）：
          并行处理状态为1的dp_v_qfg，处理过程中状态为2
          根据dpserviceparams中的配置，对before预处理节点进行处理
          根据schema_layer表中的定义，检查并修正dp_v_qfg_layer记录，
          最后将dp_v_qfg_layer记录的状态改为1，启动并行调度三；
          同时，将dp_v_qfg的状态修改为3，启动定时器的自动检查逻辑
          成功完成本步骤后，状态保持为2不变，交由定时器去检查处理！！！
          如果本步骤失败，则状态改为21，等待人工处理；
          如果人工修正后，请将状态恢复为1，等待系统自动检查修正重启
		    。定时器：
          。判断所有状态为3的dp_v_qfg，是否所有Layer图层全部成功处理完成，则将dp_v_qfg的状态改为4，以启动并行调度五；
          。如果下属的图层数为0，则将dp_v_qfg的状态改为31，等待人工处理；
           如果有失败的，否则改为31，等待人工处理；
           如果人工修正后，请将状态恢复为3，等待系统自动检查修正重启
      。并行调度三：
        。根据dp_v_qfg_layer的状态，结合schema_layer表中的定义，检查并修正dp_v_qfg_layer_file记录
        。并行处理（n）：
          并行处理状态为1的dp_v_qfg_layer，处理过程中状态为2，根据schema_layer表中的定义，检查并修正dp_v_qfg_layer记录，
          最后将dp_v_qfg_layer_file记录的状态改为1，启动并行调度四；
          同时，将dp_v_qfg_layer的状态修改为3，启动定时器的自动检查逻辑
          成功完成本步骤后，状态保持为2不变，交由定时器去检查处理！！！
          如果本步骤失败，则状态改为21，等待人工处理；
          如果人工修正后，请将状态恢复为1，等待系统自动检查修正重启
        。定时器：
          判断所有状态为3的dp_v_qfg_layer，是否所有Layer_file全部成功处理完成，则将dp_v_qfg_layer的状态改为0；
          如果有失败的，否则改为31，等待人工处理；
          如果人工修正后，请将状态恢复为3，等待系统自动检查修正重启
      。并行调度四：
        。根据dp_v_qfg_layer_file的状态，处理当前图层的记录文件
        。定时器：无
        。并行处理（n）：并行处理状态为1的dp_v_qfg_layer_file记录开始处理，处理过程中状态为2，成功的改为0，失败的改为21；
          如果人工修正后，请将状态恢复为1，等待系统自动检查修正重启
      。人工调度：
        。针对状态为4的dp_v_qfg，人工检查数据生成的状态、记录的正确性
        。如无问题，可以交付发布，将dp_v_qfg的状态改为5；
      。并行调度五
        。根据dp_v_qfg的状态，进行发布后处理，创建服务发布xml，提交服务发布服务器运行
        。并行处理（n）：并行处理状态为5的dp_v_qfg，处理过程中状态为6，创建服务发布xml，提交服务发布服务器运行
          成功完成本步骤后，状态改为7；
          如果本步骤失败，则状态改为61，等待人工处理；
          如果人工修正后，请将状态恢复为5，等待系统自动检查修正重启
      。并行调度六：
        。根据dp_v_qfg的状态，检查服务发布中心是否完成服务发布工作，并同步
        。并行处理（n）：并行处理状态为7的dp_v_qfg，处理过程中状态为8，检查服务中心的任务执行状态，如果成功完成，则将本服务状态设置为完成
          成功完成本步骤后，状态为0；
          如果本步骤失败，比如数据库无法连接，找不到任务记录，则状态改为81，等待人工处理；
          如果人工修正，请将状态恢复为7，等待系统自动检查修正重启
。2020-6-20  
  。扩展服务模式：
    。支持对特定对象类型进行发布，对象类型支持多选
    。支持影像服务的发布，在无文件处理算法时，系统将把文件位置直接发给服务发布中心
      。注意：这时，要使用dm2_Storage的dstotheroption配置属性，其中有当前Storage在Linux中Mount点的路径。
  。BugFix：
    。如果一个服务下没有图层，则服务不能发布，状态改为31，并附加错误提示。
    。如果一个图层下没有文件，图层允许直接设置为成功完成。
    。较上次发布，被删除的服务、图层和文件，将不再处理。
。2020-6-30
  。扩展服务模式：
    。考虑支持数据统计算法
      。将dp_v_qfg作为服务
      。将dp_v_qfg_Layer作为数据处理分组
      。将dp_v_qfg_Layer_File作为数据处理明细
    。需要扩展dp_v_qfg作为通用服务的职能，增加服务发布前、发布后的处理逻辑，该处理逻辑，需要和business结合，以免有复杂的处理！


。服务整理：
  。dp_v_qfg_schema
    。dpproject
      。发布目标服务坐标投影
      。格式：json数组
      。举例：[{"project":"EPSG:4326"},{"project":"EPSG:3857"}]
    。dpbatchdeploy
      。批量发布的配置
      。批量发布主要根据时间、业务、空间三个维度，与ro_global_xxx这套表配合进行批量发布
      。格式：json数组
      。举例：[{"dim_time":"t0","dim_spatial":"","dim_bus":""}]
      。备注：
        。每一个维度，都是指父节点，系统将批量处理父节点下的所有一级子节点；上例中说明的是发布所有父节点为t0的时间维度；空间维度和业务维度不处理
        。多个维度的匹配模式，可以设计多个；以json数组的形式存储
    。dpDeployDir
      。数据发布的目标目录
      。也可能是数据统计时的工作目录
    。dpFilePrefix 
      。发布目标文件的前缀
      。为了支持和linux服务器对接，本系统的目录dpDeployDir，和第三方系统的目录对应需要有一个特殊路径，比如共享名称或者mount的路径，这里进行适配
    。dpServiceType
      。wmts
        。影像或矢量的展示服务，发布服务内容将以wms和wmts为主，具体参见发布中心的技术指标
        。该模式下，系统将和发布中心对接。在调度5中，将发布命令参数发布给发布中心。
      。stat
        。统计。系统将对数据进行统计，并根据文件处理算法，将结果存储到数据库中
        。该模式下，系统不会和发布中心对接。
    。dpserviceparams
      。服务发布参数，可以对服务发布前和发布完毕后，进行特定的处理
      。结构：xml
      。样例：
<?xml version="1.0" encoding="gbk"?>
<process>
  <before hint="在服务发布前处理">
    <serverid>-1</serverid>
    <type>sql</type>
    <content><![CDATA[
delete from a_stat
    ]]></content>
  </before>
  <after hint="在服务中的每一个数据处理完之后处理">
    <serverid>-1</serverid>
    <type>sql</type>
    <content/>
  </after>
</process>

      。说明：
        。before：服务发布前处理
        。after：服务发布后处理
        。下一级节点：
          。type：
            。sql：处理的命令为sql；多个sql可以使用分号隔开
            。business：业务命令，可调用特定的业务流程
          。content：根据type类型不同，存储sql，或者业务命令的名称
          。serverid：处理sql时的数据库，仅仅在type=sql时有效
  。dp_v_qfg_schema_layer
    。在发布geo服务时，本表是图层的配置；在进行数据统计时，本表为数据统计组
    。dpdeploysubdir
      。当前数据处理后的子目录，便于归档管理
    。dpfiletags
      。可用的文件的标签
      。格式：字符串数组
      。可存储多个标签，则包含这多个标签的文件，才作为处理文件
    。dpobjecttype
      。对象类型
      。对应objecttype
      。符合这些对象类型的文件，才被处理
      。格式：字符串数组
      。对象类型在数组中的，将被处理
    。dpfileprocessalgorithm
      。文件处理算法
      。保持为空，意味着直接将原始文件发布
      。其他算法如下：
        。含.py的，将作为python算法处理
          。系统将调用<系统安装目录>\Template\python\qgis的python文件进行处理
          。vector_extract_row.py：将矢量处理为shp文件（utf8格式）
          。vector_extract_row_gpkg.py：将矢量处理geopackage文件
        。shapefile_sql：
          。针对shpFile的dbf进行数据统计
          。统计的SQL语句，在dpfileprocessparams中配置
          。调用sql语句，查询出结果
          。结果的每一条，将调用dpfileprocessparams的处理配置，进行处理，继续调用sql入库或调用business
        。vector_transform_sql：
          。将矢量转换为geopackage，然后进行使用sqlite引擎进行数据统计
          。统计的SQL语句，在dpfileprocessparams中配置
          。调用sql语句，查询出结果
          。结果的每一条，将调用dpfileprocessparams的处理配置，进行处理，继续调用sql入库或调用business
        。vector_analyse_refer_1_1：
          。一对一分析服务
          。通过标签和对象类型，获取分析参考数据
          。设置运行参数，作为数据挖掘的数据命令行输入模板
          。根据算法处理，生成目标文件geopackage
          。转换为geopackage，然后进行使用sqlite引擎进行数据统计
            。如果有stat节点，则使用stat节点内的sql，使用sqlite引擎查询数据
            。如果没有stat节点，则使用ogr方式打开数据集，使用内存数据集查询数据
          。结果的每一条，将调用dpfileprocessparams的处理配置，进行处理，继续调用sql入库或调用business
    。dpfileprocessparams
      。文件处理参数
      。格式：xml
      。样例：
<?xml version="1.0" encoding="gbk"?>
<process>
  <refer refer_object_tags="{现状数据, 2019}" refer_object_type="{shp}"/>
  <commandline name="xxx.py"> -output_field_1 JDMC -output_field_2 cc -inputfilename $inputfilename$ -ref_filename $ref_filename$</commandline>
  <stat comment="统计方法"><![CDATA[
select dlmc as subgroup, count(*) as stat_count, sum(tbmj) as stat_sum_area from $tablename$ group by dlmc
  ]]></stat>
  <before comment="处理当前数据文件前的操作">
    <serverid>-1</serverid>
    <type>sql</type>
    <content><![CDATA[
delete from a_stat where sgroup = :query_file_object_id
    ]]></content>
  </before>
  <record comment="每一条统计结果，系统按如下方式处理">
    <serverid>-1</serverid>
    <type>sql</type>
    <content><![CDATA[
insert into a_stat(sgroup, subgroup, stat_count, stat_sum_area) values(:query_file_object_id, :subgroup, :stat_count, :stat_sum_area)
    ]]></content>
  </record>
  <after comment="处理当前数据文件后的操作">
    <serverid>-1</serverid>
    <type>sql</type>
    <content/>
  </after>
</process>

      。说明：
        。stat：统计方法
          。其中tablename作为参数，将在不同文件处理时，被系统替换
        。record：
          。每一条统计结果，系统按方式要求处理
          。下一级节点：
            。type：
              。sql：处理的命令为sql；多个sql可以使用分号隔开
              。business：业务命令，可调用特定的业务流程
              。node：命令节点，content可以直接作为命令节点运行，等同于command
            。content：根据type类型不同，存储sql，或者业务命令的名称
            。serverid：处理sql时的数据库，仅仅在type=sql时有效
  		

*/

-- Table: public.dp_v_qfg_schema

-- DROP TABLE public.dp_v_qfg_schema;

CREATE TABLE public.dp_v_qfg_schema
(
    dpid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpstatus integer DEFAULT 1,
    dpprocessid character varying(100) COLLATE pg_catalog."default",
    dpaddtime timestamp(6) without time zone DEFAULT now(),
    dplastmodifytime timestamp(6) without time zone DEFAULT now(),
    dpmemo character varying(200) COLLATE pg_catalog."default",
    dptitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dptargettitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dptargetname character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dpdeploydir character varying(2000) COLLATE pg_catalog."default",
    dpfileprefix character varying(2000) COLLATE pg_catalog."default",
    dpproject character varying(2000) COLLATE pg_catalog."default",
    dpbatchdeploy character varying(2000) COLLATE pg_catalog."default",
    dpprocesstype character varying(100) COLLATE pg_catalog."default",
    dpservicetype character varying(100) COLLATE pg_catalog."default" DEFAULT 'wmts'::character varying,
    dpserviceparams text COLLATE pg_catalog."default",
    CONSTRAINT dp_v_qfg_schema_pkey PRIMARY KEY (dpid)
)

TABLESPACE pg_default;

ALTER TABLE public.dp_v_qfg_schema
    OWNER to postgres;

COMMENT ON TABLE public.dp_v_qfg_schema
    IS '发布-矢量-全覆盖展示服务-模板';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpid
    IS '标识，guid';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpstatus
    IS '并行处理状态;0-完成;1-待处理;2-处理中;3-处理有误';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpprocessid
    IS '并行处理辅助字段';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpaddtime
    IS '任务创建时间';

COMMENT ON COLUMN public.dp_v_qfg_schema.dplastmodifytime
    IS '任务最后修改时间';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpmemo
    IS '任务标识';

COMMENT ON COLUMN public.dp_v_qfg_schema.dptitle
    IS '标题';

COMMENT ON COLUMN public.dp_v_qfg_schema.dptargettitle
    IS '服务中文名模板';

COMMENT ON COLUMN public.dp_v_qfg_schema.dptargetname
    IS '服务英文名模板';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpdeploydir
    IS '发布目标数据的根目录';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpfileprefix
    IS '发布数据名称所涵盖的前缀，用于linux兼容';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpproject
    IS '投影坐标系';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpbatchdeploy
    IS '批量发布';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpprocesstype
    IS '处理类型：new-新创建；update-更新；delete-删除';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpservicetype
    IS '服务类型';

COMMENT ON COLUMN public.dp_v_qfg_schema.dpserviceparams
    IS '服务发布参数';


-- Table: public.dp_v_qfg_schema_layer

-- DROP TABLE public.dp_v_qfg_schema_layer;

CREATE TABLE public.dp_v_qfg_schema_layer
(
    dpid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpschemaid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpaddtime timestamp(6) without time zone DEFAULT now(),
    dplastmodifytime timestamp(6) without time zone DEFAULT now(),
    dpmemo character varying(200) COLLATE pg_catalog."default",
    dptitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dplayerid character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dplayername character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dplayer_datatype character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'Raster'::character varying,
    dplayer_queryable character varying(200) COLLATE pg_catalog."default",
    dplayer_resultfields character varying(1000) COLLATE pg_catalog."default" NOT NULL DEFAULT 'all'::character varying,
    dplayer_style text COLLATE pg_catalog."default",
    dpdeploysubdir character varying(2000) COLLATE pg_catalog."default",
    dpfiletags character varying[] COLLATE pg_catalog."default",
    dpobjecttype character varying[] COLLATE pg_catalog."default",
    dpfileprocessalgorithm character varying(100) COLLATE pg_catalog."default",
    dpfileprocessparams text COLLATE pg_catalog."default",
    dpbatchdeploy character varying(2000) COLLATE pg_catalog."default",
    CONSTRAINT dp_v_qfg_schema_layer_pkey PRIMARY KEY (dpid)
)

TABLESPACE pg_default;

ALTER TABLE public.dp_v_qfg_schema_layer
    OWNER to postgres;

COMMENT ON TABLE public.dp_v_qfg_schema_layer
    IS '发布-矢量-全覆盖展示服务-模板-图层';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpid
    IS '标识，guid';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpschemaid
    IS 'Schema标识';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpaddtime
    IS '任务创建时间';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplastmodifytime
    IS '任务最后修改时间';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpmemo
    IS '任务标识';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dptitle
    IS '标题';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayerid
    IS '服务图层英文名模板';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayername
    IS '服务图层中文名模板';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayer_datatype
    IS '服务图层-数据类型';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayer_queryable
    IS '服务图层-是否可查';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayer_resultfields
    IS '服务图层-结果字段集合';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dplayer_style
    IS '服务图层-渲染风格';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpdeploysubdir
    IS '图层数据的子目录';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpfiletags
    IS '满足要求的文件标签';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpobjecttype
    IS '满足要求的对象类型';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpfileprocessalgorithm
    IS '算法名称';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpfileprocessparams
    IS '算法参数';

COMMENT ON COLUMN public.dp_v_qfg_schema_layer.dpbatchdeploy
    IS '批量发布';


-- Table: public.dp_v_qfg

-- DROP TABLE public.dp_v_qfg;

CREATE TABLE public.dp_v_qfg
(
    dpid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpstatus integer DEFAULT 1,
    dpprocessid character varying(100) COLLATE pg_catalog."default",
    dpaddtime timestamp(6) without time zone DEFAULT now(),
    dplastmodifytime timestamp(6) without time zone DEFAULT now(),
    dpmemo text COLLATE pg_catalog."default",
    dpprocesstype character varying(100) COLLATE pg_catalog."default",
    dpschemaid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dptitle character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dpname character varying(200) COLLATE pg_catalog."default" NOT NULL,
    dpdeploydir character varying(2000) COLLATE pg_catalog."default",
    dpfileprefix character varying(2000) COLLATE pg_catalog."default",
    dptimeid character varying(100) COLLATE pg_catalog."default",
    dpspatialid character varying(100) COLLATE pg_catalog."default",
    dpbusid character varying(100) COLLATE pg_catalog."default",
    dpproject character varying(2000) COLLATE pg_catalog."default",
    dpservicetype character varying(100) COLLATE pg_catalog."default" DEFAULT 'wmts'::character varying,
    dpdeploymissionid character varying(100) COLLATE pg_catalog."default",
    dpserviceparams text COLLATE pg_catalog."default",
    CONSTRAINT dp_v_qfg_pkey PRIMARY KEY (dpid)
)

TABLESPACE pg_default;

ALTER TABLE public.dp_v_qfg
    OWNER to postgres;

COMMENT ON TABLE public.dp_v_qfg
    IS '发布-矢量-全覆盖展示服务-定义';

COMMENT ON COLUMN public.dp_v_qfg.dpid
    IS '标识，guid';

COMMENT ON COLUMN public.dp_v_qfg.dpstatus
    IS '并行处理状态;0-完成;1-待处理;2-处理中;3-处理有误';

COMMENT ON COLUMN public.dp_v_qfg.dpprocessid
    IS '并行处理辅助字段';

COMMENT ON COLUMN public.dp_v_qfg.dpaddtime
    IS '任务创建时间';

COMMENT ON COLUMN public.dp_v_qfg.dplastmodifytime
    IS '任务最后修改时间';

COMMENT ON COLUMN public.dp_v_qfg.dpmemo
    IS '备注';

COMMENT ON COLUMN public.dp_v_qfg.dpprocesstype
    IS '处理类型：new-新创建；update-更新；delete-删除';

COMMENT ON COLUMN public.dp_v_qfg.dpschemaid
    IS '模板标识';

COMMENT ON COLUMN public.dp_v_qfg.dptitle
    IS '服务中文名';

COMMENT ON COLUMN public.dp_v_qfg.dpname
    IS '服务英文名';

COMMENT ON COLUMN public.dp_v_qfg.dpdeploydir
    IS '发布目标目录';

COMMENT ON COLUMN public.dp_v_qfg.dpfileprefix
    IS '发布数据名称所涵盖的前缀，用于linux兼容';

COMMENT ON COLUMN public.dp_v_qfg.dptimeid
    IS '时间标识';

COMMENT ON COLUMN public.dp_v_qfg.dpspatialid
    IS '空间标识';

COMMENT ON COLUMN public.dp_v_qfg.dpbusid
    IS '业务标识';

COMMENT ON COLUMN public.dp_v_qfg.dpproject
    IS '投影坐标系';

COMMENT ON COLUMN public.dp_v_qfg.dpdeploymissionid
    IS '服务发布任务标识';

COMMENT ON COLUMN public.dp_v_qfg.dpserviceparams
    IS '服务发布参数';


-- Table: public.dp_v_qfg_layer

-- DROP TABLE public.dp_v_qfg_layer;

CREATE TABLE public.dp_v_qfg_layer
(
    dpid character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpservice_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dplayerschema_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpprocesstype character varying(100) COLLATE pg_catalog."default",
    dpstatus integer DEFAULT 1,
    dpprocessid character varying(100) COLLATE pg_catalog."default",
    dplayer_id character varying(2000) COLLATE pg_catalog."default",
    dplayer_name character varying(2000) COLLATE pg_catalog."default",
    dplayer_deploysubdir character varying(2000) COLLATE pg_catalog."default",
    dplayer_datatype character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'Raster'::character varying,
    dplayer_queryable character varying(200) COLLATE pg_catalog."default",
    dplayer_resultfields character varying(1000) COLLATE pg_catalog."default" NOT NULL DEFAULT 'all'::character varying,
    dplayer_style text COLLATE pg_catalog."default",
    dpfileprocessalgorithm character varying(100) COLLATE pg_catalog."default",
    dpfileprocessparams text COLLATE pg_catalog."default",
    dpaddtime timestamp(6) without time zone DEFAULT now(),
    dplastmodifytime timestamp(6) without time zone DEFAULT now(),
    CONSTRAINT dp_v_qfg_layer_pkey PRIMARY KEY (dpid)
)

TABLESPACE pg_default;

ALTER TABLE public.dp_v_qfg_layer
    OWNER to postgres;

COMMENT ON TABLE public.dp_v_qfg_layer
    IS '发布-矢量-全覆盖展示服务-定义-图层';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpid
    IS '标识，guid';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpservice_id
    IS '服务标识';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayerschema_id
    IS '图层定义标识';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpprocesstype
    IS '处理类型：new-新创建；update-更新；delete-删除';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpstatus
    IS '并行处理状态;0-完成;1-待处理;2-处理中;3-处理有误';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpprocessid
    IS '并行处理辅助字段';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_id
    IS '图层标识';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_name
    IS '图层名称';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_deploysubdir
    IS '服务图层-发布子目录';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_datatype
    IS '服务图层-数据类型';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_queryable
    IS '服务图层-是否可查';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_resultfields
    IS '服务图层-结果字段集合';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplayer_style
    IS '服务图层-渲染风格';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpfileprocessalgorithm
    IS '算法名称';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpfileprocessparams
    IS '算法参数';

COMMENT ON COLUMN public.dp_v_qfg_layer.dpaddtime
    IS '创建时间';

COMMENT ON COLUMN public.dp_v_qfg_layer.dplastmodifytime
    IS '最后修改时间';


-- Table: public.dp_v_qfg_layer_file

-- DROP TABLE public.dp_v_qfg_layer_file;

CREATE TABLE public.dp_v_qfg_layer_file
(
    dpdf_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpdf_layer_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    dpdf_object_id character varying(100) COLLATE pg_catalog."default",
    dpdf_object_fullname character varying(2000) COLLATE pg_catalog."default",
    dpdf_object_title character varying(2000) COLLATE pg_catalog."default",
    dpdf_object_size bigint,
    dpdf_object_date timestamp(6) without time zone,
    dpdf_object_fp character varying(200) COLLATE pg_catalog."default",
    dpdf_object_fp_lastdeploy character varying(200) COLLATE pg_catalog."default",
    dpdf_target_filepath character varying(2000) COLLATE pg_catalog."default",
    dpdf_service_filepath character varying(2000) COLLATE pg_catalog."default",
    dpdf_processtype character varying(100) COLLATE pg_catalog."default",
    dpdf_check_status integer,
    dpdf_check_memo text COLLATE pg_catalog."default",
    dpdf_check_procid character varying(100) COLLATE pg_catalog."default",
    dpdf_publish_status integer DEFAULT 0,
    dpdf_publish_memo text COLLATE pg_catalog."default",
    dpdf_publish_procid character varying(100) COLLATE pg_catalog."default",
    dpdf_addtime timestamp(6) without time zone DEFAULT now(),
    dpdf_lastmodifytime timestamp(6) without time zone DEFAULT now(),
    dpdf_publish_filename character varying(2000) COLLATE pg_catalog."default",
    dpdf_publish_filemetadata text COLLATE pg_catalog."default",
    dpdf_publish_filemetatype integer DEFAULT 0,
    CONSTRAINT dp_v_qfg_layer_file_pkey PRIMARY KEY (dpdf_id)
)

TABLESPACE pg_default;

ALTER TABLE public.dp_v_qfg_layer_file
    OWNER to postgres;

COMMENT ON TABLE public.dp_v_qfg_layer_file
    IS '发布-矢量-全覆盖展示服务-定义-文件';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_id
    IS '标识，guid';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_layer_id
    IS '图层标识';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_id
    IS '对象标识';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_fullname
    IS '对象全路径名';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_title
    IS '对象标题，注意不是全路径文件名';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_size
    IS '对象大小';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_date
    IS '对象最后修改日期';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_fp
    IS '对象指纹';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_object_fp_lastdeploy
    IS '最后一次发布的对象指纹';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_target_filepath
    IS '对象处理目标路径';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_service_filepath
    IS '服务发布文件路径';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_processtype
    IS '处理类型：new-新创建；update-更新；delete-删除';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_check_status
    IS '检查状态;0-完成;1-待处理;2-处理中;3-处理有误';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_check_memo
    IS '检查结果';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_check_procid
    IS '检查并行辅助字段';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_status
    IS '发布状态;0-完成;1-待处理;2-处理中;3-处理有误';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_memo
    IS '发布结果';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_procid
    IS '发布并行辅助字段';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_addtime
    IS '创建时间';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_lastmodifytime
    IS '最后修改时间';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_filename
    IS '发布文件名';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_filemetadata
    IS '服务发布文件元数据';

COMMENT ON COLUMN public.dp_v_qfg_layer_file.dpdf_publish_filemetatype
    IS '服务发布文件元数据类型：0-txt;1-json;2-xml';



insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(2001, 'analyse_engine', '分析-引擎', 'C:\App\QGIS\bin\python-qgis.bat', null);
insert into ro_global_config(gcfgid, gcfgcode, gcfgtitle, gcfgvalue, gcfgmemo) 
  values(3001, 'atgis_server_deploy_dbserverid', '服务-发布-目标服务标识', 'v3f935edd3d904dbd91d67c93836d8a0c', null);

update dm2_storage 
  set dstotheroption = '{"ds_opt_server_deploy_mount_point_path":"/User/wangxiya/mount/' || dstid || '"}';


/*
	2020-6-12 王西亚
	初始化测试数据
  示例1：单个WMTS服务配置发布
*/

truncate table dp_v_qfg_schema;
insert into dp_v_qfg_schema(dpid, dpstatus, dpprocessid, dpaddtime, dplastmodifytime, dpmemo, dpProcessType,
	dptitle, dptargettitle, dptargetname, dpdeploydir, dpfileprefix, dpproject, dpbatchdeploy) 
values('single_service', 1, null, now(), now(), null, 'new',
	'昆明市2019年全覆盖数据展示服务', '全覆盖数据展示服务-昆明全市-2019', 'qfg-kunming-2019', 'C:\data\Target', 'linux', 
	'[{"project":"EPSG:4326"},{"project":"EPSG:3857"}]', null);
insert into dp_v_qfg_schema(dpid, dpstatus, dpprocessid, dpaddtime, dplastmodifytime, dpmemo, dpProcessType,
  dptitle, dptargettitle, dptargetname, dpdeploydir, dpfileprefix, dpproject, dpbatchdeploy)
values('multi_service', 1, null, now(), now(), null, 'new',
  '昆明市2019年全覆盖数据展示服务', '全覆盖数据展示服务-昆明全市-$time_title$', 'qfg-kunming-$time_id$', 'C:\data\Target', 'linux',
  '[{"project":"EPSG:4326"},{"project":"EPSG:3857"}]', '[{"dim_time":"t0","dim_spatial":"","dim_bus":""}]');



truncate table dp_v_qfg_schema_layer;
insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo, 
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy, dpobjecttype) 
values('hello_layer_1', 'single_service', now(), now(), null
    , '耕地', 'gengdi', '耕地', 'gengdi_dir'
    , 'Vector', 'false', 'all', '{"STYLE":{"COLOR":"''#A5F57A''","OUTLINECOLOR":"''#A5F57A''","SIZE":"7"}}' 
    , '{v63f06e078d594bf2add38117533f81d5}' , 'vector_extract_row.py', ' -filter dlbm=%27033%27 '
    , null, '{shp}'
);
insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo,
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy, dpobjecttype) 
values('hello_layer_2', 'single_service', now(), now(), null
    , '草地', 'caodi', '草地', 'caodi_dir'
    , 'Vector', 'false', 'all', '{"STYLE":{"COLOR":"''#A5F57A''","OUTLINECOLOR":"''#A5F57A''","SIZE":"7"}}' 
    , '{v63f06e078d594bf2add38117533f81d5}' , 'vector_extract_row.py', ' -filter dlbm=%27031%27 '
    , null, '{shp}'
);

insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo, 
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy, dpobjecttype) 
values('hello_layer_1', 'multi_service', now(), now(), null
    , '耕地', 'gengdi', '耕地', 'gengdi_dir'
    , 'Vector', 'false', 'all', '{"STYLE":{"COLOR":"''#A5F57A''","OUTLINECOLOR":"''#A5F57A''","SIZE":"7"}}' 
    , '{v63f06e078d594bf2add38117533f81d5}' , 'vector_extract_row.py', ' -filter yjdlbm=%2706%27 '
    , null, '{shp}'
);
insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo, 
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy, dpobjecttype) 
values('hello_layer_2', 'multi_service', now(), now(), null
    , '草地', 'caodi', '草地', 'caodi_dir'
    , 'Vector', 'false', 'all', '{"STYLE":{"COLOR":"''#A5F57A''","OUTLINECOLOR":"''#A5F57A''","SIZE":"7"}}' 
    , '{v63f06e078d594bf2add38117533f81d5}' , 'vector_extract_row.py', ' -filter yjdlbm=%2701%27 '
    , null, '{shp}'
);

/*
  2020-6-30 王西亚
  。数据统计：
    。shapefile_sql：针对shpFile的dbf进行数据统计
    。transform_sql：将矢量转换为geopackage，然后进行使用sqlite引擎进行数据统计
  。其他配置：
    。dp_v_qfg_schema.dpserviceparams
      。使用XML进行配置
      。XML格式使用GBK编码
      。XML内容：
        。启动发布前的数据预处理SQL（包括指定的DB Server ID）或调度的BusinessID
        。完成发布后的数据处理SQL（包括指定的DB Server ID）或调度的BusinessID
    。dp_v_qfg_schema_layer.dpFileProcessAlgorithm
      。shapefile_sql：针对shpFile的dbf进行数据统计
      。transform_sql：将矢量转换为geopackage，然后进行使用sqlite引擎进行数据统计
    。dp_v_qfg_schema_layer.dpFileProcessParams
      。使用XML进行配置
      。XML格式使用GBK编码
      。XML内容：
        。每一条记录运行的SQL（包括指定的DB Server ID）
        。每一条记录调度的BusinessID
*/

insert into dp_v_qfg_schema(dpid, dpstatus, dpprocessid, dpaddtime, dplastmodifytime, dpmemo, dpProcessType,
  dptitle, dptargettitle, dptargetname, dpdeploydir, dpfileprefix, dpproject, dpbatchdeploy
  , dpservicetype, dpserviceparams
  ) 
values('shapefile_stat', 1, null, now(), now(), null, 'new',
  '昆明市2019年全覆盖数据展示服务', '全覆盖数据展示服务-昆明全市', 'qfg-kunming', 'C:\data\Target', 'linux', 
  null, null, 'stat', null
  );

insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo,
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy) 
values('group_1', 'shapefile_stat', now(), now(), null
    , '耕地', 'gengdi', '耕地', 'gengdi_dir'
    , 'Vector', 'false', 'all', null 
    , '{v63f06e078d594bf2add38117533f81d5}' , 'shapefile_sql', null, null
);


DROP TABLE public.a_stat;

CREATE TABLE public.a_stat
(
    sid bigserial NOT NULL,
    sgroup character varying(100) COLLATE pg_catalog."default" ,
    subgroup character varying(100) COLLATE pg_catalog."default",
    stat_count numeric(19,6),
    stat_sum_area numeric(30,15),

    CONSTRAINT a_stat_pkey PRIMARY KEY (sid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.a_stat
    OWNER to postgres;
COMMENT ON TABLE public.a_stat
    IS '发布-矢量-统计服务-测试';

/*
  2020-7-9 王西亚
  。数据统计：
    。shapefile_sql：针对shpFile的dbf进行数据统计
    。transform_sql：将矢量转换为geopackage，然后进行使用sqlite引擎进行数据统计
  。其他配置：
    。dp_v_qfg_schema.dpserviceparams
      。使用XML进行配置
      。XML格式使用GBK编码
      。XML内容：
        。启动发布前的数据预处理SQL（包括指定的DB Server ID）或调度的BusinessID
        。完成发布后的数据处理SQL（包括指定的DB Server ID）或调度的BusinessID
    。dp_v_qfg_schema_layer.dpFileProcessAlgorithm
      。shapefile_sql：针对shpFile的dbf进行数据统计
      。transform_sql：将矢量转换为geopackage，然后进行使用sqlite引擎进行数据统计
    。dp_v_qfg_schema_layer.dpFileProcessParams
      。使用XML进行配置
      。XML格式使用GBK编码
      。XML内容：
        。每一条记录运行的SQL（包括指定的DB Server ID）
        。每一条记录调度的BusinessID
*/

insert into dp_v_qfg_schema(dpid, dpstatus, dpprocessid, dpaddtime, dplastmodifytime, dpmemo, dpProcessType,
  dptitle, dptargettitle, dptargetname, dpdeploydir, dpfileprefix, dpproject, dpbatchdeploy
  , dpservicetype, dpserviceparams
  ) 
values('vector_analyse', 1, null, now(), now(), null, 'new',
  '现状与规划分析', '现状与规划分析', 'analyse_xz_gh', 'C:\data\Target', 'linux', 
  null, null, 'stat', null
  );

insert into dp_v_qfg_schema_layer(dpid, dpSchemaID, dpaddtime, dplastmodifytime, dpmemo,
    dptitle, dpLayerID, dpLayerName, dpDeploySubDir
    , dpLayer_DataType, dplayer_queryable, dplayer_resultfields, dplayer_style
    , dpfiletags, dpObjecttype, dpFileProcessAlgorithm, dpFileProcessParams, dpBatchDeploy) 
values('vector_analyse_g1', 'vector_analyse', now(), now(), null
    , '对比分析', 'intersect', '对比分析', 'intersect_dir'
    , 'Vector', 'false', 'all', null 
    , '{9654e86eec1145d38309c263700384M2}', '{shp}' , 'vector_analyse_refer_1_1', null, null
);


-- dpFileProcessParams:
/*
<?xml version="1.0" encoding="gbk"?>
<process>
  <refer refer_object_tags="{v63f06e078d594bf2add38117533f81d5}" refer_object_type="{vector_dataset_layer}"/>
  <commandline name="vector_refer_analyse.py"> -ofs 项目编号 -ofr dlbm -mn analyse_intersect</commandline>
  <before comment="处理当前数据文件前的操作">
    <serverid>-1</serverid>
    <type>sql</type>
    <content><![CDATA[
    ]]></content>
  </before>
  <record comment="每一条统计结果，系统按如下方式处理">
    <serverid>-1</serverid>
    <type>node</type>
    <content type="9" text="9-将数据存储到数据表中" serverid="-1" tablename="a_stat" mode="1" exceptonfailure="-1">
      <record id="1">
        <sgroup>$项目编号$</sgroup>
        <subgroup>$dlbm$</subgroup>
        <shape srid="4326">$shape$</shape>
      </record>
    </content>
  </record>
  <after comment="处理当前数据文件后的操作">
    <serverid>-1</serverid>
    <type>sql</type>
    <content/>
  </after>
</process>

*/