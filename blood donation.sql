CREATE DATABASE Vaibhav1;

USE Vaibhav1;

CREATE TABLE project (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Mobile_number VARCHAR(15) NOT NULL,
    City VARCHAR(100),
    Address VARCHAR(255),
    Passw VARCHAR(20) NOT NULL  -- Password stored as a string
);

