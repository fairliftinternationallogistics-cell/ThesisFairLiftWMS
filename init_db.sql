CREATE DATABASE IF NOT EXISTS fairlift_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fairlift_db;

-- users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(256) NOT NULL,
  role VARCHAR(50) DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- parcels
CREATE TABLE IF NOT EXISTS parcels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tracking_number VARCHAR(64) NOT NULL UNIQUE,
  size VARCHAR(10),
  weight DOUBLE,
  arrival_date DATE,
  destination VARCHAR(200),
  status VARCHAR(50) DEFAULT 'stored',
  location_rack VARCHAR(64),
  metadata JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- tickets
CREATE TABLE IF NOT EXISTS tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  parcel_id INT NOT NULL,
  created_by INT,
  department VARCHAR(120),
  status VARCHAR(50) DEFAULT 'open',
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (parcel_id) REFERENCES parcels(id) ON DELETE CASCADE,
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- drivers
CREATE TABLE IF NOT EXISTS drivers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  phone VARCHAR(50),
  vehicle_plate VARCHAR(50),
  current_lat DOUBLE,
  current_lng DOUBLE,
  status VARCHAR(50) DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- sample user (password: password123) -- we'll insert hashed password via Python snippet below
INSERT INTO parcels (tracking_number, size, weight, arrival_date, destination, status, location_rack, metadata)
VALUES
('FL-0001','S',1.2,'2025-09-10','Manila','stored','R1','{\"notes\":\"fragile\"}'),
('FL-0002','L',12.5,'2025-09-12','Cebu','stored','R2','{\"notes\":\"heavy\"}');
