"""
Title       : Minas 
Description : Defines class Minas, child of Scraper, which scrapes the political section of Estado de Minas website.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
import os
from   scraper import Scraper

import line_profiler
import atexit
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

class Minas(Scraper):
    """
    Class, child of Scraper, which scrapes the political section of Estado de Minas website.
    """
    start_url   = "https://www.em.com.br/politica/"
    next_xpath  = "//*[@id='em-read-more']"
    row_xpath   = "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]"
    title_xpath = ".//a[@class='txt-gray']"
    date_xpath  = ".//small"
    n_last      = 200
    log_file    = "test"
    db_name     = "test.db"
    db_table    = "minas"
    
    @staticmethod
    @profile
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