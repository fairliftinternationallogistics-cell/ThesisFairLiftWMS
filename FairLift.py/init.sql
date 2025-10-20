-- init.sql
-- Run this in http://localhost/phpmyadmin -> fairlift_db -> SQL
CREATE DATABASE IF NOT EXISTS fairlift_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fairlift_db;

CREATE TABLE IF NOT EXISTS parcels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tracking_number VARCHAR(50) NOT NULL,
  size VARCHAR(10) DEFAULT 'S',
  weight DECIMAL(10,2) DEFAULT 0.00,
  arrival_date DATE DEFAULT CURRENT_DATE,
  destination VARCHAR(100) DEFAULT '',
  status VARCHAR(50) DEFAULT 'stored',
  location_rack VARCHAR(50) DEFAULT '',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- sample data
INSERT INTO parcels (tracking_number, size, weight, arrival_date, destination, status, location_rack)
VALUES
('FL-0001', 'S', 1.2, '2025-09-10', 'Manila', 'stored', 'R1'),
('FL-0002', 'L', 12.5, '2025-09-12', 'Cebu', 'stored', 'R2'),
('FL-0003', 'M', 4.1, '2025-09-15', 'Manila', 'pending', 'R1'),
('FL-0004', 'XL', 25.0, '2025-09-17', 'Davao', 'stored', 'R5'),
('FL-0005', 'S', 0.5, '2025-09-18', 'Iloilo', 'stored', 'R3');
