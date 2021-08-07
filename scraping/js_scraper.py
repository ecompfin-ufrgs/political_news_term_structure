

import base_scraper


class JSScraper(base_scraper.BaseScraper):
    
    @property
    def LOG_FILENAME(self): pass
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        self.webdriver.get(self.START_URL)
        