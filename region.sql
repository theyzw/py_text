/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : newmiao

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 06/07/2019 17:54:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tbl_health_up_region_config
-- ----------------------------
DROP TABLE IF EXISTS `plan_region_config`;
CREATE TABLE `tbl_health_up_region_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plan_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '计划id',
  `library_id` int(11) NOT NULL DEFAULT '0' COMMENT 'address_library表id',
  `region_code` int(11) NOT NULL DEFAULT '0' COMMENT '地址code',
  `region_name` varchar(100) NOT NULL DEFAULT '' COMMENT '地址名称',
  `limit_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '限制类型。1限量  2限业务员  3业务员限量',
  `region_count` bigint(20) NOT NULL DEFAULT '0' COMMENT '当前数量',
  `region_total` bigint(20) NOT NULL DEFAULT '0' COMMENT '总数',
  `limit_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态。-1关闭  1开启',
  `update_user` varchar(20) NOT NULL DEFAULT '' COMMENT '更新人',
  `create_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_region_plan` (`region_code`,`plan_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='地区限制表';

-- ----------------------------
-- Table structure for tbl_health_up_region_salesman
-- ----------------------------
DROP TABLE IF EXISTS `plan_region_salesman`;
CREATE TABLE `tbl_health_up_region_salesman` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plan_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '计划id',
  `region_code` int(11) NOT NULL DEFAULT '0' COMMENT '地址code',
  `job_num` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '业务员工号',
  `limit_count` bigint(20) NOT NULL DEFAULT '0' COMMENT '业务员限量，0为不限制',
  `create_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_job_region_plan` (`job_num`,`region_code`,`up_plan_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='业务员限制表';

SET FOREIGN_KEY_CHECKS = 1;
