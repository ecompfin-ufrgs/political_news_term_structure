import datetime as dt

import pandas as pd


class SpotRate:

    def __init__(self,
                 spot_rate_path: str
                 ) -> None:
        self.spot_rate_path = spot_rate_path

    def __call__(self
                 ) -> pd.Series:
        spot_df = self._load_csv()
        spot_s = self._process_df(spot_df=spot_df)
        return spot_s

    def _load_csv(self
                  ) -> pd.DataFrame:
        return pd.read_csv(self.spot_rate_path, sep=';')[:-1]

    @staticmethod
    def _process_df(spot_df: pd.DataFrame
                    ) -> pd.Series:
        spot_df.index = spot_df['Date'].apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y').date())
        spot_s = spot_df[spot_df.columns[-1]]
        spot_s = spot_s.apply(lambda x: float(x))
        return spot_s
