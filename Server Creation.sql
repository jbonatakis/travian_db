/*Written by Duncan McConnell
USE line must be changed each time. */

USE blackbla_uk3;

CREATE TABLE `total_table` (
  `playerid` int(11) DEFAULT NULL,
  `xCoord` int(11) DEFAULT NULL,
  `yCoord` int(11) DEFAULT NULL,
  `tID` int(11) DEFAULT NULL,
  `vID` int(11) DEFAULT NULL,
  `village` varchar(50) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `player` varchar(50) DEFAULT NULL,
  `aID` int(11) DEFAULT NULL,
  `aName` varchar(50) DEFAULT NULL,
  `population` int(11) DEFAULT NULL,
  `createdTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE total_table CONVERT TO CHARACTER SET utf8;