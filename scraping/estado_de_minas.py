
import bs4
import selenium

import js_scraper


class EstaddoDeMinasScraper(js_scraper.JSScraper):
    
    NAME = "Estado de Minas"
    SHORT_NAME = "minas"
    N_LAST_ARTICLES = 200
    START_URL = "https://www.em.com.br/politica/"
    SELECTORS = {
        "next_page": (
            selenium.webdriver.common.by.By.XPATH,
            "//*[@id='em-read-more']"
            ),
        "article": (
            selenium.webdriver.common.by.By.XPATH,
            "//div[@class='news-box free pb-10 mb-20' and position()>last()-200]"
            ),
        "article_datetime": "small",
        "article_title_link": ".txt-gray",
        }
    LOG_FILENAME = "estado_de_minas"
       
    @staticmethod 
    def get_date(date):
        try:
            lst  = date.split()
            day  = lst[2]
            time = lst[0]
            return f"{day[6:]}-{day[3:5]}-{day[:2]} {time}:00"
        except:
            raise js_scraper.DateError("date does not contain day data")
            
    def get_info(self, v_article):
        
        try:
            soup = bs4.BeautifulSoup(v_article.get_attribute('innerHTML'), "html.parser")
            date = soup.select(self.SELECTORS["article_datetime"])[0].text
            date = self.get_date(date)
            title_link = soup.select(self.SELECTORS["article_title_link"])[0]
            title = title_link.text
            link = title_link['href']
            values = (self.ID, date, title, link)
            self.database.insert_article(values)
        except:
            self.logger.warning("article data not available")
    
if __name__ == "__main__":
    em = EstaddoDeMinasScraper()
    em.scrape()