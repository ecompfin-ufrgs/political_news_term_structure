from   logger                               import Logger
from   selenium                             import webdriver
from   selenium.webdriver.chrome.options    import Options
from   selenium.webdriver.common.by         import By
from   selenium.webdriver.support.ui        import WebDriverWait
from   selenium.webdriver.support           import expected_conditions as EC
from   selenium.webdriver.common.keys       import Keys
from   selenium.webdriver.remote.webelement import WebElement
import time


class Webdriver:
    def __init__(self,
        path     : str = "/Users/bernardopaulsen/chromedriver",
        options  : str = "--headless",
        log_name : str = "webdriver",
        log_file : str = "log.log"):
        
        self.logger = Logger(log_name, log_file)
        self.driver = self.config(path = path, options = options)

    def __del__(self):
        self.driver.close()
        self.logger.debug("connection closed")

    def config(self,
        path    : str,
        options : str) -> webdriver.Chrome:
        driver_options = Options()
        driver_options.add_argument(options)
        driver = webdriver.Chrome(path, options=driver_options)
        self.logger.debug("connection open")
        return driver

    def get(self,
        url : str):
        self.logger.debug(f"getting page {url}")
        self.driver.get(url)
        self.logger.debug(f"page received")
    
    def get_elements(self,
        xpath : str) -> list:
        elements = self.driver.find_elements(By.XPATH, xpath)
        self.logger.debug(f"{len(elements)} elements found")
        return elements

    def get_inner(self,
        xpath   : str,
        element : WebElement) -> WebElement:
        inner = element.find_element(By.XPATH, xpath)
        return inner

    def next_page(self,
        xpath : str):
        find     = (By.XPATH, xpath)
        self.logger.debug("clicking next page")
        presence = EC.presence_of_element_located(find)
        next     = WebDriverWait(self.driver, 10).until(presence)
        enter    = "webdriver" + Keys.ENTER
        next.send_keys(enter)
        self.logger.debug("next page clicked, sleeping...")
        time.sleep(.5)



if __name__ == "__main__":
    wd = Webdriver(log_name = "webdriver test")
    del wd
