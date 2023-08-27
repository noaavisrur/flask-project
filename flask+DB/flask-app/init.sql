-- Create the database
CREATE DATABASE IF NOT EXISTS devopsroles;
USE devopsroles;

-- Create the table for storing song lyrics
CREATE TABLE IF NOT EXISTS lyrics_table (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255),
  artist VARCHAR(255),
  lyrics TEXT
);
