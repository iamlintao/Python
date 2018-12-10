-- phpMyAdmin SQL Dump
-- version 4.1.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2018-12-04 07:09:08
-- 服务器版本： 5.6.16
-- PHP Version: 5.5.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `p7dy`
--

-- --------------------------------------------------------

--
-- 表的结构 `category`
--

CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影分类表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `country`
--

CREATE TABLE IF NOT EXISTS `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_name` varchar(255) NOT NULL COMMENT '国家名字',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='国家表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `download`
--

CREATE TABLE IF NOT EXISTS `download` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL,
  `download_type` tinyint(4) NOT NULL COMMENT '下载类型，1 迅雷 2 电驴 3 百度网盘 4 ftp',
  `download_url` varchar(255) NOT NULL COMMENT '下载地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影下载地址' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `language`
--

CREATE TABLE IF NOT EXISTS `language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_name` varchar(255) NOT NULL COMMENT '语言名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `movies`
--

CREATE TABLE IF NOT EXISTS `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title_cn` varchar(255) NOT NULL,
  `short_title` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `cover` varchar(255) NOT NULL,
  `year` int(11) NOT NULL,
  `country` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `language` varchar(255) NOT NULL,
  `sub_title` varchar(255) NOT NULL,
  `release_time` varchar(255) NOT NULL,
  `imdb_score` varchar(255) NOT NULL,
  `douban_score` varchar(255) NOT NULL,
  `file_format` varchar(255) NOT NULL,
  `ratio` varchar(255) NOT NULL,
  `length` varchar(255) NOT NULL,
  `director` varchar(255) NOT NULL,
  `writers` varchar(255) NOT NULL,
  `actors` varchar(255) NOT NULL COMMENT '主演',
  `profiles` varchar(255) NOT NULL COMMENT '简介',
  `create_time` varchar(255) NOT NULL COMMENT '演员id，多个用半角逗号分割',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影基础信息表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `release`
--

CREATE TABLE IF NOT EXISTS `release` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `release_time` varchar(255) NOT NULL COMMENT '上映时间',
  `release_country` varchar(255) NOT NULL COMMENT '上映地区',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='上映时间表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `score`
--

CREATE TABLE IF NOT EXISTS `score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL COMMENT '电影id',
  `score_type` tinyint(4) NOT NULL COMMENT '1 豆瓣评分 2 IMDb 评分',
  `score` varchar(255) NOT NULL COMMENT '评分',
  `from_user` int(11) NOT NULL COMMENT '评分用户数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影评分表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `subtitle`
--

CREATE TABLE IF NOT EXISTS `subtitle` (
  `1` int(11) NOT NULL AUTO_INCREMENT,
  `subtitle_name` int(11) NOT NULL COMMENT '字幕名称',
  PRIMARY KEY (`1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='字幕' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `worker`
--

CREATE TABLE IF NOT EXISTS `worker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_type` tinyint(4) NOT NULL COMMENT '工作人员类型，1 导演 2 演员 3 编剧',
  `worker_name` varchar(255) NOT NULL COMMENT '名字（前半部分）',
  `worker_name_sec` varchar(255) NOT NULL COMMENT '名字（英文名字等）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='导演演员表' AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
