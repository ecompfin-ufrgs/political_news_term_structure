import datetime as dt
import typing as tp

import pandas as pd

from .spot_rate import SpotRate
from .term_structure import TermStructure


class TermStructureManager:

    def __init__(self,
                 spot_rate_path: str,
                 term_structure_path: str,
                 start_date: dt.date,
                 end_date: dt.date
                 ) -> None:
        self.spot_rate_path = spot_rate_path
        self.term_structure_path = term_structure_path
        self.start_date = start_date
        self.end_date = end_date

    def __call__(self
                 ) -> dict[str, tp.Union[pd.Series, pd.DataFrame]]:
        spot = SpotRate(spot_rate_path=self.spot_rate_path)().loc[self.start_date:self.end_date]
        future = TermStructure(term_structure_path=self.term_structure_path,
                               spot_rate_index=spot.index)()
        return dict(spot=spot,
                    future=future)
