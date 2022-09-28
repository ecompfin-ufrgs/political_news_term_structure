from arch import arch_model
import pandas as pd


class GARCH:

    def __call__(self,
                 series: pd.Series
                 ) -> pd.Series:
        am = arch_model(series.values)
        res = am.fit(update_freq=5, disp=False)
        return pd.Series(data=res.conditional_volatility, index=series.index)
