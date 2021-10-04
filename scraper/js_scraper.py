import time
from typing import Dict, Tuple

from .base_scraper import BaseScraper


class JSScraper(BaseScraper):

    id: int
    NAME: str
    N_LAST_ARTICLES: int
    SELECTORS: Dict[str, Tuple[str, str]]
    LOG_FILENAME: str
    START_URL: str

    N_MAX_LOAD: int = 50
    N_MAX_CLICK: int = 10
    ID = None
    SHORT_NAME = None
    
    def __init__(self):
        
        super().__init__()
        
        self.previous_articles = list()
        self.last_article = None
        self.n_page = 0
        self.n_load_attempt = 1
        self.n_click_attempt = 1
    
    def scrape(self):
        self.config_db()
        self.webdriver.get(self.START_URL)
        while True:
            self.logger.debug(f"page {self.n_page};  load attempts {self.n_load_attempt}; click attempts {self.n_click_attempt}...")
            visible_articles = self.webdriver.get_elements(self.SELECTORS["article"])
            last_visible_article = visible_articles[-1]
            if last_visible_article != self.last_article:
                self.logger.debug("new article(s) visible, getting data...")
                self.last_article = last_visible_article
                self.n_load_attempt = 1
                self.n_click_attempt = 1
                self.loop_articles(visible_articles)
                self.click_next()
            elif self.n_load_attempt < self.N_MAX_LOAD:
                self.n_load_attempt += 1
                self.logger.warning("no new article visible")
                time.sleep(.2)
            elif self.n_click_attempt < self.N_MAX_CLICK:
                self.click_next()
            else:
                self.logger.warning("maximum number of load and click attempts reached, finishing scrape...")
                break
            
    def config_db(self):
        self.database.execute(self.database.USE_DB)
        self.id = self.database.query_website_id(self.NAME)
        self.database.delete_articles(self.ID)
                
    def click_next(self):
        
        try:
            self.webdriver.click_element(
                    *self.SELECTORS["next_page"],
                    sleep_time=0.2)
            self.n_page += 1
            self.n_click_attempt = 1
            self.n_load_attempt = 1
            self.logger.debug("clicked")
        except:
            self.n_click_attempt += 1
            self.n_load_attempt = 1
            self.logger.warning("unable to click")
                    
    def loop_articles(self, visible_articles : list):
        
        self.logger.debug("        id|date               |title                    |link                            ")
        self.logger.debug("        +-+-------------------+-------------------------+-------------------------+      ")
        self.previous_articles = self.previous_articles[-self.N_LAST_ARTICLES:]
        for v_article in visible_articles:
            if v_article not in self.previous_articles:
                self.previous_articles.append(v_article)
                self.get_info(v_article)
        self.logger.debug("        +-+-------------------+-------------------------+-------------------------+      ")
        self.database.commit()

    def get_info(self, v_article):
        pass
            
    @staticmethod
    def get_date(date : str):
        pass
