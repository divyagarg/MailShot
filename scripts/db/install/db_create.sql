
DROP DATABASE IF EXISTS `MailShot`;
CREATE DATABASE IF NOT EXISTS `MailShot`;

use `MailShot`;

DROP TABLE IF EXISTS `Category`;
CREATE TABLE `Category` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `Template`;
CREATE TABLE `Template` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(128) DEFAULT NULL,
  `UserId` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE(`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



DROP TABLE IF EXISTS `Variant`;
CREATE TABLE `Variant` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `VariantName` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `HTML` longtext COLLATE utf8mb4_unicode_ci,
  `TemplateId` int(11) DEFAULT NULL,
  `Subject` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL
  PRIMARY KEY (`ID`),
  KEY `VTemplateId_idx` (`TemplateId`),
  CONSTRAINT `VTemplateId` FOREIGN KEY (`TemplateId`) REFERENCES `Template` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



DROP TABLE IF EXISTS `Campaign`;
CREATE TABLE `Campaign` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Status` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `SendTime` datetime DEFAULT NULL,
  `CategoryId` int(11) DEFAULT NULL,
  `CreateDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ModifiedDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `TemplateId` int(11) DEFAULT NULL,
  `UserId` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `CTemplateId_idx` (`TemplateId`),
  KEY `CCategoryId_idx` (`CategoryId`),
  CONSTRAINT `CCategoryId` FOREIGN KEY (`CategoryId`) REFERENCES `Category` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `CTemplateId` FOREIGN KEY (`TemplateId`) REFERENCES `Template` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `Segment`;
CREATE TABLE `Segment` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `CampaignSegmentMap`;
CREATE TABLE `CampaignSegmentMap` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `CampaignId` int(11) DEFAULT NULL,
  `SegmentId` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Id_idx` (`CampaignId`),
  KEY `Id_idx1` (`SegmentId`),
  CONSTRAINT `CampaignSegmentId1` FOREIGN KEY (`CampaignId`) REFERENCES `Campaign` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `CampaignSegmentId2` FOREIGN KEY (`SegmentId`) REFERENCES `Segment` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `CampaignSummary`;
CREATE TABLE `CampaignSummary` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `CampaignId` int(11) DEFAULT NULL,
  `ContactCount` int(11) DEFAULT NULL,
  `ClickCount` int(11) DEFAULT '0',
  `UniqueClickCount` int(11) DEFAULT '0',
  `OpenCount` int(11) DEFAULT '0',
  `BounceCount` int(11) DEFAULT '0',
  `SpamCount` int(11) DEFAULT '0',
  `VariantId` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `CampaignId_UNIQUE` (`CampaignId`),
  KEY `CSTemplateId_idx` (`VariantId`),
  CONSTRAINT `CSCampaign` FOREIGN KEY (`CampaignId`) REFERENCES `Campaign` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `CSTemplateId` FOREIGN KEY (`VariantId`) REFERENCES `Template` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;





DROP TABLE IF EXISTS `ContactInfo`;
CREATE TABLE `ContactInfo` (
  `ContactId` int(11) NOT NULL AUTO_INCREMENT,
  `Email` varchar(128) DEFAULT NULL,
  `Name` varchar(128) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Gender` enum('F','M','O') DEFAULT NULL,
  `IsValid` tinyint(4) DEFAULT '1',
  `SubscriptionStatus` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`ContactId`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ContactSegmentMap`;
CREATE TABLE `ContactSegmentMap` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ContactId` int(11) DEFAULT NULL,
  `SegmentId` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `ContactId_idx` (`ContactId`),
  KEY `Id_idx` (`SegmentId`),
  CONSTRAINT `ContactId` FOREIGN KEY (`ContactId`) REFERENCES `ContactInfo` (`ContactId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Id` FOREIGN KEY (`SegmentId`) REFERENCES `Segment` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `MailTrack`;
CREATE TABLE `MailTrack` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `UserTrackerId` binary(16) DEFAULT NULL,
  `CampaignId` int(11) DEFAULT NULL,
  `ContactId` int(11) DEFAULT NULL,
  `OpenStatus` tinyint(4) DEFAULT '0',
  `DeliveryStatus` tinyint(4) DEFAULT '0',
  `BounceStatus` tinyint(4) DEFAULT '0',
  `IsSpam` tinyint(4) DEFAULT '0',
  `IsSample` tinyint(4) DEFAULT '0',
  `VariantId` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `TrackerId_UNIQUE` (`UserTrackerId`),
  KEY `Id_idx` (`CampaignId`),
  KEY `ContactId_idx` (`ContactId`),
  KEY `MTTemplateId_idx` (`VariantId`),
  CONSTRAINT `MTCampaignId` FOREIGN KEY (`CampaignId`) REFERENCES `Campaign` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `MTContactId` FOREIGN KEY (`ContactId`) REFERENCES `ContactInfo` (`ContactId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `MTVariantId` FOREIGN KEY (`VariantId`) REFERENCES `Variant` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `LinkTrack`;
CREATE TABLE `LinkTrack` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `UserTrackerId` binary(16) DEFAULT NULL,
  `Link` varchar(516) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RedirectId` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ClickCount` int(11) DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `RedirectId_UNIQUE` (`RedirectId`),
  KEY `CampaignLinkMap_Id` (`UserTrackerId`),
  CONSTRAINT `CampaignLinkMap_Id` FOREIGN KEY (`UserTrackerId`) REFERENCES `MailTrack` (`UserTrackerId`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



DROP TABLE IF EXISTS `SampleCampaignSummary`;
CREATE TABLE `SampleCampaignSummary` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `CampaignId` int(11) DEFAULT NULL,
  `ContactCount` int(11) DEFAULT NULL,
  `ClickCount` int(11) DEFAULT '0',
  `UniqueClickCount` int(11) DEFAULT '0',
  `OpenCount` int(11) DEFAULT '0',
  `BounceCount` int(11) DEFAULT '0',
  `SpamCount` int(11) DEFAULT '0',
  `VariantId` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `CSTemplateId_idx` (`VariantId`),
  KEY `SCSCampaign` (`CampaignId`),
  CONSTRAINT `SCSCampaign` FOREIGN KEY (`CampaignId`) REFERENCES `Campaign` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `SCSVariant` FOREIGN KEY (`VariantId`) REFERENCES `Variant` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



DROP TABLE IF EXISTS `TestParameters`;
CREATE TABLE `TestParameters` (
  `Id` int(11) NOT NULL,
  `CampaignId` int(11) DEFAULT NULL,
  `Winner` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TestTime` int(11) DEFAULT NULL,
  `SendTime` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `CampaignId_UNIQUE` (`CampaignId`),
  CONSTRAINT `TPCampaignId` FOREIGN KEY (`CampaignId`) REFERENCES `Campaign` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



