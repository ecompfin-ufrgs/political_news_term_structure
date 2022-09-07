import numpy as np


class VasicekModel:

    def term_structure(self,
                       spot_rate: float,
                       time_to_maturity: np.array,
                       gamma: float,
                       rho: float,
                       q: float,
                       alpha: float
                       ) -> np.array:
        r_inf = self.infinite_yield(gamma, rho, q, alpha)
        cons = 1 - np.exp(-alpha * time_to_maturity)

        a = (spot_rate - r_inf) * (1 / (alpha * time_to_maturity)) * cons
        b = rho ** 2 / (4 * alpha ** 3 * time_to_maturity) * cons ** 2

        return r_inf + a + b

    @staticmethod
    def infinite_yield(gamma: float,
                       rho: float,
                       q: float,
                       alpha: float
                       ) -> float:
        return gamma + rho * q / alpha - (1 / 2) * (rho**2 / alpha**2)
