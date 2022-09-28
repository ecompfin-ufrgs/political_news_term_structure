import pandas as pd
import statsmodels.api as sm


class Granger:

    def __init__(self,
                 causing: pd.Series,
                 caused: pd.Series
                 ) -> None:
        self.causing = causing
        self.caused = caused

    def __call__(self
                 ) -> dict:
        data = pd.DataFrame()
        data[0] = self.caused
        data[1] = self.causing
        res = sm.tsa.stattools.grangercausalitytests(data, maxlag=40, verbose=False)
        return res
