from   logger import Logger
import sqlite3

class Database:
    def __init__(
        self,
        name        : str = "test.db",
        table       : str = "test",
        log_name    : str = "database"):

        self.logger      = Logger(log_name)

        self.name        = name
        self.table       = table
        self.conn        = self.config()

    def __del__(self):
        self.conn.close()
        self.logger.debug(f"{self.name} connection closed")

    def config(self):
        conn = sqlite3.connect(self.name)
        self.logger.debug(f"{self.name} connection open")
        conn.execute(self.get_drop())
        self.logger.debug(f"{self.table} table dropped")
        conn.execute(self.get_create())
        self.logger.debug(f"{self.table} table created")
        return conn

    def insert(self,
        date  : str, 
        title : str):
        values = (date, title)
        self.conn.execute(self.get_insert(),values)
        self.conn.commit()
        self.logger.debug(f"{values} inserted into {self.name}")

    def get_drop(self):
        script = f"""
        DROP TABLE IF EXISTS {self.table};
        """
        return script

    def get_create(self):
        script = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
        id    INT AUTO INCREMENT PRIMARY KEY,
        date  DATETIME,
        title VARCHAR(255),
        link  VARCHAR(255)
        );
        """
        return script

    def get_insert(self):
        script = f"""
        INSERT INTO {self.table} (date, title)
        VALUES (?, ?);
        """
        return script

if __name__ == "__main__":
    db = Database(log_name="database test")
    del db
