import pandas as pd

import vasicek


def calculate_parameters_for_term_structure(term_structure_df: pd.DataFrame):

    for index, row in term_structure_df.iterrows():
        row = row.dropna()
        row_index = row.index.to_numpy()
        row_values = row.values
        parameters = vasicek.minimize_see(term_rate=row_values,
                                          term_matutiry=row_index)
        term_structure = vasicek.term_structure(spot_rate=parameters['spot_rate'], 
                                                time_to_maturity=np.array([0, 21, 63, 252]),
                                                gamma=parameters['gamma'],
                                                rho=parameters['rho'],
                                                q=parameters['q'],
                                                alpha=parameters['alpha'])
        print(term_structure)
