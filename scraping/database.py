"""
Title: Database Class
Description: Class which manages a SQLite3 database.
Version: 0.0.1
Author: Bernardo Paulsen
"""


import sqlite3

from logger import Logger


class Database:
    """
    Connects to database and executes commands.
    """
    def __init__(self,
        log_filename : str,
        db_name : str = "data.db"):
        
        self.logger = Logger("database", log_filename)
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.commit = self.conn.commit
        self.execute = self.conn.execute
        
    def __del__(self):
        self.conn.close()