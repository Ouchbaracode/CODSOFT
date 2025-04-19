create database contactapp;
use contactapp;

CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE USER 'Mohamed'@'localhost' IDENTIFIED BY 'mohamed@mysql';
GRANT ALL PRIVILEGES ON *.* TO 'Mohamed'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

