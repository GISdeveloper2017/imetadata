/*
 Navicat Premium Data Transfer

 Source Server         : 生态审计localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 100011
 Source Host           : localhost:5432
 Source Catalog        : atplatform4_np_inside20210208_big
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100011
 File Encoding         : 65001

 Date: 20/02/2021 19:37:09
*/


-- ----------------------------
-- Table structure for dm2_import_step
-- ----------------------------
DROP TABLE IF EXISTS "public"."dm2_import_step";
CREATE TABLE "public"."dm2_import_step" (
  "dis_id" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "dis_directory_count" int4,
  "dis_file_count" int4,
  "dis_object_count" int4,
  "dis_detail_count" int4,
  "dis_object_tag_count" int4,
  "dis_object_notag_count" int4,
  "dis_query_time" timestamp(6),
  "dis_addtime" timestamp(6)
)
;
COMMENT ON COLUMN "public"."dm2_import_step"."dis_id" IS '标识，guid';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_directory_count" IS '目录个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_file_count" IS '文件个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_object_count" IS '数据个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_detail_count" IS '附属文件个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_object_tag_count" IS '已挂接标签个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_object_notag_count" IS '未挂接标签个数';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_query_time" IS '查询时间';
COMMENT ON COLUMN "public"."dm2_import_step"."dis_addtime" IS '添加时间';

-- ----------------------------
-- Primary Key structure for table dm2_import_step
-- ----------------------------
ALTER TABLE "public"."dm2_import_step" ADD CONSTRAINT "dm2_import_step_pkey" PRIMARY KEY ("dis_id");
