import datetime as dt

import pandas as pd
from workalendar.america.brazil import BrazilSaoPauloCity


def get_trading_day(datetime):
    sp = BrazilSaoPauloCity()
    if datetime.hour >= 18:
        datetime += dt.timedelta(days=1)
    return sp.find_following_working_day(datetime)


class NewsProcessor:

    def __init__(self,
                 news_df: pd.DataFrame
                 ) -> None:
        self.news_df = news_df

    def __call__(self,
                 ) -> pd.Series:
        self.news_df['date'] = self.news_df['date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.news_df['trading'] = self.news_df['date'].apply(get_trading_day)
        group_df = self.news_df.groupby('trading').count()
        return group_df['title']
