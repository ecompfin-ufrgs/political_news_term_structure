"""
Title       : Minas 
Description : Defines class Minas, child of Scraper, which scrapes the political section of Estado de Minas website.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
from   scraper import Scraper

#import line_profiler
#import atexit
#profile = line_profiler.LineProfiler()
#atexit.register(profile.print_stats)

class Minas(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Estado de Minas website.
    """
    start_url   = "https://noticias.uol.com.br/politica/"
    next_xpath  = "//button[text()='ver mais ']"
    row_type    = "div"
    row_class   = "thumbnails-item align-horizontal list col-xs-8 col-sm-12 small col-sm-24 small"
    title_xpath = "h3"
    date_xpath  = "time"
    n_last      = 100
    n_next      = 10
    log_file    = "uol"
    db_name     = "news.db"
    db_table    = "uol"
    
    def get_row_xpath(self):
        return f"descendant-or-self::{self.row_type}[@class='{self.row_class}' and position()>last()-{self.n_last}]"
    
    @staticmethod
    def get_date(
        date : str):
        """
        Gets date string and formats it to DATETIME data type (SQLite3).

        :param date: Date string
        :type date: str

        :return: Formatted date
        :rtype: str
        """
        if len(date) == 16:
            return f"{date[6:10]}-{date[3:5]}-{date[:2]} {date[11:13]}:{date[14:]}:00"
        else:
            raise NameError


if __name__ == "__main__":
    c = Minas()
    c.run()