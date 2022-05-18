from typing import Any

from statsmodels.tsa.stattools import grangercausalitytests


class Granger:

    @property
    def result(self) -> dict:
        return self.res

    def __init__(self,
                 causing_series: pd.Series,
                 caused_series: pd.Series,
                 lags: int
                 ) -> None:
        self.res = self.estimate(causing_series=causing_series,
                                 caused_series=caused_series,
                                 lags=lags)

    @staticmethod
    def estimate(causing_series: pd.Series,
                 caused_series: pd.Series,
                 lags: int
                 ) -> Any:
        df = pd.DataFrame()
        df['first'] = caused_series
        df['second'] = causing_series
        res = grangercausalitytests(df, maxlag=lags)
        return res
