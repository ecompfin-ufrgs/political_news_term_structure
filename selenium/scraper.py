"""
Title       : Scraper
Description : Defines abstract class Scraper, which scrapes news websites.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
import os
import time
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement

from database import Database
from logger import Logger
from webdriver import Webdriver


class Scraper(ABC):
    """
    Class for scraping news websites.
    """
    log_name = "scraper"

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
    def row_type(self):
        pass

    @property
    @abstractmethod
    def row_class(self):
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
    def n_last(self):
        pass

    @property
    @abstractmethod
    def n_next_max(self):
        pass

    @property
    @abstractmethod
    def n_load_max(self):
        pass

    @property
    @abstractmethod
    def n_error_max(self):
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

    def __init__(self):
        """
        Constructor method. Initiates Logger, Database and Webdriver.
        """
        os.system(f"rm logs/{self.log_file}.log")
        self.logger = Logger(self.log_name, self.log_file)
        self.database = Database(self.db_name, self.db_table, log_file=self.log_file)
        self.webdriver = Webdriver(log_file=self.log_file)
        self.row_xpath = self.get_row_xpath()
        self.elements = []
        self.n_page = 1
        self.n_load = 1
        self.n_next = 1
        self.n_error = 0

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
        time.sleep(1)
        l = None
        while True:
            self.logger.debug(
                f"page {self.n_page}, {self.n_next} try to click next, {self.n_load} try to load elements")
            new_elements = self.webdriver.get_elements(self.row_xpath)
            last_element_found = new_elements[-1]
            if last_element_found != l:
                l = last_element_found
                self.loop_elements(new_elements)
                finish = self.next_page()
                if finish:
                    break
                self.n_load = 1
                self.n_next = 1
            elif self.n_load < self.n_load_max:
                time.sleep(.2)
                self.n_load += 1
            elif self.n_next < self.n_next_max:
                self.webdriver.next_page(self.next_xpath)
                self.n_load = 1
                self.n_next += 1
            else:
                self.logger.error("new elements not loading, finishing program...")
                break
        del self

    def next_page(self):
        finish = False
        try:
            self.webdriver.next_page(self.next_xpath)
            self.n_page += 1
            self.n_error = 0
        except:
            self.n_error += 1
            if self.n_error < self.n_error_max:
                self.logger.warning(f"no next page for the {self.n_error} time, trying again...")
            else:
                self.logger.error(f"no next page for the {self.n_error} time, finishing program...")
                finish = True
        return finish

    def loop_elements(self,
                      new_elements: list):
        """
        Loops through elements, finds new article elements, gets their information and inserts the information in the database.
        
        :param new_elements: List of new article elements which will be looped by in search of article elements not yet found.
        :type new_elements: list
        """
        self.logger.debug("looping through elements...")
        self.elements = self.elements[-self.n_last:]
        for element in new_elements:
            if element not in self.elements:
                self.elements.append(element)
                self.get_info(element)
        self.database.commit()

    def get_info(self,
                 element: WebElement):
        """
        Extacts information from elements and inserts it in the database.

        :param element: Article element containing information
        :type element: selenium.webdriver.remote.webelement.WebElement
        """
        try:
            soup = BeautifulSoup(element.get_attribute('innerHTML'), "html.parser")
            title = soup.select(self.title_xpath)[0].text
            date = soup.select(self.date_xpath)[0].text
            date = self.get_date(date)
            self.database.insert(date, title)
        except:
            self.logger.warning("inner elements not found")

    @abstractmethod
    def get_row_xpath(self):
        pass

    @staticmethod
    @abstractmethod
    def get_date(
            date: str):
        """
        Abstract method. Gets date string and formats it to DATETIME data type (SQLite3).

        :param date: Date string.
        :type date: str
        """
        pass
