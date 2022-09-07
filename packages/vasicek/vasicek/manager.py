import numpy as np
import pandas as pd
import tqdm

from ..market_data import TermStructure

from .estimator import VasicekEstimator
from .model import VasicekModel


class VasicekManager:

    MATURITY_ARRAY = np.array(range(1, 2000)) / 252

    def __init__(self,
                 term_structure: TermStructure
                 ) -> None:
        self.term_structure = term_structure

    def __call__(self
                 ) -> pd.DataFrame:
        df = pd.DataFrame()
        for index, spot_rate in tqdm.tqdm(self.term_structure.spot.iteritems()):
            term_s = self.term_structure.future.loc[index, :].dropna()
            future_rate = term_s.to_numpy()
            future_time = np.array(list(term_s.index))/252
            try:
                parameters = VasicekEstimator()(spot_rate=spot_rate,
                                                term_rate=future_rate,
                                                term_maturity=future_time)
                term_structure_ = VasicekModel().term_structure(spot_rate=spot_rate,
                                                                time_to_maturity=self.MATURITY_ARRAY,
                                                                gamma=parameters['gamma'],
                                                                rho=parameters['rho'],
                                                                q=parameters['q'],
                                                                alpha=parameters['alpha'])
            except Exception as exp:
                print(index, exp)
            else:
                row = pd.Series(term_structure_, index=self.MATURITY_ARRAY)
                df[index] = row

        return df
