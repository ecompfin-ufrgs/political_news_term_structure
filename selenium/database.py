"""
Title       : Database
Description : Defines class Database, which uses SQLite3 to manage a database file.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
from   logger import Logger
import sqlite3

import line_profiler
import atexit
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

class Database:
    """
    Class which connects to and edits database using SQLite3.
    
    :param name: Name of database file, defaults to "test.db"
    :type name: str, optional
    :param table: Name of table in database, defaults to "test"
    :type table: str, optional
    :param log_name: Logger name, defaults to "database"
    :type log_name: str, optional
    :param log_file: Log file name, defaults to "log.log"
    :type log_file: str, optional
    """
    def __init__(
        self,
        name     : str = "test.db",
        table    : str = "test",
        log_name : str = "database",
        log_file : str = "log"):
        """
        Constructor method.
        """
        self.logger        = Logger(log_name, log_file)
        self.name          = name
        self.table         = table
        self.conn          = self.config()
        self.insert_scrpit = f"INSERT INTO {self.table} (date, title) VALUES (?, ?);"

    def __del__(self):
        """
        Destructor method. Closes database connection.
        """
        self.conn.close()
        self.logger.debug(f"{self.name} connection closed")

    def commit(self):
        self.conn.commit()
        self.logger.debug("changes commited")

    def config(self):
        """
        Connects to database, drops table if it exists and creates new table.
        """
        self.logger.debug(f"{self.name} opening connection")
        conn = sqlite3.connect(self.name)
        self.logger.debug(f"{self.name} connection open")
        conn.execute(self.get_drop())
        self.logger.debug(f"{self.table} table dropped")
        conn.execute(self.get_create())
        self.logger.debug(f"{self.table} table created")
        return conn

    @profile
    def insert(self,
        date  : str, 
        title : str):
        """
        Inserts values into database.

        :param date: Article date
        :type date: str
        :param title: Article title
        :type title: str
        """
        values = (date, title)
        self.conn.execute(self.insert_scrpit,values)
        self.logger.debug(f"({date}|{title[:20]}) inserted into table in database")

    def get_drop(self):
        """
        Returns scrip used to drop table.
        """
        script = f"""
        DROP TABLE IF EXISTS {self.table};
        """
        return script

    def get_create(self):
        """
        Returns script used to create table.
        """
        script = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
        id    INT AUTO INCREMENT PRIMARY KEY,
        date  DATETIME,
        title VARCHAR(255),
        link  VARCHAR(255)
        );
        """
        return script

if __name__ == "__main__":
    db = Database(log_name="database test")
    del db
