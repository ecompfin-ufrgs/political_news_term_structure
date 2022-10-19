import datetime as dt
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm

from econometrics import GARCH, Granger
from news_volume import NewsManager
from term_structure import TermStructureManager
from vasicek import VasicekManager


def plot_news_volume(news_series_dict: dict) -> None:
    # Plot individual portals
    for news_portal_name, daily_volume_series in news_series_dict.items():
        plt.plot(daily_volume_series)
        plt.ylabel('Volume of News Articles')
        plt.xlabel('Time')
        plt.savefig(f'{news_portal_name}.png')
        plt.clf()
    # Plot sum of all portals
    plt.plot(news_series_dict['g1']+news_series_dict['minas'])
    plt.ylabel('Volume of News Articles')
    plt.xlabel('Time')
    plt.savefig('total_news.png')
    plt.clf()


def plot_spot_rate(spot_series: pd.Series) -> None:
    plt.plot(spot_series)
    plt.ylabel('Spot Rate')
    plt.xlabel('Time')
    plt.savefig('spot.png')
    plt.clf()


def plot_multiple_term_structure(df: pd.DataFrame) -> None:
    for index, row in df.loc[df.index[::int(len(df.index)/6)]].iterrows():
        plt.plot(row.dropna().sort_index(), marker='o', label=index)
    plt.legend()
    plt.ylabel('Price')
    plt.xlabel('Days to Maturity')
    plt.savefig('6_dates_term.png')
    plt.clf()


def plot_vasicek(df: pd.DataFrame):

    x = np.array([[index for _ in df.columns] for index in df.index.to_series().apply(lambda x: dt.datetime.combine(x, dt.time()).timestamp())])
    y = np.array([df.columns for _ in df.index])
    z = df.to_numpy()

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(x, y, z, color='black')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Years to Maturity')
    ax.set_zlabel('Interest Rate')
    plt.savefig('vasicek.png')
    plt.clf()


def plot_volatility(dataframe: pd.DataFrame) -> None:
    x = np.array([[index for _ in dataframe.columns] for index in dataframe.index.to_series().apply(lambda x: dt.datetime.combine(x, dt.time()).timestamp())])
    y = np.array([dataframe.columns for _ in dataframe.index])
    z = dataframe.to_numpy()

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(x, y, z, color='black')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Years to Maturity')
    ax.set_zlabel('Conditional Volatility')
    plt.savefig('volatility.png')
    plt.clf()


def plot_causality_surface(causality_df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(10, 10))
    x = [[index for _ in causality_df.columns] for index in causality_df.index]
    y = [causality_df.columns for _ in causality_df.index]
    z = causality_df.to_numpy()
    cs = plt.contourf(x, y, z, levels=[0.0, 0.01, 0.05, 0.1, 1])
    cbar = plt.colorbar(cs)
    plt.xlabel('Years to Maturity')
    plt.ylabel('Lags')
    plt.savefig('causality_surface.png')
    plt.clf()


def main():

    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

    start_date = dt.date(2019, 1, 1)
    end_date = dt.date(2020, 10, 14)

    news_series_dict = dict(g1=NewsManager(db_path='../../databases/g1.db',
                                           table='g1')().loc[start_date:end_date],
                            minas=NewsManager(db_path='../../databases/minas.db',
                                              table='minas7')().loc[start_date:end_date])

    plot_news_volume(news_series_dict=news_series_dict)

    term_structure = TermStructureManager(spot_rate_path='../../databases/di_anual.csv',
                                          term_structure_path='../../databases/economatica.xlsx',
                                          start_date=start_date,
                                          end_date=end_date)()

    plot_spot_rate(spot_series=term_structure['spot'])
    plot_multiple_term_structure(df=term_structure['future'])

    vasicek_df = VasicekManager(term_structure=term_structure)()
    vasicek_df = vasicek_df.T

    plot_vasicek(vasicek_df)

    vol_df = pd.DataFrame()
    for column in vasicek_df.columns:
        vol_df[column] = GARCH()(series=vasicek_df[column])

    plot_volatility(vol_df)

    # vol_df.index = [index.to_pydatetime().date() for index in vol_df.index]

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
    plot_multiple_term_structure(df=term_structure['future'].loc[all_df.index])


if __name__ == '__main__':
    main()
