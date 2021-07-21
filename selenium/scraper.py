"""
Title       : Scraper 
Description : Defines abstract class Scraper, which scrapes news websites.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
from abc                                  import ABC, abstractmethod
from database                             import Database
from logger                               import Logger
from webdriver                            import Webdriver
from selenium.webdriver.remote.webelement import WebElement


class Scraper(ABC):
    """
    Class for scraping news websites.
    
    :param start_ulr: Main webpage from which to start scrapping
    :type  start_url: str
    :param next_xpath: Xpath expression for next page element
    :type  next_xpath: str
    :param row_xpath: Xpath expression for news elements
    :type  row_xpath: str
    :param title_xpath: Xpath expression for title element inside news element
    :type  title_xpath: str
    :param date_xpath: Xpath expression for data element inside news element
    :type  date_xpath: str
    :param n_pages: Number of pages to scrap, defaults to 2000
    :type  n_pages: int, optional
    :param n_last: Number of (last) news elements to inspect when looking for previously unscrapped news after next page click, defaults to 200
    :type  n_last: int, optional
    :param log_name: Logger name, defaults to "sraper"
    :type  log_name: str, optional
    :param log_file: Log file name, defaults to "log.log"
    :type  log_file: str, optional
    :param db_name: Database file name, defaults to "test.db"
    :type  db_name: str, optional
    :param db_table: Database table name, defaults to "test"
    :type  db_table: str, optional
    """
    def __init__(
        self,
        start_url   : str,
        next_xpath  : str,
        row_xpath   : str,
        title_xpath : str,
        date_xpath  : str,
        n_pages     : int = 2000,
        n_last      : int = 200,
        log_name    : str = "scraper",
        log_file    : str = "log.log",
        db_name     : str = "test.db",
        db_table    : str = "test"):
        """
        Constructor method. Initiates Logger, Database and Webdriver.
        """
        self.logger      = Logger(log_name, log_file)
        self.database    = Database(db_name, db_table, log_file = log_file)
        self.webdriver   = Webdriver(log_file = log_file)
        self.start_url   = start_url
        self.next_xpath  = next_xpath
        self.row_xpath   = row_xpath
        self.title_xpath = title_xpath
        self.date_xpath  = date_xpath
        self.n_pages     = n_pages
        self.n_last      = n_last
        self.elements    = []

    def __del__(self):
        """
        Destructor method. Deletes Database and Logger.
        """
        del self.database
        del self.webdriver

    def run(self):
        """
        Runs web scrapping.
        """
        self.webdriver.get(self.start_url)
        for i in range(self.n_pages):
            self.logger.debug(f"page {i} - finding elements")
            new_elements = self.webdriver.get_elements(self.row_xpath)
            self.loop_elements(new_elements)
            try:
                self.webdriver.next_page(self.next_xpath)
            except:
                self.logger.warning("no next page")
                break

    def loop_elements(self,
        new_elements : list):
        """
        Loops through elements, finds new article elements, gets their information and inserts the information in the database.
        
        :param new_elements: List of new article elements which will be looped by in search of article elements not yet found.
        :type new_elements: list
        """
        self.logger.debug(f"looping through last {self.n_last} elements")
        for element in new_elements[-self.n_last:]:
            if element not in self.elements[-self.n_last:]:
                self.elements.append(element)
                self.get_info(element)

    def get_info(self,
        element : WebElement):
        """
        Extacts information from elements and inserts it in the database.

        :param element: Article element containing information
        :type element: selenium.webdriver.remote.webelement.WebElement
        """
        try:
            title = self.webdriver.get_inner(self.title_xpath, element).text
            date  = self.webdriver.get_inner(self.date_xpath, element).text
            date = self.get_date(date)
            self.database.insert(date, title)
        except:
            self.logger.warning("inner elements not found")

    @staticmethod
    @abstractmethod
    def get_date(
        date : str):
        """
        Abstract method. Gets date string and formats it to DATETIME data type (SQLite3).

        :param date: Date string.
        :type date: str
        """
        pass

if __name__ == "__main__":
    s = Scraper()
    del s