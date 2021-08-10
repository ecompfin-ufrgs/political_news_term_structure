"""
Title: Database Class
Description: Class which manages a SQLite3 database.
Version: 0.0.1
Author: Bernardo Paulsen
"""


import mysql.connector

import logger


class Database:
    """
    Connects to database and executes commands.
    """
    USE_DB = "USE news;"
    DROP_WEBSITE = "DROP TABLE websites;"
    DROP_ARTICLE = "DROP TABLE articles;"
    CREATE_WEBSITE = """
        CREATE TABLE websites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        short_name VARCHAR(20)
        );
        """ 
    CREATE_ARTICLE = """
        CREATE TABLE articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        website_id INT,
        date DATETIME,
        title VARCHAR(255),
        link VARCHAR(255),
        FOREIGN KEY (website_id) REFERENCES websites(id)
        );
        """
    INSERT_WEBSITE = "INSERT INTO websites (name, short_name) VALUES (%s, %s);"
    INSERT_ARTICLE = "INSERT INTO articles (website_id, date, title, link) VALUES (%s, %s, %s, %s);"
    INSERT_TEXTS = "INSERT INTO texts (article_id, text) VALUES (%s, %s);"
    
    def __init__(self,
        log_filename : str):
        
        self.logger = logger.Logger("database", log_filename)
        
        with open("password.txt") as file:
            password = file.read()
        self.conn = mysql.connector.connect(
            host="localhost",
            user="ubuntu",
            password=password
            )
        self.logger.debug("connected")
        self.cursor = self.conn.cursor()
        
        self.execute = self.cursor.execute
        
    def __del__(self):
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        self.logger.debug("commited")
        
    def query_website_id(self, name : str):
        self.execute(f"SELECT id FROM websites WHERE name = '{name}'")
        result = self.cursor.fetchall()
        website_id = result[0][0]
        self.logger.debug(f"website_id {website_id} from website {name} collected")
        return website_id
        
    def delete_articles(self, website_id : int):
        self.execute(f"DELETE FROM articles WHERE website_id = {website_id}")
        self.logger.debug(f"deleted all articles with website_id = {website_id}")
        
    def insert_article(self, values : tuple):
        self.execute(self.INSERT_ARTICLE, values)
        self.logger.debug(f"values ({values[0]}|{values[1]}|{values[2][-25:]}|{values[3][-25:]}) inserted")

if __name__ == "__main__":
    db = Database("log.log")
