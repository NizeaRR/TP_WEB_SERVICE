CREATE TABLE IF NOT EXISTS Utilisateur(
    id serial PRIMARY KEY, 
    firstname VARCHAR(255) NOT NULL, 
    lastname VARCHAR(255) NOT NULL, 
    age int NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    job VARCHAR(255) NOT NULL);

CREATE TABLE IF NOT EXISTS Applications(
    id serial PRIMARY KEY, 
    appname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL, 
    lastconnection VARCHAR(255) NOT NULL, 
    user_id int,
    FOREIGN KEY (user_id) REFERENCES Utilisateur(id));