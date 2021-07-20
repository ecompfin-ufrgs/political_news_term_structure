import logging
from   selenium                          import webdriver
from   selenium.webdriver.chrome.options import Options
from   selenium.webdriver.common.by      import By
from   selenium.webdriver.support.ui     import WebDriverWait
from   selenium.webdriver.support        import expected_conditions as EC
from   selenium.webdriver.common.keys    import Keys
import sqlite3
import time

logging.basicConfig(level=0)

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

a          = "-" * 50

next_path  = "//*[@id='em-read-more']"
row_path   = "//div[@class='row']"
title_path = ".//a[@class='txt-gray']"
time_path  = ".//small"

driver_path    = "/Users/bernardopaulsen/chromedriver"
driver_options = Options()
driver_options.add_argument("--headless")

with sqlite3.connect("news.db") as conn:
    conn.execute(DROP_TABLE)
    conn.execute(CREATE_TABLE)
    with webdriver.Chrome(driver_path, options=driver_options) as driver:
        driver.get("https://www.em.com.br/politica/")
        #all_elements = []
        for i in range(2):
            #new_elements = driver.find_elements(By.XPATH, row_path)
            #all_elements + [element for element in new_elements if element not in all_elements]
            try:
                find     = (By.XPATH, next_path)
                presence = EC.presence_of_element_located(find)
                next     = WebDriverWait(driver, 10).until(presence)
                enter    = "webdriver" + Keys.ENTER
                next.send_keys(enter)
                time.sleep(.5)
            except:
                break
        all_elements = driver.find_elements(By.XPATH, row_path)
        for element in all_elements:
                title_link = element.find_element(By.XPATH, title_path)
                print(title_link.text)