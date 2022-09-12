import pandas as pd

from .loader import NewsLoader
from .processor import NewsProcessor


class NewsManager:

    def __init__(self,
                 db_path: str,
                 table: str
                 ) -> None:
        self.db_path = db_path
        self.table = table

    def __call__(self
                 ) -> pd.Series:
        news_volume_df = NewsLoader(db_path=self.db_path,
                                    table=self.table)()
        news_volume_series = NewsProcessor(news_df=news_volume_df)()
        return news_volume_series
