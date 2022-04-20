import numpy as np
from scipy.optimize import minimize

from term_structure import term_structure


def objective(x,
              term_rate: np.array,
              term_maturity: np.array
              ):

    predicted_term_rate = term_structure(x[0],
                                         term_maturity,
                                         x[1],
                                         x[2],
                                         x[3],
                                         x[4])
    return sum((term_rate-predicted_term_rate)**2)


def estimate_parameters(term_rate: np.array,
                        term_maturity: np.array
                        ):
    x0 = [0.0, 0.0, 0.0, 0.0, 0.0]
    result = minimize(lambda x: objective(x, term_rate, term_maturity),
                      x0)
    res = {
        'spot_rate': result.x[0],
        'gamma': result.x[1],
        'rho': result.x[2],
        'q': result.x[3],
        'alpha': result.x[4]
    }
    return res
