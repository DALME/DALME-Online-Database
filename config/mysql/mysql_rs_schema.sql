SET @ORIG_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;

SET @ORIG_UNIQUE_CHECKS = @@UNIQUE_CHECKS;
SET UNIQUE_CHECKS = 0;

SET @ORIG_TIME_ZONE = @@TIME_ZONE;
SET TIME_ZONE = '+00:00';

SET @ORIG_SQL_MODE = @@SQL_MODE;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE IF NOT EXISTS `resourcespace` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
USE `resourcespace`;

DROP TABLE IF EXISTS `usergroup_dash_tile`;
DROP TABLE IF EXISTS `usergroup_collection`;
DROP TABLE IF EXISTS `usergroup`;
DROP TABLE IF EXISTS `user_userlist`;
DROP TABLE IF EXISTS `user_report`;
DROP TABLE IF EXISTS `user_rating`;
DROP TABLE IF EXISTS `user_preferences`;
DROP TABLE IF EXISTS `user_message`;
DROP TABLE IF EXISTS `user_dash_tile`;
DROP TABLE IF EXISTS `user_collection`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `sysvars`;
DROP TABLE IF EXISTS `site_text`;
DROP TABLE IF EXISTS `search_saved`;
DROP TABLE IF EXISTS `resource_type_field`;
DROP TABLE IF EXISTS `resource_type`;
DROP TABLE IF EXISTS `resource_related`;
DROP TABLE IF EXISTS `resource_node`;
DROP TABLE IF EXISTS `resource_log`;
DROP TABLE IF EXISTS `resource_keyword`;
DROP TABLE IF EXISTS `resource_dimensions`;
DROP TABLE IF EXISTS `resource_data`;
DROP TABLE IF EXISTS `resource_custom_access`;
DROP TABLE IF EXISTS `resource_alt_files`;
DROP TABLE IF EXISTS `resource`;
DROP TABLE IF EXISTS `research_request`;
DROP TABLE IF EXISTS `request`;
DROP TABLE IF EXISTS `report_periodic_emails_unsubscribe`;
DROP TABLE IF EXISTS `report_periodic_emails`;
DROP TABLE IF EXISTS `report`;
DROP TABLE IF EXISTS `preview_size`;
DROP TABLE IF EXISTS `plugins`;
DROP TABLE IF EXISTS `node_keyword`;
DROP TABLE IF EXISTS `node`;
DROP TABLE IF EXISTS `message`;
DROP TABLE IF EXISTS `keyword_related`;
DROP TABLE IF EXISTS `keyword`;
DROP TABLE IF EXISTS `job_queue`;
DROP TABLE IF EXISTS `ip_lockout`;
DROP TABLE IF EXISTS `external_access_keys`;
DROP TABLE IF EXISTS `dynamic_tree_node`;
DROP TABLE IF EXISTS `dash_tile`;
DROP TABLE IF EXISTS `daily_stat`;
DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `collection_savedsearch`;
DROP TABLE IF EXISTS `collection_resource`;
DROP TABLE IF EXISTS `collection_log`;
DROP TABLE IF EXISTS `collection_keyword`;
DROP TABLE IF EXISTS `collection`;
DROP TABLE IF EXISTS `api_whitelist`;
DROP TABLE IF EXISTS `annotation_node`;
DROP TABLE IF EXISTS `annotation`;
DROP TABLE IF EXISTS `annotate_notes`;
DROP TABLE IF EXISTS `activity_log`;


CREATE TABLE `activity_log` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `logged` datetime DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `log_code` char(1) DEFAULT NULL,
  `note` text,
  `value_old` text,
  `value_new` text,
  `value_diff` text,
  `remote_table` varchar(100) DEFAULT NULL,
  `remote_column` varchar(100) DEFAULT NULL,
  `remote_ref` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=2735 DEFAULT CHARSET=utf8;


CREATE TABLE `annotate_notes` (
  `ref` int(11) DEFAULT NULL,
  `top_pos` int(11) DEFAULT NULL,
  `left_pos` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `preview_width` int(11) DEFAULT NULL,
  `preview_height` int(11) DEFAULT NULL,
  `note` text,
  `note_id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `page` int(5) DEFAULT NULL,
  PRIMARY KEY (`note_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;


CREATE TABLE `annotation` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `resource` int(11) DEFAULT NULL,
  `resource_type_field` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `x` decimal(17,16) DEFAULT NULL,
  `y` decimal(17,16) DEFAULT NULL,
  `width` decimal(17,16) DEFAULT NULL,
  `height` decimal(17,16) DEFAULT NULL,
  `page` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `annotation_node` (
  `annotation` int(11) DEFAULT NULL,
  `node` int(11) DEFAULT NULL,
  KEY `annotation_node` (`annotation`,`node`),
  KEY `annotation` (`annotation`),
  KEY `node` (`node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `api_whitelist` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `ip_domain` varchar(200) DEFAULT NULL,
  `apis` varchar(200) DEFAULT NULL,
  `userref` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `collection` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `public` int(11) DEFAULT '0',
  `theme` varchar(100) DEFAULT NULL,
  `theme2` varchar(100) DEFAULT NULL,
  `theme3` varchar(100) DEFAULT NULL,
  `allow_changes` int(11) DEFAULT '0',
  `cant_delete` int(11) DEFAULT '0',
  `keywords` text,
  `savedsearch` int(11) DEFAULT NULL,
  `home_page_publish` int(11) DEFAULT NULL,
  `home_page_text` text,
  `home_page_image` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  `theme4` varchar(100) DEFAULT NULL,
  `theme5` varchar(100) DEFAULT NULL,
  `theme6` varchar(100) DEFAULT NULL,
  `theme7` varchar(100) DEFAULT NULL,
  `theme8` varchar(100) DEFAULT NULL,
  `theme9` varchar(100) DEFAULT NULL,
  `theme10` varchar(100) DEFAULT NULL,
  `theme11` varchar(100) DEFAULT NULL,
  `theme12` varchar(100) DEFAULT NULL,
  `theme13` varchar(100) DEFAULT NULL,
  `theme14` varchar(100) DEFAULT NULL,
  `theme15` varchar(100) DEFAULT NULL,
  `theme16` varchar(100) DEFAULT NULL,
  `theme17` varchar(100) DEFAULT NULL,
  `theme18` varchar(100) DEFAULT NULL,
  `theme19` varchar(100) DEFAULT NULL,
  `theme20` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ref`),
  KEY `theme` (`theme`),
  KEY `public` (`public`),
  KEY `user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=1257 DEFAULT CHARSET=utf8;


CREATE TABLE `collection_keyword` (
  `collection` int(11) DEFAULT NULL,
  `keyword` int(11) DEFAULT NULL,
  KEY `collection` (`collection`),
  KEY `keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `collection_log` (
  `date` datetime DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `collection` int(11) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `resource` int(11) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  KEY `user` (`user`),
  KEY `collection` (`collection`),
  KEY `resource` (`resource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `collection_resource` (
  `collection` int(11) DEFAULT NULL,
  `resource` int(11) DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` text,
  `rating` int(11) DEFAULT NULL,
  `use_as_theme_thumbnail` int(11) DEFAULT NULL,
  `purchase_size` varchar(10) DEFAULT NULL,
  `purchase_complete` int(11) DEFAULT '0',
  `purchase_price` decimal(10,2) DEFAULT '0.00',
  `sortorder` int(11) DEFAULT NULL,
  KEY `collection` (`collection`),
  KEY `resource_collection` (`collection`,`resource`),
  KEY `resource` (`resource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `collection_savedsearch` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `collection` int(11) DEFAULT NULL,
  `search` text,
  `restypes` text,
  `starsearch` int(11) DEFAULT NULL,
  `archive` varchar(50) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `result_limit` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;


CREATE TABLE `comment` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `ref_parent` int(11) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `hide` int(1) DEFAULT '0',
  `collection_ref` int(11) DEFAULT NULL,
  `resource_ref` int(11) DEFAULT NULL,
  `user_ref` int(11) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website_url` text,
  `body` text,
  PRIMARY KEY (`ref`),
  KEY `ref_parent` (`ref_parent`),
  KEY `collection_ref` (`collection_ref`),
  KEY `resource_ref` (`resource_ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `daily_stat` (
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `usergroup` int(11) DEFAULT '0',
  `activity_type` varchar(50) DEFAULT NULL,
  `object_ref` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT '0',
  `external` tinyint(1) DEFAULT '0',
  KEY `stat_day` (`year`,`month`,`day`),
  KEY `stat_month` (`year`,`month`),
  KEY `stat_usergroup` (`usergroup`),
  KEY `stat_day_activity` (`year`,`month`,`day`,`activity_type`),
  KEY `stat_day_activity_ref` (`year`,`month`,`day`,`activity_type`,`object_ref`),
  KEY `activity_type` (`activity_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `dash_tile` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `txt` text,
  `all_users` int(1) DEFAULT NULL,
  `default_order_by` int(11) DEFAULT NULL,
  `url` text,
  `link` text,
  `reload_interval_secs` int(11) DEFAULT NULL,
  `resource_count` int(1) DEFAULT NULL,
  `allow_delete` int(1) DEFAULT '1',
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


CREATE TABLE `dynamic_tree_node` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `resource_type_field` int(11) DEFAULT '0',
  `parent` int(11) DEFAULT '0',
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ref`),
  KEY `parent` (`parent`),
  KEY `resource_type_field` (`resource_type_field`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `external_access_keys` (
  `resource` int(11) DEFAULT NULL,
  `access_key` char(10) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `usergroup` int(11) DEFAULT NULL,
  `collection` int(11) DEFAULT NULL,
  `request_feedback` int(11) DEFAULT '0',
  `email` varchar(100) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `lastused` datetime DEFAULT NULL,
  `access` int(11) DEFAULT '-1',
  `expires` datetime DEFAULT NULL,
  KEY `resource` (`resource`),
  KEY `resource_key` (`resource`,`access_key`),
  KEY `access_key` (`access_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `ip_lockout` (
  `ip` varchar(40) NOT NULL DEFAULT '',
  `tries` int(11) DEFAULT '0',
  `last_try` datetime DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `job_queue` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  `job_data` text,
  `start_date` datetime DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `success_text` varchar(250) DEFAULT NULL,
  `failure_text` varchar(250) DEFAULT NULL,
  `job_code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `keyword` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(100) DEFAULT NULL,
  `soundex` varchar(50) DEFAULT NULL,
  `hit_count` int(11) DEFAULT '0',
  PRIMARY KEY (`ref`),
  KEY `keyword` (`keyword`),
  KEY `keyword_hit_count` (`hit_count`)
) ENGINE=InnoDB AUTO_INCREMENT=112123 DEFAULT CHARSET=utf8;


CREATE TABLE `keyword_related` (
  `keyword` int(11) DEFAULT NULL,
  `related` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `message` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime DEFAULT NULL,
  `owner` int(11) DEFAULT NULL,
  `message` mediumtext,
  `url` text,
  `expires` datetime DEFAULT NULL,
  `related_activity` int(11) DEFAULT NULL,
  `related_ref` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;


CREATE TABLE `node` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `resource_type_field` int(11) DEFAULT NULL,
  `name` text,
  `parent` int(11) DEFAULT NULL,
  `order_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`),
  KEY `resource_type_field` (`resource_type_field`,`ref`,`parent`,`order_by`),
  KEY `name` (`name`(20))
) ENGINE=InnoDB AUTO_INCREMENT=306 DEFAULT CHARSET=utf8;


CREATE TABLE `node_keyword` (
  `node` int(11) DEFAULT NULL,
  `keyword` int(11) DEFAULT NULL,
  `position` int(11) DEFAULT '0',
  KEY `node_keyword` (`node`,`keyword`),
  KEY `node` (`node`),
  KEY `keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `plugins` (
  `name` varchar(50) NOT NULL DEFAULT '',
  `descrip` text,
  `author` varchar(100) DEFAULT NULL,
  `update_url` varchar(100) DEFAULT NULL,
  `info_url` varchar(100) DEFAULT NULL,
  `inst_version` float DEFAULT NULL,
  `config` longblob,
  `config_json` mediumtext,
  `config_url` varchar(100) DEFAULT NULL,
  `enabled_groups` varchar(200) DEFAULT NULL,
  `priority` int(11) DEFAULT '999',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `preview_size` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `id` char(3) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `padtosize` int(11) DEFAULT '0',
  `name` varchar(50) DEFAULT NULL,
  `internal` int(11) DEFAULT '0',
  `allow_preview` int(11) DEFAULT '0',
  `allow_restricted` int(11) DEFAULT '0',
  `quality` int(3) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `report` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `query` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


CREATE TABLE `report_periodic_emails` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `send_all_users` int(11) DEFAULT NULL,
  `user_groups` varchar(255) DEFAULT NULL,
  `report` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `email_days` int(11) DEFAULT NULL,
  `last_sent` datetime DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `report_periodic_emails_unsubscribe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `periodic_email_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `request` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `collection` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `request_mode` int(11) DEFAULT '0',
  `status` int(11) DEFAULT '0',
  `comments` text,
  `expires` date DEFAULT NULL,
  `assigned_to` int(11) DEFAULT NULL,
  `reason` text,
  `reasonapproved` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE `research_request` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `description` text,
  `deadline` datetime DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `finaluse` text,
  `resource_types` varchar(50) DEFAULT NULL,
  `noresources` int(11) DEFAULT NULL,
  `shape` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `assigned_to` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `collection` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`),
  KEY `research_collections` (`collection`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `resource_type` int(11) DEFAULT NULL,
  `has_image` int(11) DEFAULT '0',
  `is_transcoding` int(11) DEFAULT '0',
  `hit_count` int(11) DEFAULT '0',
  `new_hit_count` int(11) DEFAULT '0',
  `creation_date` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `user_rating` int(11) DEFAULT NULL,
  `user_rating_count` int(11) DEFAULT NULL,
  `user_rating_total` int(11) DEFAULT NULL,
  `country` varchar(200) DEFAULT NULL,
  `file_extension` varchar(10) DEFAULT NULL,
  `preview_extension` varchar(10) DEFAULT NULL,
  `image_red` int(11) DEFAULT NULL,
  `image_green` int(11) DEFAULT NULL,
  `image_blue` int(11) DEFAULT NULL,
  `thumb_width` int(11) DEFAULT NULL,
  `thumb_height` int(11) DEFAULT NULL,
  `archive` int(11) DEFAULT '0',
  `access` int(11) DEFAULT '0',
  `colour_key` varchar(5) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `file_path` varchar(500) DEFAULT NULL,
  `file_modified` datetime DEFAULT NULL,
  `file_checksum` varchar(32) DEFAULT NULL,
  `request_count` int(11) DEFAULT '0',
  `expiry_notification_sent` int(11) DEFAULT '0',
  `preview_tweaks` varchar(50) DEFAULT NULL,
  `geo_lat` double DEFAULT NULL,
  `geo_long` double DEFAULT NULL,
  `mapzoom` int(11) DEFAULT NULL,
  `disk_usage` bigint(20) DEFAULT NULL,
  `disk_usage_last_updated` datetime DEFAULT NULL,
  `file_size` bigint(20) DEFAULT NULL,
  `preview_attempts` int(11) DEFAULT NULL,
  `field12` varchar(200) DEFAULT NULL,
  `field8` varchar(200) DEFAULT NULL,
  `field3` varchar(200) DEFAULT NULL,
  `annotation_count` int(11) DEFAULT NULL,
  `field51` varchar(200) DEFAULT NULL,
  `field79` varchar(200) DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ref`),
  KEY `hit_count` (`hit_count`),
  KEY `resource_archive` (`archive`),
  KEY `resource_access` (`access`),
  KEY `resource_type` (`resource_type`),
  KEY `resource_creation_date` (`creation_date`),
  KEY `rating` (`rating`),
  KEY `colour_key` (`colour_key`),
  KEY `has_image` (`has_image`),
  KEY `file_checksum` (`file_checksum`),
  KEY `geo_lat` (`geo_lat`),
  KEY `geo_long` (`geo_long`),
  KEY `disk_usage` (`disk_usage`),
  KEY `created_by` (`created_by`)
) ENGINE=InnoDB AUTO_INCREMENT=41267 DEFAULT CHARSET=utf8;


CREATE TABLE `resource_alt_files` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `resource` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  `file_extension` varchar(10) DEFAULT NULL,
  `file_size` bigint(20) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `unoconv` int(11) DEFAULT NULL,
  `alt_type` varchar(100) DEFAULT NULL,
  `page_count` int(11) DEFAULT NULL,
  `transform_scale_w` int(11) DEFAULT NULL,
  `transform_scale_h` int(11) DEFAULT NULL,
  `transform_flop` int(11) DEFAULT NULL,
  `transform_rotation` int(11) DEFAULT NULL,
  `transform_crop_w` int(11) DEFAULT NULL,
  `transform_crop_h` int(11) DEFAULT NULL,
  `transform_crop_x` int(11) DEFAULT NULL,
  `transform_crop_y` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=425 DEFAULT CHARSET=utf8;


CREATE TABLE `resource_custom_access` (
  `resource` int(11) DEFAULT NULL,
  `usergroup` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `access` int(11) DEFAULT NULL,
  `user_expires` date DEFAULT NULL,
  KEY `resource` (`resource`),
  KEY `usergroup` (`usergroup`),
  KEY `user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource_data` (
  `resource` int(11) DEFAULT NULL,
  `resource_type_field` int(11) DEFAULT NULL,
  `value` mediumtext,
  `django_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`django_id`),
  KEY `resource` (`resource`)
) ENGINE=InnoDB AUTO_INCREMENT=287639 DEFAULT CHARSET=utf8;


CREATE TABLE `resource_dimensions` (
  `resource` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT '0',
  `height` int(11) DEFAULT '0',
  `file_size` bigint(20) DEFAULT NULL,
  `resolution` int(11) DEFAULT '0',
  `unit` varchar(11) DEFAULT '0',
  `page_count` int(11) DEFAULT NULL,
  KEY `resource` (`resource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource_keyword` (
  `resource` int(11) DEFAULT NULL,
  `keyword` int(11) DEFAULT NULL,
  `hit_count` int(11) DEFAULT '0',
  `position` int(11) DEFAULT '0',
  `resource_type_field` int(11) DEFAULT '0',
  `new_hit_count` int(11) DEFAULT '0',
  `annotation_ref` int(11) DEFAULT NULL,
  KEY `resource_keyword` (`resource`,`keyword`),
  KEY `resource` (`resource`),
  KEY `keyword` (`keyword`),
  KEY `resource_type_field` (`resource_type_field`),
  KEY `rk_all` (`resource`,`keyword`,`resource_type_field`,`hit_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource_log` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `resource` int(11) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `resource_type_field` int(11) DEFAULT NULL,
  `notes` text,
  `diff` text,
  `usageoption` int(11) DEFAULT NULL,
  `purchase_size` varchar(10) DEFAULT NULL,
  `purchase_price` decimal(10,2) DEFAULT '0.00',
  `access_key` char(50) DEFAULT NULL,
  `previous_value` longtext,
  `previous_file_alt_ref` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`),
  KEY `resource` (`resource`),
  KEY `type` (`type`),
  KEY `user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=259232 DEFAULT CHARSET=utf8;


CREATE TABLE `resource_node` (
  `resource` int(11) NOT NULL,
  `node` int(11) NOT NULL,
  `hit_count` int(11) DEFAULT '0',
  `new_hit_count` int(11) DEFAULT '0',
  PRIMARY KEY (`resource`,`node`),
  KEY `resource_node` (`resource`,`node`),
  KEY `resource` (`resource`),
  KEY `node` (`node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource_related` (
  `resource` int(11) DEFAULT NULL,
  `related` int(11) DEFAULT NULL,
  KEY `resource_related` (`resource`),
  KEY `related` (`related`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `resource_type` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `allowed_extensions` text,
  `order_by` int(11) DEFAULT NULL,
  `config_options` text,
  `tab_name` varchar(50) DEFAULT NULL,
  `push_metadata` int(11) DEFAULT NULL,
  `inherit_global_fields` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `resource_type_field` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `title` varchar(400) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `order_by` int(11) DEFAULT '0',
  `keywords_index` int(11) DEFAULT '0',
  `partial_index` int(11) DEFAULT '0',
  `resource_type` int(11) DEFAULT '0',
  `resource_column` varchar(50) DEFAULT NULL,
  `display_field` int(11) DEFAULT '1',
  `use_for_similar` int(11) DEFAULT '1',
  `iptc_equiv` varchar(20) DEFAULT NULL,
  `display_template` text,
  `tab_name` varchar(50) DEFAULT NULL,
  `required` int(11) DEFAULT '0',
  `smart_theme_name` varchar(200) DEFAULT NULL,
  `exiftool_field` varchar(200) DEFAULT NULL,
  `advanced_search` int(11) DEFAULT '1',
  `simple_search` int(11) DEFAULT '0',
  `help_text` text,
  `display_as_dropdown` int(11) DEFAULT '0',
  `external_user_access` int(11) DEFAULT '1',
  `autocomplete_macro` text,
  `hide_when_uploading` int(11) DEFAULT '0',
  `hide_when_restricted` int(11) DEFAULT '0',
  `value_filter` text,
  `exiftool_filter` text,
  `omit_when_copying` int(11) DEFAULT '0',
  `tooltip_text` text,
  `regexp_filter` varchar(400) DEFAULT NULL,
  `sync_field` int(11) DEFAULT NULL,
  `display_condition` varchar(400) DEFAULT NULL,
  `onchange_macro` text,
  `field_constraint` int(11) DEFAULT NULL,
  `linked_data_field` text,
  `automatic_nodes_ordering` tinyint(1) DEFAULT '0',
  `fits_field` varchar(255) DEFAULT NULL,
  `personal_data` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ref`),
  KEY `resource_type` (`resource_type`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;


CREATE TABLE `search_saved` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime DEFAULT NULL,
  `owner` int(11) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `search` text,
  `restypes` text,
  `archive` int(11) DEFAULT NULL,
  `enabled` int(11) DEFAULT NULL,
  `checksum` varchar(100) DEFAULT NULL,
  `checksum_when` datetime DEFAULT NULL,
  `checksum_matches` int(11) DEFAULT NULL,
  `checksum_data` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


CREATE TABLE `site_text` (
  `page` varchar(50) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `text` text,
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `language` varchar(10) DEFAULT NULL,
  `ignore_me` int(11) DEFAULT NULL,
  `specific_to_group` int(11) DEFAULT NULL,
  `custom` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;


CREATE TABLE `sysvars` (
  `name` varchar(50) DEFAULT NULL,
  `value` text,
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `usergroup` int(11) DEFAULT NULL,
  `last_active` datetime DEFAULT NULL,
  `logged_in` int(11) DEFAULT NULL,
  `last_browser` text,
  `last_ip` varchar(100) DEFAULT NULL,
  `current_collection` int(11) DEFAULT NULL,
  `accepted_terms` int(11) DEFAULT '0',
  `account_expires` datetime DEFAULT NULL,
  `comments` text,
  `session` varchar(50) DEFAULT NULL,
  `ip_restrict` text,
  `search_filter_override` text,
  `password_last_change` datetime DEFAULT NULL,
  `login_tries` int(11) DEFAULT '0',
  `login_last_try` datetime DEFAULT NULL,
  `approved` int(11) DEFAULT '1',
  `lang` varchar(11) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `hidden_collections` text,
  `password_reset_hash` varchar(100) DEFAULT NULL,
  `origin` varchar(50) DEFAULT NULL,
  `unique_hash` varchar(50) DEFAULT NULL,
  `wp_authrequest` varchar(50) DEFAULT NULL,
  `csrf_token` varchar(255) DEFAULT NULL,
  `simplesaml_custom_attributes` mediumtext,
  PRIMARY KEY (`ref`),
  KEY `session` (`session`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;


CREATE TABLE `user_collection` (
  `user` int(11) DEFAULT NULL,
  `collection` int(11) DEFAULT NULL,
  `request_feedback` int(11) DEFAULT '0',
  KEY `collection` (`collection`),
  KEY `user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user_dash_tile` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `dash_tile` int(11) DEFAULT NULL,
  `order_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=268 DEFAULT CHARSET=utf8;


CREATE TABLE `user_message` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL DEFAULT '0',
  `message` int(11) NOT NULL DEFAULT '0',
  `seen` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ref`,`user`,`message`,`seen`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;


CREATE TABLE `user_preferences` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `parameter` varchar(150) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;


CREATE TABLE `user_rating` (
  `user` int(11) DEFAULT '0',
  `rating` int(11) DEFAULT '0',
  `ref` int(11) DEFAULT '0',
  KEY `ref` (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user_report` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `params` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user_userlist` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `userlist_name` varchar(50) DEFAULT NULL,
  `userlist_string` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `usergroup` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `permissions` text,
  `fixed_theme` varchar(50) DEFAULT NULL,
  `parent` varchar(50) DEFAULT NULL,
  `search_filter` text,
  `edit_filter` text,
  `derestrict_filter` text,
  `ip_restrict` text,
  `resource_defaults` text,
  `config_options` text,
  `welcome_message` text,
  `request_mode` int(11) DEFAULT '0',
  `allow_registration_selection` int(11) DEFAULT '0',
  `group_specific_logo` text,
  `inherit_flags` text,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;


CREATE TABLE `usergroup_collection` (
  `usergroup` int(11) NOT NULL DEFAULT '0',
  `collection` int(11) NOT NULL DEFAULT '0',
  `request_feedback` int(11) DEFAULT '0',
  PRIMARY KEY (`usergroup`,`collection`),
  KEY `usergroup` (`usergroup`),
  KEY `collection` (`collection`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `usergroup_dash_tile` (
  `ref` int(11) NOT NULL AUTO_INCREMENT,
  `usergroup` int(11) DEFAULT NULL,
  `dash_tile` int(11) DEFAULT NULL,
  `default_order_by` int(11) DEFAULT NULL,
  `order_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SET FOREIGN_KEY_CHECKS = @ORIG_FOREIGN_KEY_CHECKS;

SET UNIQUE_CHECKS = @ORIG_UNIQUE_CHECKS;

SET @ORIG_TIME_ZONE = @@TIME_ZONE;
SET TIME_ZONE = @ORIG_TIME_ZONE;

SET SQL_MODE = @ORIG_SQL_MODE;
