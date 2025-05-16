-- 1. users: autenticación y roles
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(128) NOT NULL,
  role ENUM('User','Admin') NOT NULL DEFAULT 'User',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. boxes: definición de boxes
CREATE TABLE boxes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  corridor VARCHAR(50) NOT NULL,
  specialty VARCHAR(100) NOT NULL,
  status ENUM('Free','Occupied','Disabled') NOT NULL DEFAULT 'Free'
);

-- 3. availability: franjas asignadas a boxes
CREATE TABLE availability (
  id INT AUTO_INCREMENT PRIMARY KEY,
  box_id INT NOT NULL,
  doctor_name VARCHAR(150),
  start_time DATETIME,
  end_time DATETIME,
  FOREIGN KEY (box_id) REFERENCES boxes(id)
);
