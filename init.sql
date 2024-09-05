-- Create the database 'testdb' if it doesn't already exist
CREATE DATABASE IF NOT EXISTS testdb;

-- Use the database
USE testdb;

-- Create a table 'users' in the 'testdb' database
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);

-- Grant full root permissions
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

-- Flush privileges to make sure changes take effect
FLUSH PRIVILEGES;
