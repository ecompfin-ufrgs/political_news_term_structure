

import database
import logger
import webdriver

class BaseScraper:
    def __init__(self,
        log_filename : str,
        db_tablename : str):
            
        self.logger = logger.Logger("scraper", log_filename)
        self.database = database.Database(log_filename)
        self.webdriver = webdriver.Webdriver(log_filename)