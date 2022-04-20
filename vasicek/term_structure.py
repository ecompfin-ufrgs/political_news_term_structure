from typing import Union

import numpy as np


def infinite_yield(gamma: float,
                   rho: float,
                   q: float,
                   alpha: float
                   ) -> float:
    
    return gamma + (rho*q)/alpha - (1/2)*(rho**2/alpha**2)


def term_structure(spot_rate: float,
                   time_to_maturity: Union[float, np.array],
                   gamma: float,
                   rho: float,
                   q: float,
                   alpha: float
                   ) -> Union[float, np.array]:
    
    r_inf = infinite_yield(gamma, rho, q, alpha)
    cons = (1-np.exp(-alphe*time_to_maturity))

    a = (spot_rate-r_inf)*(1/(alpha*t))*cons
    b = rho**2/(4*alpha**3*time_to_maturity)*cons**2
    
    return a + b    
    