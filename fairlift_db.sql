-- fairlift_db.sql
-- Creates database and events table with start/end datetimes and description

CREATE DATABASE IF NOT EXISTS fairlift_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE fairlift_db;

CREATE TABLE IF NOT EXISTS events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  start_datetime DATETIME NOT NULL,
  end_datetime DATETIME DEFAULT NULL,
  type VARCHAR(50) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
