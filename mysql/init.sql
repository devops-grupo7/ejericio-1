CREATE DATABASE IF NOT EXISTS players;
CREATE TABLE IF NOT EXISTS players.players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(25) UNIQUE NOT NULL 
)  ENGINE=INNODB;
