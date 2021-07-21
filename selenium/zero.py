import os
from   scraper import Scraper


class Zero(Scraper):
    def __init__(self,
        start_url    : str = "https://gauchazh.clicrbs.com.br/politica/ultimas-noticias/",
        next_xpath   : str = "//button[@class='btn-show-more']",
        row_xpath    : str = "//div[@class='card article-card article']",
        title_xpath  : str = ".//h2",#[@class='m-crd-pt__headline']",
        date_xpath   : str = ".//time",
        n_pages      : int = 5,
        n_last_pages : int = 50,
        db_name      : str = "news.db",
        db_table     : str = "zero",
        log_file     : str = "zero.log"):
        super().__init__(
            log_file = log_file,
            db_name  = db_name,
            db_table = db_table)
        self.start_url    = start_url
        self.next_xpath   = next_xpath
        self.row_xpath    = row_xpath
        self.title_xpath  = title_xpath
        self.date_xpath   = date_xpath
        self.n_pages      = n_pages
        self.n_last_pages = n_last_pages
        self.elements     = []

    def run(self):
        self.webdriver.get(self.start_url)
        for i in range(self.n_pages):
            self.logger.debug(f"page {i} - finding elements")
            new_elements = self.webdriver.get_elements(self.row_xpath)
            self.logger.debug("looping through elements")
            for element in new_elements[-self.n_last_pages:]:
                if element not in self.elements:
                    self.elements.append(element)
                    try:
                        title = self.webdriver.get_inner(self.title_xpath, element).text
                        date  = self.webdriver.get_inner(self.date_xpath, element).text
                        date = self.get_date(date)
                        self.database.insert(date, title)
                    except:
                        self.logger.warning("inner elements not found")
            try:
                self.webdriver.next_page(self.next_xpath)
            except:
                self.logger.warning("no next page")
                break

    @staticmethod
    def get_date(date):
        lst  = date.split()
        day  = lst[2]
        time = lst[0]
        day = day[6:] + "-" + day[3:5] + "-" + day[:2]
        time = time + ":00"
        return day + " " + time

if __name__ == "__main__":
    os.system("rm zero.log")
    c = Zero()
    c.run()
    del c