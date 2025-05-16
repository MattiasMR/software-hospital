-- Crea la base de datos
CREATE DATABASE IF NOT EXISTS hospital
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Crea el usuario
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'pass';

-- Permisos
GRANT ALL PRIVILEGES ON hospital.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
