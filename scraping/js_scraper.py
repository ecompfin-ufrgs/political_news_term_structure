

import bs4

import base_scraper


class DateError(Exception):
    def __init__(self,
        msg : str):
    
        self.msg = msg


class JSScraper(base_scraper.BaseScraper):
    
    @property
    def NAME(self): pass
    @property
    def N_LAST_ARTICLES(self): pass
    @property
    def SELECTORS(self): pass
    @property
    def LOG_FILENAME(self): pass
    @property
    def START_URL(self): pass
    N_MAX_LOAD = 50
    N_MAX_CLICK = 10
    
    def __init__(self):
        
        super().__init__()
        
        self.previous_articles = list()
        self.last_article = None
        self.n_page = 0
        self.n_load_attempt = 1
        self.n_click_attempt = 1
        self.run = True
        
    def scrape(self):
        
        self.webdriver.get(self.START_URL)
        while self.run:
            self.n_page += 1
            self.logger.debug(f"page {self.n_page};  load attempts {self.n_load_attempt}; click attempts {self.n_click_attempt}...")
            visible_articles = self.webdriver.get_elements(self.SELECTORS["article"])
            last_visible_article = visible_articles[-1]
            if last_visible_article != self.last_article:
                self.logger.debug("new article visible, getting data...")
                self.last_article = last_visible_article
                self.n_load_attempt = 1
                self.n_click_attempt = 1
                self.loop_articles(visible_articles)
                self.click_next()
            elif self.n_load_attempt < self.N_MAX_LOAD:
                self.n_load_attempt += 1
                self.logger.warning("no new article visible")
            elif self.n_click_attempt < self.N_MAX_CLICK:
                self.click_next()
            else:
                self.logger.warning("maximum number of load and click attempts reached, finishing scrape...")
                break
            try:
                self.webdriver.click_next()
                self.n_click_attempt = 1
                self.logger.debug("clicked")
            except:
                self.n_click_attempt += 1
                self.n_load_attempt = 1
                self.logger.warning("unable to click")
                
    def click_next(self):
        
        try:
            self.webdriver.click_element(
                *self.SELECTORS["next_page"],
                sleep_time=0.2)
            self.n_click_attempt = 1
            self.n_load_attempt = 1
            self.webdriver.debug("clicked")
        except:
            self.n_click_attempt += 1
            self.n_load_attempt = 1
            self.logger.warning("unable to click")
                    
    def loop_articles(self, visible_articles : list):
        
        self.previous_articles = self.previous_articles[-self.N_LAST_ARTICLES:]
        for v_article in visible_articles:
            if v_article in self.previous_articles:
                self.logger.debug("article previously visible")
            else:
                self.previous_articles.append(v_article)
                self.get_info(v_article)
        self.database.commit()
                
    def get_info(self, v_article):
        
        soup = bs4.BeautifulSoup(v_article.get_attribute('innerHTML'), "html.parser")
        date = soup.select(self.SELECTORS["article_datetime"])[0].text
        title = soup.select(self.SELECTORS["article_title"])[0].text
        link = soup.select(self.SELECTORS["article_link"])
        try:
            date = self.get_date(date)
            values = (date, title, link)
            self.database.execute(self.database.INSERT_ARTICLE, values)
            self.logger.debug("article data found and inserted into database")
        except DateError as msg:
            self.logger.warning(f"article date not available: {msg}")
    
    @staticmethod
    def get_date(date : str):
        pass
