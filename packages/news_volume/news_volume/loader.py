import pandas as pd
import sqlite3


class NewsLoader:

    def __call__(self):

        with sqlite3.connect('../databases/news.db') as con:
            daily_news_volume = pd.read_sql_query("SELECT * FROM minas7",
                                                  con)
        return daily_news_volume
