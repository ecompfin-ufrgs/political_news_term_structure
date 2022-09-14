import numpy as np
import scipy

from .model import VasicekModel


class VasicekEstimator:

    def __call__(self,
                 spot_rate: float,
                 term_rate: np.array,
                 term_maturity: np.array
                 ):

        x0 = [1, 1, 1, 1]
        bounds = (-np.inf, np.inf)
        result = scipy.optimize.least_squares(fun=lambda x: self.objective(term_rate=term_rate,
                                                                           term_maturity=term_maturity,
                                                                           spot_rate=spot_rate,
                                                                           gamma=x[0],
                                                                           rho=x[1],
                                                                           q=x[2],
                                                                           alpha=x[3]),
                                              x0=x0,
                                              bounds=bounds)
        res = {
            'gamma': result.x[0],
            'rho': result.x[1],
            'q': result.x[2],
            'alpha': result.x[3]
        }
        return res

    @staticmethod
    def objective(term_rate: np.array,
                  term_maturity: np.array,
                  spot_rate,
                  gamma,
                  rho,
                  q,
                  alpha
                  ) -> np.array:
        estimated_term = VasicekModel().term_structure(spot_rate=spot_rate,
                                                       time_to_maturity=term_maturity,
                                                       gamma=gamma,
                                                       rho=rho,
                                                       q=q,
                                                       alpha=alpha)
        return (estimated_term - term_rate)**2
