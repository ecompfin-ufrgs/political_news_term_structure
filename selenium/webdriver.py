"""
Title       : Webdriver
Description : Defines class Webdriver, which uses selenium to connect to, navigate and collect data from the internet.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
from   logger                               import Logger
import os
from   selenium                             import webdriver
from   selenium.webdriver.firefox.options   import Options
from   selenium.webdriver.common.by         import By
from   selenium.webdriver.support.ui        import WebDriverWait
from   selenium.webdriver.support           import expected_conditions as EC
from   selenium.webdriver.common.keys       import Keys
from   selenium.webdriver.remote.webelement import WebElement
import time

#import line_profiler
#import atexit
#profile = line_profiler.LineProfiler()
#atexit.register(profile.print_stats)

class Webdriver:
    """
    Class which uses selenium to connect to, navigate and collect data from the internet.
    
    :param log_file: Log file name, defaults to "log.log"
    :type log_file: str, optional
    """
    #path     = "./chromedriver"
    #path     = "/usr/lib/chromium-browser/chromedriver"
    path     = "/usr/bin/geckodriver"
    options  = ["--headless"]#,
    #    "start-maximized",
    #    "disable-infobars",
    #    "--disable-extensions",
    #    "--no-sandbox",
    #    "--disable-application-cache",
    #    "--disable-gpu",
    #    "--disable-dev-shm-usage"]
    log_name = "webdriver"
    def __init__(self,
        log_file : str = "log"):
        """
        Contructor method.
        """
        self.logger = Logger(
            self.log_name,
            log_file)
        self.driver = self.config()

    def __del__(self):
        """
        Destructor method. Closes webdriver.
        """
        self.driver.quit()
        self.logger.debug("connection closed")

    def config(self) -> webdriver.Chrome:
        """
        Configures Chrome webdriver.
        """
        #driver_profile = webdriver.FirefoxProfile()
        #driver_profile.set_preference("permissions.default.image", 2)
        #driver_profile.set_preference("browser.cache.disk.enable", False)
        #driver_profile.set_preference("browser.cache.memory.enable", False)
        #driver_profile.set_preference("browser.cache.offline.enable", False)
        #driver_profile.set_preference("network.http.use-cache", False) 
        driver_options = Options()
        for option in self.options:
            driver_options.add_argument(option)
        self.logger.debug("opening connection...")
        driver = webdriver.Firefox(executable_path=self.path,
            service_log_path=os.path.devnull,
            options=driver_options)#,
        #    firefox_profile=driver_profile)
        self.logger.debug("connection open")
        return driver

    def get(self,
        url : str):
        """
        Gets url.

        :param url: Url to connect to in webdriver
        :type url: str
        """
        self.logger.debug(f"getting page {url}...")
        self.driver.get(url)
        self.logger.debug(f"page received")
    
    def get_elements(self,
        xpath : str) -> list:
        """
        Gets all elements given xpath expression.

        :param xpath: Xpath expression for elements
        :type xpath: str

        :return: Elements which match xpath expression,
        :rtype: list
        """
        self.logger.debug("findind elements...")
        elements = self.driver.find_elements(By.XPATH, xpath)
        self.logger.debug(f"{len(elements)} elements found")
        return elements

    def get_inner(self,
        xpath   : str,
        element : WebElement) -> WebElement:
        """
        Gets element which is inside given element.

        :param xpath: Xpath expression for element
        :type xpath: str
        :param element: Element from which to search for inner element.
        :type element: WebElement

        :return: Inner element
        :rtype: WebElement
        """
        inner = element.find_element(By.XPATH, xpath)
        return inner

    def next_page(self,
        xpath : str):
        """
        Clicks next page element.

        :param xpath: Xpath expression for next page element
        :type xpath: str
        """
        find     = (By.XPATH, xpath)
        self.logger.debug("clicking next page")
        presence = EC.presence_of_element_located(find)
        next     = WebDriverWait(self.driver, 10).until(presence)
        enter    = "webdriver" + Keys.ENTER
        next.send_keys(enter)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.debug("next page clicked")
        time.sleep(.2)



if __name__ == "__main__":
    wd = Webdriver()
    del wd
