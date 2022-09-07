from dataclasses import dataclass
import datetime as dt

import pandas as pd

from .future_processor import FutureProcessor


@dataclass
class TermStructure:

    dataframe_name: str

    def __post_init__(self):
        self.spot = self._init_spot()
        self.future = self._init_future(spot_series=self.spot)

    @staticmethod
    def _init_spot(
                   ) -> pd.Series:
        # spot_df = dataframe.iloc[:, :1].dropna()
        # spot_s = spot_df[spot_df.columns[0]]
        # spot_s = spot_s.drop(spot_s[spot_s == '-'].index)
        spot_df = pd.read_csv('di_anual.csv', sep=';')[:-1]
        spot_df.index = spot_df['Date'].apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))
        spot_s = spot_df[spot_df.columns[-1]]
        spot_s = spot_s.apply(lambda x: float(x))
        return spot_s

    def _init_future(self,
                     spot_series: pd.Series
                     ) -> pd.DataFrame:
        dataframe = pd.read_excel(self.dataframe_name, header=3, index_col=0)
        future_df = dataframe.iloc[:, 1:]
        future_df = future_df.loc[spot_series.index, :]
        future_df = FutureProcessor()(dataframe=future_df)
        return future_df





