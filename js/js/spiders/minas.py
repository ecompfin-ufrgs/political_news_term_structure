import scrapy
from   selenium                          import webdriver
from   selenium.webdriver.chrome.options import Options
from   selenium.webdriver.common.by      import By
from   selenium.webdriver.support.ui     import WebDriverWait
from   selenium.webdriver.support        import expected_conditions as EC
import sqlite3

class MySpider(scrapy.Spider):
    name       = "minas"

    DROP_TABLE = """
        DROP TABLE IF EXISTS minas;
        """

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS minas (
        id    INT AUTO INCREMENT PRIMARY KEY,
        date  DATETIME,
        title VARCHAR(255),
        link  VARCHAR(255)
        );
        """
    
    INSERT_DATA = """
        INSERT INTO minas (date, title, link)
        VALUES (?, ?, ?);
        """

    def __init__(self):
        super(MySpider, self).__init__()
        self.start_urls = ["https://www.em.com.br/politica/"]
        self.n          = 1
        self.conn       = sqlite3.connect("news.db")
        print("-"*50 + "SQLite connection open.")
        self.conn.execute(self.DROP_TABLE)
        self.conn.execute(self.CREATE_TABLE)
        self.driver_options = Options()
        self.driver_options.add_argument("--headless")
        self.driver     = webdriver.Chrome('/Users/bernardopaulsen/chromedriver',options=self.driver_options)
        print("-"*50 + "Webdriver open.")

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print("-"*50 + "SQLite connection closed.")
        self.driver.close()
        print("-"*50 + "Webdriver closed.")
        
    def parse(self, response):
        next_xpath = '//a[@id="em-read-more"]'
        self.driver.get(response.url)
        while True:
            print("-"*50 + f"SOURCE LENGTH: {len(self.driver.page_source)}")
            print("-"*50 + "Webdriver waiting for element.")
            next = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, next_xpath)))
            print("-"*50 + "Webdriver element found.")
            #next = self.driver.find_element_by_xpath("//a[@id='em-read-more']/a")
            try:
                print("-"*50 + "Webdriver clicking element")
                next.click()
                print("-"*50 + "Webdriver element clicked")
                # get the data and write it to scrapy items
            except:
                print("-"*50 + 'No next page.')
                break

