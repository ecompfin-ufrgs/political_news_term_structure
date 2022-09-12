import pandas as pd
import sqlite3


class NewsLoader:

    def __init__(self,
                 db_path: str,
                 table: str
                 ) -> None:
        self.db_path = db_path
        self.table = table

    def __call__(self):

        with sqlite3.connect(self.db_path) as con:
            daily_news_volume = pd.read_sql_query(f'SELECT * FROM {self.table}',
                                                  con)
        return daily_news_volume
