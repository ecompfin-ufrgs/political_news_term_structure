from   bs4      import BeautifulSoup
from   database import Database
from   logger   import Logger
import os
from   webdriver import Webdriver

class Senado:
    start_url   = "https://www12.senado.leg.br/noticias/ultimas/"
    row_xpath   = "div[@class='clearfix']"
    date_css    = "a"
    title_css   = "span[class='text-muted milli']"
    n_pages_max = 1700
    log_file    = "senado"
    
    def __init__(self,
        log_file : str,
        db_name  : str,
        db_table : str):
        self.logger    = Logger(name="senado",file=self.log_file)
        self.database  = Database(name="test.db",table="senado",log_file=self.log_file)
        self.webdriver = Webdriver(log_file=self.log_file)
        self.n_page    = 0
        self.elements  = []
        
    def run(self):
        while self.n_page < self.n_pages_max:
            self.n_page += 1
            url          = f"{self.start_url}{self.n_page}"
            self.webdriver.get(url)
            self.elements = self.webdriver.get_elements(self.row_xpath)
            self.loop_elements()
            
    def loop_elements(self):
        for element in self.elements:
            soup  = BeautifulSoup(element.get_attribute('innerHTML'), "html.parser")
            date  = soup.select(self.date_css)[0].text
            title = soup.select(self.title_css)[0].text
            date  = self.get_date(date)
            self.database.insert(date, title)
    
    @staticmethod
    def get_date(date):
        return date
            
    