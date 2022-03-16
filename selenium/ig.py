"""
Title       : Minas 
Description : Defines class Minas, child of Scraper, which scrapes the political section of Estado de Minas website.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
from scraper import Scraper


# import line_profiler
# import atexit
# profile = line_profiler.LineProfiler()
# atexit.register(profile.print_stats)

class Ig(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Estado de Minas website.
    """
    start_url = "https://ultimosegundo.ig.com.br/politica/"
    next_xpath = "//a[@class='proxima']"
    row_type = "div"
    row_class = "empilhaImg-text"
    title_xpath = "h2"
    date_xpath = "cite"
    n_last = 100
    n_next = 10
    n_load = 50
    n_error = 20
    log_file = "ig"
    db_name = "news.db"
    db_table = "ig"

    def get_row_xpath(self):
        return f"descendant-or-self::{self.row_type}[@class='{self.row_class}' and position()>last()-{self.n_last}]"

    @staticmethod
    def get_date(
            date: str):
        """
        Gets date string and formats it to DATETIME data type (SQLite3).

        :param date: Date string
        :type date: str

        :return: Formatted date
        :rtype: str
        """
        return f"{date[14:]}-{date[11:13]}-{date[8:10]} {date[:2]}:{date[3:5]}:00"


if __name__ == "__main__":
    c = Ig()
    c.run()
