from abc       import ABC, abstractmethod
from database  import Database
from logger    import Logger
from webdriver import Webdriver

class Scraper(ABC):
    def __init__(
        self,
        start_url   : str,
        next_xpath  : str,
        row_xpath   : str,
        title_xpath : str,
        date_xpath  : str,
        n_pages     : int = 2000,
        n_last      : int = 50,
        log_name    : str = "scraper",
        log_file    : str = "log.log",
        db_name     : str = "test.db",
        db_table    : str = "test"):
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
        del self.database
        del self.webdriver

    def run(self):
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
        self.logger.debug(f"looping through last {2*self.n_last} elements")
        for element in new_elements[-self.n_last:]:
            if element not in self.elements[-2*self.n_last:]:
                self.elements.append(element)
                self.get_info(element)

    def get_info(self,
        element):
        try:
            title = self.webdriver.get_inner(self.title_xpath, element).text
            date  = self.webdriver.get_inner(self.date_xpath, element).text
            date = self.get_date(date)
            self.database.insert(date, title)
        except:
            self.logger.warning("inner elements not found")

    @staticmethod
    @abstractmethod
    def get_date(self):
        pass

if __name__ == "__main__":
    s = Scraper()
    del s