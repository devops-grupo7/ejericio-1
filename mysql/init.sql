CREATE DATABASE IF NOT EXISTS players;
CREATE TABLE IF NOT EXISTS players.players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(25) UNIQUE NOT NULL 
)  ENGINE=INNODB;

INSERT INTO players (player_name) VALUES ("JUAN")
INSERT INTO players (player_name) VALUES ("VICTOR")
INSERT INTO players (player_name) VALUES ("VLADIMIR")
INSERT INTO players (player_name) VALUES ("CRISTIAN")
INSERT INTO players (player_name) VALUES ("ARIADNA")

CREATE TABLE IF NOT EXISTS players.categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(25) UNIQUE NOT NULL, 
    description VARCHAR(75) NOT NULL 
)  ENGINE=INNODB;

INSERT INTO players.categories (name, description) VALUES ("CATEGORIA-A", "Categoría alta")
INSERT INTO players.categories (name, description) VALUES ("CATEGORIA-B", "Categoría media")


CREATE TABLE IF NOT EXISTS players.teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    team_name VARCHAR(50) UNIQUE NOT NULL,
    team_description VARCHAR(50) 
)  ENGINE=INNODB;

INSERT INTO players.teams (team_name, category_id,team_description) VALUES ("RIVER", 1, "EQUIPO BELGRANO R")
INSERT INTO players.teams (team_name, category_id,team_description) VALUES ("BOCA", 2, "EQUIPO BAJO BOCA")


CREATE TABLE IF NOT EXISTS players.match(
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    team_1 INT NULL,
    team_2 INT NULL,
    match_score VARCHAR(50)
) ENGINE=INNODB;

INSERT INTO players.match (team_1, team_2,match_score) VALUES (1,2, "2-1")
