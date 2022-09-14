import typing as tp

import pandas as pd

from .spot_rate import SpotRate
from .term_structure import TermStructure


class TermStructureManager:

    def __init__(self,
                 spot_rate_path: str,
                 term_structure_path: str
                 ) -> None:
        self.spot_rate_path = spot_rate_path
        self.term_structure_path = term_structure_path

    def __call__(self
                 ) -> dict[str, tp.Union[pd.Series, pd.DataFrame]]:
        spot = SpotRate(spot_rate_path=self.spot_rate_path)()
        future = TermStructure(term_structure_path=self.term_structure_path,
                               spot_rate_index=spot.index)()
        return dict(spot=spot,
                    future=future)
