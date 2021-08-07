"""
Title: Database Class
Description: Class which manages a SQLite3 database.
Version: 0.0.1
Author: Bernardo Paulsen
"""


import sqlite3

from logger 


class Database:
    """
    Connects to database and executes commands.
    """
    DB_NAME = "data.db"
    
    def __init__(self,
        log_filename : str):
        
        self.logger = logger.Logger("database", log_filename)
        
        self.conn = sqlite3.connect(self.DB_NAME)
        
        self.commit = self.conn.commit
        self.execute = self.conn.execute
        
    def __del__(self):
        self.conn.close()