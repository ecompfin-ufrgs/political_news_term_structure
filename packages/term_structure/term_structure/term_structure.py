import typing as tp

import pandas as pd

from .future_processor import FutureProcessor


class TermStructure:

    def __init__(self,
                 term_structure_path: str,
                 spot_rate_index: tp.Optional[pd.Index] = None
                 ) -> None:
        self.term_structure_path = term_structure_path
        self.spot_rate_index = spot_rate_index

    def __call__(self
                 ) -> pd.DataFrame:
        dataframe = pd.read_excel(self.term_structure_path, header=3, index_col=0)
        future_df = dataframe.iloc[:, 1:]
        future_df.index = future_df.index.to_series().apply(lambda x: x.to_pydatetime().date())
        if self.spot_rate_index is not None:
            future_df = future_df.loc[self.spot_rate_index]
        future_df = FutureProcessor()(dataframe=future_df)
        return future_df
