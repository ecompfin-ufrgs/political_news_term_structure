from scraper import Scraper


class Correio(Scraper):
    @staticmethod
    def get_date(date):
        lst  = date.split()
        day  = lst[2]
        time = lst[3]
        day = day[6:] + "-" + day[3:5] + "-" + day[:2]
        time = time + ":00"
        return day + " " + time

if __name__ == "__main__":
    c = Correio(
        start_url   = "https://www.correiobraziliense.com.br/politica",
        next_xpath  = "//*[@id='em-read-more' and position()>last()-200]",
        row_xpath   = "//article",
        title_xpath = ".//h2",
        date_xpath  = ".//small",
        n_pages     = 10,
        n_last      = 50,
        db_name     = "news.db",
        db_table    = "correio")
    c.run()
    del c