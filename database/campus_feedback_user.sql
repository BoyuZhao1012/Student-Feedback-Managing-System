-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: campus_feedback
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'张三','pbkdf2:sha256:600000$kIC6kV79Flhon3fc$d978ec62253f69d0faba81b3fbd1496b3f9d21283917634a8c887557a7e68e82','student','https://api.dicebear.com/7.x/avataaars/svg?seed=张三','2025-06-13 11:51:34'),(2,'李四','pbkdf2:sha256:600000$KjrhV3G1X0mU8UE5$ae88cc89c450b31de9d0b9417cfb32aef0f00329465593474948a58962a71b74','admin','https://api.dicebear.com/7.x/avataaars/svg?seed=李四','2025-06-13 11:51:34'),(3,'王五','pbkdf2:sha256:600000$ajeSzDyYenokKlz1$cf68b77da484272b7937f59e8e83ef11e1e2a7d0189855ce56218fbc97b10a18','supervisor','https://api.dicebear.com/7.x/avataaars/svg?seed=王五','2025-06-13 11:51:34'),(4,'赵六','pbkdf2:sha256:600000$0I5LC78gYzMU6Qsi$7a78217f94edad0d8e47e18358e001e710b2bcf2daefa29626d462460849d2c0','specialist','https://api.dicebear.com/7.x/avataaars/svg?seed=赵六','2025-06-13 11:51:34'),(6,'Mary','pbkdf2:sha256:600000$XrZxlhw08UtVlXTi$02d347aa76f210f71e6e32daffaef5d80c32937f26ab616e678040c85e5337ce','student','https://api.dicebear.com/7.x/avataaars/svg?seed=Mary','2025-06-18 09:25:45'),(7,'小明','pbkdf2:sha256:600000$bEBHWkAenkkxKv4h$1d52c8c1b4c9a92674fa00946c434265b9a13e5aa9ab3316ce4c97d45abd63d9','student','https://api.dicebear.com/7.x/avataaars/svg?seed=小明','2025-06-27 17:05:27');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-12 14:28:32
