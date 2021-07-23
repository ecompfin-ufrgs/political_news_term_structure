"""
Title       : Minas 
Description : Defines class Minas, child of Scraper, which scrapes the political section of Estado de Minas website.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
import os
from   scraper import Scraper


class Minas(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Estado de Minas website.
    """
    start_url   : str = "https://www.em.com.br/politica/"
    next_xpath  : str = "//*[@id='em-read-more']"
    row_xpath   : str = "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]"
    title_xpath : str = ".//a[@class='txt-gray']"
    date_xpath  : str = ".//small"
    n_last      : int = 200
    log_file    : str = "minas"
    db_name     : str = "news.db"
    db_table    : str = "minas"
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
        lst  = date.split()
        day  = lst[2]
        time = lst[0]
        return f"{day[6:]}-{day[3:5]}-{day[:2]} {time}:00"


if __name__ == "__main__":
    os.system("rm minas.log")
    c = Minas()
    c.run()
    del c