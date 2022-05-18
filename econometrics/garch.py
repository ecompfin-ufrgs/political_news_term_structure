import abc
from typing import Any

from arch import arch_model
import pandas as pd


class GARCH:

    @property
    def conditional_volatility(self) -> pd.Series:
        return res.conditional_volatility

    def __init__(self,
                 time_series: pd.DataFrame
                 ) -> None:
        self.res = self.estimate(time_series=time_series)

    @staticmethod
    def estimate(time_series: pd.DataFrame
                 ) -> Any:
        am = arch_model(series)
        res = am.fit()
        return res
