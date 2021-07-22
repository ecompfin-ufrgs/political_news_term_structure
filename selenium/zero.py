import os
from   scraper import Scraper


class Minas(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Estado de Minas website.

    :param start_ulr: Main webpage from which to start scrapping, defaults to "https://www.em.com.br/politica/"
    :type  start_url: str, optional
    :param next_xpath: Xpath expression for next page element, defaults to "//*[@id='em-read-more']"
    :type  next_xpath: str, optional
    :param row_xpath: Xpath expression for news elements, defaults to "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]"
    :type  row_xpath: str, optional
    :param title_xpath: Xpath expression for title element inside news element, defaults to ".//a[@class='txt-gray']"
    :type  title_xpath: str, optional
    :param date_xpath: Xpath expression for data element inside news element, defaults to ".//small"
    :type  date_xpath: str, optional
    :param n_pages: Number of pages to scrap, defaults to 2000
    :type  n_pages: int, optional
    :param n_last: Number of (last) news elements to inspect when looking for previously unscrapped news after next page click, defaults to 200
    :type  n_last: int, optional
    :param log_name: Logger name, defaults to "sraper"
    :type  log_name: str, optional
    :param log_file: Log file name, defaults to "zero.log"
    :type  log_file: str, optional
    :param db_name: Database file name, defaults to "news.db"
    :type  db_name: str, optional
    :param db_table: Database table name, defaults to zero
    :type  db_table: str, optional
    """
    def __init__(self,
        start_url   : str = "https://www.em.com.br/politica/",
        next_xpath  : str = "//*[@id='em-read-more']",
        row_xpath   : str = "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]",
        title_xpath : str = ".//a[@class='txt-gray']",
        date_xpath  : str = ".//small",
        n_pages     : int = 2000,
        n_last      : int = 200,

        log_file    : str = "minas.log",
        db_name     : str = "news.db",
        db_table    : str = "minas"):
        super().__init__(
            start_url   = start_url,
            next_xpath  = next_xpath,
            row_xpath   = row_xpath,
            title_xpath = title_xpath,
            date_xpath  = date_xpath,
            n_pages     = n_pages,
            n_last      = n_last,
            log_name    = log_name,
            log_file    = log_file,
            db_name     = db_name,
            db_table    = db_table)



class Zero(Scraper):
    def __init__(self,
        start_url    : str = "https://gauchazh.clicrbs.com.br/politica/ultimas-noticias/",
        next_xpath   : str = "//button[@class='btn-show-more']",
        row_xpath    : str = "//div[@class='card article-card article' and position()>last()-200]",
        title_xpath  : str = ".//h2",#[@class='m-crd-pt__headline']",
        date_xpath   : str = ".//time",
        n_pages      : int = 5,
        n_last       : int = 200,
        db_name      : str = "news.db",
        db_table     : str = "zero",
        log_file     : str = "zero.log"):
        super().__init__(
            start_url   = start_url,
            next_xpath  = next_xpath,
            row_xpath   = row_xpath,
            title_xpath = title_xpath,
            date_xpath  = date_xpath,
            n_pages     = n_pages,
            n_last      = n_last,
            log_file    = log_file,
            db_name     = db_name,
            db_table    = db_table)

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