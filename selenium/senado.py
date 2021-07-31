from   bs4      import BeautifulSoup
from   database import Database
from   logger   import Logger
import os
from   webdriver import Webdriver

class Senado():
    start_url   = "https://www12.senado.leg.br/noticias/ultimas/"
    row_xpath   = "descendant-or-self::div[@class='clearfix']"
    date_css    = "span[class='text-muted milli']"
    title_css   = "a"
    n_pages_max = 1700
    log_file    = "senado"
    
    def __init__(self):
        self.logger    = Logger(name="senado",file=self.log_file)
        self.database  = Database(name="news.db",table="senado",log_file=self.log_file)
        self.webdriver = Webdriver(log_file=self.log_file)
        self.n_page    = 0
        self.elements  = []
        
    def run(self):
        while self.n_page < self.n_pages_max:
            if not self.n_page % 100:
                self.webdriver.driver.close()
                self.webdriver.config()
            self.n_page += 1
            url          = f"{self.start_url}{self.n_page}"
            self.webdriver.get(url)
            self.elements = self.webdriver.get_elements(self.row_xpath)
            self.loop_elements()
            self.database.commit()
    def loop_elements(self):
        for element in self.elements:
            soup  = BeautifulSoup(element.get_attribute('innerHTML'), "html.parser")
            date  = soup.select(self.date_css)[0].text
            title = soup.select(self.title_css)[0].text
            date  = date.strip()
            title = title.strip()
            title = title.replace("\n", " ")
            date  = self.get_date(date)
            self.database.insert(date, title)
    
    @staticmethod
    def get_date(date):
        date = f"{date[6:10]}-{date[3:5]}-{date[0:2]} {date[13:15]}:{date[16:18]}:00"
        return date
            
if __name__ =="__main__":
    s = Senado()
    s.run()
    del s