-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2022-01-05 09:03:23
-- 伺服器版本： 10.4.22-MariaDB
-- PHP 版本： 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `pygame`
--

-- --------------------------------------------------------

--
-- 資料表結構 `record`
--

CREATE TABLE `record` (
  `player1` varchar(20) NOT NULL,
  `player2` varchar(20) NOT NULL,
  `player1_score` int(10) NOT NULL,
  `player2_score` int(10) NOT NULL,
  `time` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `record`
--

INSERT INTO `record` (`player1`, `player2`, `player1_score`, `player2_score`, `time`) VALUES
('u', 't', 24, 5, '2021-12-27 20:07:31.'),
('a', 'b', 1, 25, '2021-12-27 20:07:52.'),
('c', 'd', 5, 15, '2021-12-27 20:08:02.'),
('b', 'd', 0, 22, '2021-12-27 20:08:17.'),
('b', 'd', 0, 22, '2021-12-27 20:09:00.'),
('b', 'd', 0, 22, '2021-12-27 20:09:27.'),
('b', 'd', 0, 22, '2021-12-27 20:09:40.'),
('AAA', 'BBB', 10, 26, '2021-12-30 11:13:51.');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
