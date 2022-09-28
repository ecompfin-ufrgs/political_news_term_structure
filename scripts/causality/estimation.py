import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm

from econometrics import GARCH, Granger
from news_volume import NewsManager
from term_structure import TermStructureManager
from vasicek import VasicekManager


def plot_causality_surface(causality_df: pd.DataFrame) -> None:

    fig = plt.figure(figsize=(10, 10))
    x = [[index for _ in causality_df.columns] for index in causality_df.index]
    y = [causality_df.columns for _ in causality_df.index]
    z = causality_df.to_numpy()
    cs = plt.contourf(x, y, z, levels=20)
    cbar = plt.colorbar(cs)
    plt.savefig('causality_surface.png')
    plt.clf()


def plot_causality_binary_surface(causality_df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(10, 10))
    x = [[index for _ in causality_df.columns] for index in causality_df.index]
    y = [causality_df.columns for _ in causality_df.index]
    z = causality_df.to_numpy()
    cs = plt.contourf(x, y, z, levels=[0.0, 0.05, 1])
    cbar = plt.colorbar(cs)
    plt.savefig('causality_surface.png')
    plt.clf()


def main():

    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

    term_structure = TermStructureManager(spot_rate_path='../../databases/di_anual.csv',
                                          term_structure_path='../../databases/economatica.xlsx')()
    vasicek_df = VasicekManager(term_structure=term_structure)()
    vasicek_df = vasicek_df.T

    vol_df = pd.DataFrame()
    for column in vasicek_df.columns:
        vol_df[column] = GARCH()(series=vasicek_df[column])

    news_series_dict = dict(g1=NewsManager(db_path='../../databases/g1.db',
                                           table='g1')(),
                            minas=NewsManager(db_path='../../databases/minas.db',
                                              table='minas7')())

    vol_df.index = [index.to_pydatetime().date() for index in vol_df.index]

    # news_series_dict['g1'] = news_series_dict['g1'].loc[vol_df.index[0]:vol_df.index[-1]]
    # news_series_dict['minas'] = news_series_dict['g1'].loc[vol_df.index[0]:vol_df.index[-1]]

    news_df = pd.DataFrame()
    news_df['volume'] = news_series_dict['g1'] + news_series_dict['minas']

    all_df = vol_df[:]
    all_df['volume'] = news_df['volume']
    all_df = all_df.dropna(0)

    vol_df = vol_df.loc[all_df.index]
    news_df = news_df.loc[all_df.index]

    causality_df = pd.DataFrame()
    for column in tqdm.tqdm(vol_df.columns):
        res = Granger(news_df['volume'], vol_df[column])()
        causality_df[column] = pd.Series({key: value[0]['params_ftest'][1] for key, value in res.items()})

    causality_df = causality_df.T

    plot_causality_surface(causality_df=causality_df)
    plot_causality_binary_surface(causality_df=causality_df)


if __name__ == '__main__':
    main()
