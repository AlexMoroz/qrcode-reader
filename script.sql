DROP DATABASE students;
CREATE DATABASE students;
USE students;

CREATE TABLE `attend` (
  `token` varchar(32) NOT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `present` (
  `token` varchar(32) NOT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

