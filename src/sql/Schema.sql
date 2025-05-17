-- 1. Crear la base de datos y el usuario
DROP DATABASE hospital;
CREATE DATABASE IF NOT EXISTS hospital
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
  
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON hospital.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

USE hospital;