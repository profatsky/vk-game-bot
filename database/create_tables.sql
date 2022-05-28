CREATE TABLE `admins` (
  `admin_id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `lvl` tinyint(1) DEFAULT '1',
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `mining` (
  `mining_id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `low_card` datetime DEFAULT NULL,
  `medium_card` datetime DEFAULT NULL,
  `high_card` datetime DEFAULT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `reports` (
  `report_id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` varchar(256) NOT NULL,
  `is_answered` tinyint(1) DEFAULT '0',
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
)

CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `vk_id` int NOT NULL,
  `balance` int NOT NULL DEFAULT '0',
  `skin` tinyint NOT NULL,
  `face` tinyint NOT NULL,
  `haircut` tinyint NOT NULL,
  `clothes` tinyint NOT NULL DEFAULT '0',
  `nickname` varchar(16) NOT NULL,
  `slot_1` varchar(11) NOT NULL DEFAULT 'no_card',
  `slot_2` varchar(11) NOT NULL DEFAULT 'no_card',
  `slot_3` varchar(11) NOT NULL DEFAULT 'no_card'
)