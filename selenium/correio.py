import logging
from   selenium                          import webdriver
from   selenium.webdriver.chrome.options import Options
from   selenium.webdriver.common.by      import By
from   selenium.webdriver.support.ui     import WebDriverWait
from   selenium.webdriver.support        import expected_conditions as EC
from   selenium.webdriver.common.keys    import Keys
import sqlite3
import time

def main():
    log_filename = "log.txt"
    log_format   = "%(asctime)s:%(levelname)s:%(message)s"

    logging.basicConfig(
        filename = "log.txt",
        level    = 0,
        filemode = "w",
        format   = log_format)

    DROP_TABLE = """
        DROP TABLE IF EXISTS correio;
        """

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS correio (
        id    INT AUTO INCREMENT PRIMARY KEY,
        date  DATETIME,
        title VARCHAR(255),
        link  VARCHAR(255)
        );
        """
        
    INSERT_DATA = """
        INSERT INTO correio (date, title)
        VALUES (?, ?);
        """

    a          = "-" * 50

    next_path  = "//*[@id='em-read-more']"
    row_path   = "//article"
    title_path = ".//h2"
    date_path  = ".//small"

    driver_path    = "/Users/bernardopaulsen/chromedriver"
    driver_options = Options()
    driver_options.add_argument("--headless")

    def get_date(date):
        lst  = date.split()
        day  = lst[2]
        time = lst[3]
        day = day[6:] + "-" + day[3:5] + "-" + day[:2]
        time = time + ":00"
        return day + " " + time

    with sqlite3.connect("news.db") as conn:
        logging.debug("SQLITE3 connect")
        conn.execute(DROP_TABLE)
        logging.debug("")
        conn.execute(CREATE_TABLE)
        with webdriver.Chrome(driver_path, options=driver_options) as driver:
            driver.get("https://www.correiobraziliense.com.br/politica")
            all_elements = []
            for i in range(2000):
                new_elements = driver.find_elements(By.XPATH, row_path)
                for element in new_elements:
                    if element not in all_elements:
                        all_elements.append(element)
                        try:
                            title = element.find_element(By.XPATH, title_path).text
                            date  = element.find_element(By.XPATH, date_path).text
                            if date:
                                    date   = get_date(date)
                                    values = (date, title)
                                    conn.execute(INSERT_DATA, values)
                                    conn.commit()
                        except:
                            pass
                try:
                    find     = (By.XPATH, next_path)
                    presence = EC.presence_of_element_located(find)
                    next     = WebDriverWait(driver, 10).until(presence)
                    enter    = "webdriver" + Keys.ENTER
                    next.send_keys(enter)
                    time.sleep(.5)
                except:
                    break

if "__name__" == __main__:
    main()
