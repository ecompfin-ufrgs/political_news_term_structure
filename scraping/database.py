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
    CREATE_WEBSITE = """
        CREATE TABLE IF NOT EXISTS websites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
        );
        """ 
    CREATE_ARTICLES = """
        CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        website_id INT,
        date DATETIME,
        title VARCHAR(255),
        link VARCHAR(255),
        FOREIGN KEY (website_id) REFERENCES websites(id)
        );
        """
    INSERT_WEBSITE = "INSERT INTO websites (name, short_name, url) VALUEs (?, ?, ?);"
    INSERT_ARTICLE = "INSERT INTO articles (website_id, date, title, link) VALUES (?, ?, ?, ?);"
    INSERT_TEXTS = "INSERT INTO texts (article_id, text) VALUES (?, ?);"
    
    def __init__(self,
        log_filename : str):
        
        self.logger = logger.Logger("database", log_filename)
        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="ubuntu",
            password="Ber8822?"
            )
        self.logger.debug("connected")
        self.cursor = self.conn.cursor()
        
        self.execute = self.cursor.execute
        
    def __del__(self):
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        self.logger.debug("commit")
        

if __name__ == "__main__":
    db = Database("log.log")
