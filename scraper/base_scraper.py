from database import Database
from logger import Logger
from webdriver import Webdriver


class BaseScraper:
    """
    Basic scraper.
    """
    LOG_FILENAME: str
    
    def __init__(self):
        """
        Initiator method.
        """
        self.logger: Logger = Logger("scraper", self.LOG_FILENAME)
        self.database: Database = Database(self.LOG_FILENAME)
        self.webdriver: Webdriver = Webdriver(self.LOG_FILENAME)
        