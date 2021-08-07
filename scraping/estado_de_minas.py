

import selenium

import js_scraper


class EstaddoDeMinasScraper(js_scraper.JSScraper):
    
    NAME = "estado_de_minas"
    START_URL = "https://www.em.com.br/politica/"
    SELECTORS = {
        "next_page": (
            selenium.webdriver.common.by.By.XPATH,
            "//*[@id='em-read-more']"
            ),
        "article": (
            selenium.webdriver.common.by.By.XPATH,
            "//div{self.row_type}[@class='news-box free pb-10 mb-20' and position()>last()-200]"
            ),
        "article_datetime": "small",
        "article_title": "a[class='txt-gray']",
        "article_link": "href"
        }
    