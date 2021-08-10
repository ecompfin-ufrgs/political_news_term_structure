

import os
import time

import selenium
from selenium import webdriver
from   selenium.webdriver.support import expected_conditions

import logger


class Webdriver:
    path = "/usr/lib/chromium-browser/chromedriver"
    option  = "--headless"
    
    def __init__(self,
        log_filename : str):
        
        self.logger = logger.Logger("webdriver", log_filename)
        
        self.driver = self.get_driver()
        
    def __del__(self):
        
        self.driver.quit()
        
    def get_driver(self):
        
        driver_options = selenium.webdriver.chrome.options.Options()
        driver_options.add_argument(self.option)
        self.logger.debug("opening connection...")
        driver = webdriver.Chrome(
            executable_path=self.path,
            service_log_path=os.path.devnull,
            options=driver_options
            )
        self.logger.debug("connection open")
        return driver
        
    def get(self,
        url : str):
        
        self.logger.debug(f"getting page {url}...")
        self.driver.get(url)
        self.logger.debug("page received")
        
    def click_element(self,
        selector : selenium.webdriver.common.by.By,
        path : str,
        sleep_time : float):
        
        wait = selenium.webdriver.support.ui.WebDriverWait(self.driver, 10)
        c_values = (selector, path)
        condition = expected_conditions.visibility_of_element_located(c_values)
        button = wait.until(condition)
        enter = "webdriver" + selenium.webdriver.common.keys.Keys.ENTER
        self.logger.debug(f"{path}: clicking...")
        button.send_keys(enter)
        self.logger.debug(f"{path}: clicked")
        time.sleep(sleep_time)
        
    def get_elements(self,
        selector_and_path : tuple):
        
        path = selector_and_path[1]
        self.logger.debug(f"{path}: findind elements...")
        elements = self.driver.find_elements(*selector_and_path)
        self.logger.debug(f"{path}: {len(elements)} elements found")
        return elements