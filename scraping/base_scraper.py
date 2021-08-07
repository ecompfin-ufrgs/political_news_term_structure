

import database
import logger
import webdriver


class BaseScraper:
    
    @property
    def LOG_FILENAME(self): pass
    
    def __init__(self):
            
        self.logger = logger.Logger("scraper", self.LOG_FILENAME)
        self.database = database.Database(self.LOG_FILENAME)
        self.webdriver = webdriver.Webdriver(self.LOG_FILENAME)
        