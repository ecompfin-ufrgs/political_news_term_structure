import os
from   scraper import Scraper

class Zero(Scraper):
    def __init__(self,
        start_url    : str = "https://gauchazh.clicrbs.com.br/politica/ultimas-noticias/",
        next_xpath   : str = "//button[@class='btn-show-more']",
        row_xpath    : str = "//div[@class='card article-card article' and position()>last()-200]",
        title_xpath  : str = ".//h2",#[@class='m-crd-pt__headline']",
        date_xpath   : str = ".//*[@class='m-crd-pt__publish-date']",
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
        day  = lst[0]
        time = lst[2]
        day  = f"{day[6:]}-{day[3:5]}-{day[:2]}"
        hm   = time.split("h")
        h    = hm[0]
        h    = h if len(h) == 2 else f"0{h}"
        m    = hm[1].split("min")[0]
        m    = m if len(m) == 2 else f"0{m}"
        time = f"{h}:{m}:00"
        return f"{day} {time}"


if __name__ == "__main__":
    os.system("rm zero.log")
    c = Zero()
    c.run()
    del c