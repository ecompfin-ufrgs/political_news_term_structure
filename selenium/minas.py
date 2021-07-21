import os
from   scraper import Scraper



class Minas(Scraper):
    @staticmethod
    def get_date(date):
        lst  = date.split()
        day  = lst[2]
        time = lst[0]
        day  = f"{day[6:]}-{day[3:5]}-{day[:2]}"
        time = f"{time}:00"
        return f"{day} {time}"


if __name__ == "__main__":
    os.system("rm minas.log")
    c = Minas(
        start_url   = "https://www.em.com.br/politica/",
        next_xpath  = "//*[@id='em-read-more']",
        row_xpath   = "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]",
        title_xpath = ".//a[@class='txt-gray']",
        date_xpath  = ".//small",
        n_pages     = 2000,
        n_last      = 200)#,
        #db_name     = "test.db",
        #db_table    = "minas",
        #log_file    = "test.log")
    c.run()
    del c