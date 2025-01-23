-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: vacationbooking
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vacations`
--

DROP TABLE IF EXISTS `vacations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vacations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `price` float DEFAULT NULL,
  `likes` int DEFAULT NULL,
  `image_url` varchar(250) DEFAULT NULL,
  `countries_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vacations_countries1_idx` (`countries_id`),
  CONSTRAINT `fk_vacations_countries1` FOREIGN KEY (`countries_id`) REFERENCES `countries` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vacations`
--

LOCK TABLES `vacations` WRITE;
/*!40000 ALTER TABLE `vacations` DISABLE KEYS */;
INSERT INTO `vacations` VALUES (2,'Vacation to Israel','Explore the beauty of Israel.','2025-07-01','2025-07-08',1050,0,NULL,1),(3,'Vacation to United States','Explore the beauty of United States.','2025-07-02','2025-07-09',1100,0,NULL,2),(4,'Vacation to Canada','Explore the beauty of Canada.','2025-07-03','2025-07-10',1150,0,NULL,3),(5,'Vacation to Germany','Explore the beauty of Germany.','2025-07-04','2025-07-11',1200,0,NULL,4),(6,'Vacation to France','Explore the beauty of France.','2025-07-05','2025-07-12',1250,0,NULL,5),(7,'Vacation to United Kingdom','Explore the beauty of United Kingdom.','2025-07-06','2025-07-13',1300,0,NULL,6),(8,'Vacation to Italy','Explore the beauty of Italy.','2025-07-07','2025-07-14',1350,0,NULL,7),(9,'Vacation to Spain','Explore the beauty of Spain.','2025-07-08','2025-07-15',1400,0,NULL,8),(10,'Vacation to Australia','Explore the beauty of Australia.','2025-07-09','2025-07-16',1450,0,NULL,9),(11,'Vacation to Japan','Explore the beauty of Japan.','2025-07-10','2025-07-17',1500,0,NULL,10),(12,'Vacation to China','Explore the beauty of China.','2025-07-11','2025-07-18',1550,0,NULL,11),(13,'Vacation to India','Explore the beauty of India.','2025-07-12','2025-07-19',1600,0,NULL,12),(14,'Vacation to Mexico','Explore the beauty of Mexico.','2025-07-13','2025-07-20',1650,0,NULL,13),(15,'Vacation to Brazil','Explore the beauty of Brazil.','2025-07-14','2025-07-21',1700,0,NULL,14);
/*!40000 ALTER TABLE `vacations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-23  9:14:02
