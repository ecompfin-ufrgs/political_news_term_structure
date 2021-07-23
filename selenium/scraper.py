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
    """
    def __init__(self):
        """
        Constructor method. Initiates Logger, Database and Webdriver.
        """
        self.logger      = Logger(self.log_name, self.log_file)
        self.database    = Database(self.db_name, self.db_table, log_file = self.log_file)
        self.webdriver   = Webdriver(log_file = self.log_file)
        self.elements    = []

    def __del__(self):
        """
        Destructor method. Deletes Database and Logger.
        """
        del self.database
        del self.webdriver

    @property
    @abstractmethod
    def start_url(self):
        pass
    @property
    @abstractmethod
    def next_xpath(self):
        pass
    @property
    @abstractmethod
    def row_xpath(self):
        pass
    @property
    @abstractmethod
    def title_xpath(self):
        pass
    @property
    @abstractmethod
    def date_xpath(self):
        pass
    @property
    @abstractmethod
    def n_pages(self):
        pass
    @property
    @abstractmethod
    def n_last(self):
        pass
    @property
    @abstractmethod
    def log_name(self):
        pass
    @property
    @abstractmethod
    def log_file(self):
        pass
    @property
    @abstractmethod
    def db_name(self):
        pass
    @property
    @abstractmethod
    def db_table(self):
        pass

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
        del self

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
        self.database.commit()

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