from   selenium                          import webdriver
from   selenium.webdriver.chrome.options import Options
from   selenium.webdriver.common.by      import By
from   selenium.webdriver.support.ui     import WebDriverWait
from   selenium.webdriver.support        import expected_conditions as EC
from   selenium.webdriver.common.keys    import Keys

from database import Database
from logger import Logger

class Scraper:

    def __init__(
        self,
        log_filename   : str = "log.log",
        log_level      : int = 0,
        log_filemode   : str = "w",
        log_format     : str = "%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        db_name        : str = "news.db",
        db_table       : str = "correio",
        driver_path    : str = "/Users/bernardopaulsen/chromedriver",
        driver_options : str = "--headless"):

        self.logger = Logger(
            "scraper",
            log_filename,
            log_level,
            log_filemode,
            log_format)

        self.database = Database(
            log_filename = log_filename,
            log_level    = log_level,
            log_filemode = log_filemode,
            log_format   = log_format,
            db_name      = db_name,
            db_table     = db_table)

def main():
    Scraper()

if __name__ == "__main__":
    main()