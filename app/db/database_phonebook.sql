CREATE DATABASE IF NOT EXISTS phonebook_db;
USE phonebook_db;

CREATE TABLE contacts (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          phone_number CHAR(10) NOT NULL UNIQUE,
                          first_name VARCHAR(255) NOT NULL,
                          last_name VARCHAR(255) NOT NULL,
                          address VARCHAR(255),
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                          CHECK (phone_number REGEXP '^[0-9]{10}$')
    );