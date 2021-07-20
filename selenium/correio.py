from scraper import Scraper


class Correio(Scraper):
    def __init__(self,
        start_url   : str = "https://www.correiobraziliense.com.br/politica",
        next_xpath  : str = "//*[@id='em-read-more']",
        row_xpath   : str = "//article",
        title_xpath : str = ".//h2",
        date_xpath  : str = ".//small",
        n_pages     : int = 1000,
        n_last      : int = 50,
        db_name     : str = "news.db",
        db_table    : str = "correio"):
        super().__init__(
            db_name  = db_name,
            db_table = db_table)
        self.start_url    = start_url
        self.next_xpath   = next_xpath
        self.row_xpath    = row_xpath
        self.title_xpath  = title_xpath
        self.date_xpath   = date_xpath
        self.n_pages      = n_pages
        self.n_last       = n_last
        self.elements     = []

    def run(self):
        self.webdriver.get(self.start_url)
        for i in range(self.n_pages):
            self.logger.debug(f"page {i} - finding elements")
            new_elements = self.webdriver.get_elements(self.row_xpath)
            self.logger.debug("looping through elements")
            for element in new_elements[-self.n_last:]:
                if element not in self.elements[-2*self.n_last:]:
                    self.elements.append(element)
                    try:
                        title = self.webdriver.get_inner(self.title_xpath, element).text
                        date  = self.webdriver.get_inner(self.date_xpath, element).text
                        if date:
                            date = self.get_date(date)
                            self.database.insert(date, title)
                        else:
                            self.logger.warning("null date")
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
        time = lst[3]
        day = day[6:] + "-" + day[3:5] + "-" + day[:2]
        time = time + ":00"
        return day + " " + time

if __name__ == "__main__":
    c = Correio()
    c.run()
    del c