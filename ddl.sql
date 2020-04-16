-- ----------------------------------------
-- Database trading_db
-- ----------------------------------------
DROP DATABASE IF EXISTS `tradingdemodb`;
CREATE DATABASE `tradingdemodb`;

-- ----------------------------------------------------------
-- Change database to tradingdemodb
-- ----------------------------------------------------------
USE tradingdemodb;

-- --------------------------------------------------
-- Table structure for account_info
-- --------------------------------------------------
DROP TABLE IF EXISTS  `account_info`;
CREATE TABLE `account_info` (
    `id` int(11)  UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(20)  NOT NULL DEFAULT '' COMMENT 'user name',
    `balance` decimal(19,4) NOT NULL,
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;

-- --------------------------------------------------
-- Table structure for trading_records
-- --------------------------------------------------
DROP TABLE IF EXISTS `trading_records`;
CREATE TABLE IF NOT EXISTS `trading_records` (
    `id` int(11)  UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` int(11) UNSIGNED NOT NULL COMMENT 'id in account_info table',
    `trade_amount` decimal(19,4)  NOT NULL,
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
