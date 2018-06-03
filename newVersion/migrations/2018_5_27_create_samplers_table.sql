CREATE TABLE `samplers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `electorate_nm` varchar(200) NOT NULL DEFAULT '',
  `vote_collection_point_nm` varchar(200) NOT NULL DEFAULT '',
  `vote_collection_point_id` varchar(200) NOT NULL DEFAULT '',
  `batch_no` int(11) NOT NULL,
  `paper_no` int(11) NOT NULL,
  `preferences` text NOT NULL,
  `match` int(11) DEFAULT NULL,
  `preferences_after_audit` text,
  `job_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;