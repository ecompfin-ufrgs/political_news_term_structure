from logger    import Logger
import logging
from database  import Database
from webdriver import Webdriver

class Scraper:
    def __init__(
        self,
        log_name        : str = "scraper",
        log_file        : str = "log.log",
        db_name         : str = "test.db",
        db_table        : str = "test"):
        self.logger     = Logger(log_name, log_file)
        self.database   = Database(db_name, db_table, log_file = log_file)
        self.webdriver  = Webdriver(log_file = log_file)

    def __del__(self):
        del self.database
        del self.webdriver

if __name__ == "__main__":
    s = Scraper()
    del s