from scraper import Scraper


class Zero(Scraper):
    start_url = "https://gauchazh.clicrbs.com.br/politica/ultimas-noticias/"
    next_xpath = "descendant-or-self::button[@class='btn-show-more']"
    row_type = "div"
    row_class = "article-card__summary"
    title_xpath = "h2"
    date_xpath = "*[class='m-crd-pt__publish-date']"
    n_last = 50
    n_next = 10
    log_file = "zero"
    db_name = "news.db"
    db_table = "zero"

    def get_row_xpath(self):
        return f"//{self.row_type}[@class='{self.row_class}' and position()>last()-{self.n_last}]"

    @staticmethod
    def get_date(date):
        lst = date.split()
        day = lst[0]
        time = lst[2]
        hm = time.split("h")
        h = hm[0]
        h = h if len(h) == 2 else f"0{h}"
        m = hm[1].split("min")[0]
        m = m if len(m) == 2 else f"0{m}"
        return f"{day[6:]}-{day[3:5]}-{day[:2]} {h}:{m}:00"


if __name__ == "__main__":
    c = Zero()
    c.run()
    del c
