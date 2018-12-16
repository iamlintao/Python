-- phpMyAdmin SQL Dump
-- version 4.7.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2018-12-13 10:34:36
-- 服务器版本： 10.1.29-MariaDB
-- PHP Version: 7.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `p7dy`
--

-- --------------------------------------------------------

--
-- 表的结构 `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL COMMENT '分类名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影分类表';

--
-- 转存表中的数据 `category`
--

INSERT INTO `category` (`id`, `category_name`) VALUES
(1, '科幻'),
(2, '悬疑'),
(3, '惊悚');

-- --------------------------------------------------------

--
-- 表的结构 `country`
--

CREATE TABLE `country` (
  `id` int(11) NOT NULL,
  `country_name` varchar(255) NOT NULL COMMENT '国家名字'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='国家表';

--
-- 转存表中的数据 `country`
--

INSERT INTO `country` (`id`, `country_name`) VALUES
(1, '美国'),
(2, '英国'),
(3, '\'countryName\''),
(4, '\'countryName\''),
(5, '\'countryName\''),
(6, '\'countryName\''),
(7, '\'countryName\''),
(8, '\'countryName\''),
(9, '\'countryName\''),
(10, '\'countryName\''),
(11, '\'countryName\''),
(12, '\'countryName\''),
(13, '加拿大'),
(14, '');

-- --------------------------------------------------------

--
-- 表的结构 `download`
--

CREATE TABLE `download` (
  `id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `download_type` tinyint(4) NOT NULL COMMENT '下载类型，1 迅雷 2 电驴 3 百度网盘 4 ftp 5 magnet( 磁力链)',
  `download_url` varchar(2550) NOT NULL COMMENT '下载地址'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影下载地址';

--
-- 转存表中的数据 `download`
--

INSERT INTO `download` (`id`, `movie_id`, `download_type`, `download_url`) VALUES
(1, 1, 1, 'ftp://ygdy8:ygdy8@yg45.dydytt.net:3155/阳光电影www.ygdy8.com.网络谜踪.BD.720p.中英双字幕.mkv'),
(2, 1, 5, 'magnet:?xt=urn:btih:3dcecfe415c6244a059ba4dfca0bdc5d3ef38759&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e5%bd%b1.HD.1080p.%e5%9b%bd%e8%af%ad%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97.mp4&amp;tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'),
(3, 1, 5, 'magnet:?xt=urn:btih:3dcecfe415c6244a059ba4dfca0bdc5d3ef38759&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e5%bd%b1.HD.1080p.%e5%9b%bd%e8%af%ad%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97.mp4&amp;tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'),
(4, 1, 5, 'magnet:?xt=urn:btih:3dcecfe415c6244a059ba4dfca0bdc5d3ef38759&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e5%bd%b1.HD.1080p.%e5%9b%bd%e8%af%ad%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97.mp4&amp;tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&amp;tr=udp%3a%2f%2fthetracker.org%3a80%2fannounce&amp;tr=http%3a%2f%2fretracker.telecom.by%2fannounce');

-- --------------------------------------------------------

--
-- 表的结构 `language`
--

CREATE TABLE `language` (
  `id` int(11) NOT NULL,
  `language_name` varchar(255) NOT NULL COMMENT '语言名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `language`
--

INSERT INTO `language` (`id`, `language_name`) VALUES
(1, '英语'),
(2, '西班牙语');

-- --------------------------------------------------------

--
-- 表的结构 `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL COMMENT '标题',
  `short_title` varchar(255) NOT NULL COMMENT '短标题（名称）',
  `name_cn` varchar(255) NOT NULL COMMENT '翻译名',
  `name_en` varchar(255) NOT NULL COMMENT '英文名',
  `cover` varchar(255) NOT NULL COMMENT '封面图',
  `publish_year` int(11) NOT NULL COMMENT '上映年份',
  `country` varchar(255) NOT NULL COMMENT '产地',
  `category` varchar(255) NOT NULL COMMENT '分类，多个用半角逗号分隔',
  `languages` varchar(255) NOT NULL COMMENT '语言',
  `sub_title` varchar(255) NOT NULL COMMENT '字幕',
  `release_time` varchar(255) NOT NULL COMMENT '上映时间',
  `file_format` varchar(255) NOT NULL COMMENT '文件格式',
  `ratio` varchar(255) NOT NULL COMMENT '分辨率',
  `time_length` varchar(255) NOT NULL COMMENT '时长',
  `director` varchar(255) NOT NULL COMMENT '导演',
  `writers` varchar(255) NOT NULL COMMENT '编剧',
  `actors` varchar(255) NOT NULL COMMENT '主演',
  `profiles` varchar(255) NOT NULL COMMENT '简介',
  `create_time` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影基础信息表';

-- --------------------------------------------------------

--
-- 表的结构 `released`
--

CREATE TABLE `released` (
  `id` int(11) NOT NULL,
  `release_time` varchar(255) NOT NULL COMMENT '上映时间',
  `release_area` varchar(255) NOT NULL COMMENT '上映地区'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='上映时间表';

--
-- 转存表中的数据 `released`
--

INSERT INTO `released` (`id`, `release_time`, `release_area`) VALUES
(1, '2018-08-31', '威尼斯电影节'),
(2, '2018-10-05', '美国');

-- --------------------------------------------------------

--
-- 表的结构 `score`
--

CREATE TABLE `score` (
  `id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL COMMENT '电影id',
  `score_type` tinyint(4) NOT NULL COMMENT '1 豆瓣评分 2 IMDb 评分',
  `score` varchar(255) NOT NULL COMMENT '评分',
  `from_user` int(11) NOT NULL COMMENT '评分用户数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影评分表';

--
-- 转存表中的数据 `score`
--

INSERT INTO `score` (`id`, `movie_id`, `score_type`, `score`, `from_user`) VALUES
(1, 1, 1, '5.3', 19921);

-- --------------------------------------------------------

--
-- 表的结构 `subtitle`
--

CREATE TABLE `subtitle` (
  `id` int(11) NOT NULL,
  `subtitle_name` varchar(255) NOT NULL COMMENT '字幕名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='字幕';

--
-- 转存表中的数据 `subtitle`
--

INSERT INTO `subtitle` (`id`, `subtitle_name`) VALUES
(1, '0'),
(2, '中英双字幕');

-- --------------------------------------------------------

--
-- 表的结构 `worker`
--

CREATE TABLE `worker` (
  `id` int(11) NOT NULL,
  `worker_type` tinyint(4) NOT NULL COMMENT '工作人员类型，1 导演 2 演员 3 编剧',
  `worker_name_cn` varchar(255) NOT NULL COMMENT '名字（中文音译）',
  `worker_name_en` varchar(255) NOT NULL COMMENT '名字（英文）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='导演演员表';

--
-- 转存表中的数据 `worker`
--

INSERT INTO `worker` (`id`, `worker_type`, `worker_name_cn`, `worker_name_en`) VALUES
(1, 2, '查宁·塔图姆', 'Channing Tatum'),
(2, 2, '詹姆斯·柯登', 'James Corden'),
(3, 2, '赞达亚', 'Zendaya'),
(4, 2, '勒布朗·詹姆斯', 'LeBron James'),
(5, 2, '科曼', 'Common'),
(6, 2, '吉娜·罗德里格兹', 'Gina Rodriguez'),
(7, 2, '丹尼·德维托', 'Danny DeVito'),
(8, 2, '吉米·塔特罗', 'Jimmy Tatro'),
(9, 2, '雅拉·沙希迪', 'Yara Shahidi'),
(10, 2, '伊利·亨利', 'Ely Henry');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `country`
--
ALTER TABLE `country`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `download`
--
ALTER TABLE `download`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `language`
--
ALTER TABLE `language`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `released`
--
ALTER TABLE `released`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subtitle`
--
ALTER TABLE `subtitle`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `worker`
--
ALTER TABLE `worker`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用表AUTO_INCREMENT `country`
--
ALTER TABLE `country`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- 使用表AUTO_INCREMENT `download`
--
ALTER TABLE `download`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `language`
--
ALTER TABLE `language`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `released`
--
ALTER TABLE `released`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `score`
--
ALTER TABLE `score`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `subtitle`
--
ALTER TABLE `subtitle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `worker`
--
ALTER TABLE `worker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
