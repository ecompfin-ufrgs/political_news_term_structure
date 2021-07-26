import os
from scraper import Scraper


class Correio(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Correio Braziliense website.
    """
    start_url   = "https://www.correiobraziliense.com.br/politica"
    next_xpath  = "//*[@id='em-read-more']"
    row_type    = "article"
    row_class   = ""
    title_xpath = "h2"
    date_xpath  = "small"
    n_last      = 50
    n_next      = 10
    log_file    = "correio2"
    db_name     = "news.db"
    db_table    = "correio2"
    
    def get_row_xpath(self):
        return f"descendant-or-self::{self.row_type}[position()>last()-{self.n_last}]"
    
    @staticmethod
    def get_date(date):
        """
        Gets date string and formats it to DATETIME data type (SQLite3).

        :param date: Date string
        :type date: str

        :return: Formatted date
        :rtype: str
        """
        lst  = date.split()
        day  = lst[2]
        time = lst[3]
        return f"{day[6:]}-{day[3:5]}-{day[:2]} {time}:00"

if __name__ == "__main__":
    os.system("rm correio.log")
    c = Correio()
    c.run()
    del c