import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from econometrics import GARCH
from term_structure import TermStructureManager
from vasicek import VasicekManager


def plot_separate(dataframe: pd.DataFrame) -> None:
    for column in dataframe.columns:
        plt.plot(dataframe[column])
    plt.savefig('individual_maturities.png')
    plt.clf()


def plot_3d(dataframe: pd.DataFrame) -> None:
    x = np.array([[index.timestamp() for _ in dataframe.columns] for index in dataframe.index])
    y = np.array([dataframe.columns for _ in dataframe.index])
    z = dataframe.to_numpy()

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(x, y, z, color='black')
    plt.savefig('all_dates.png')
    plt.clf()


def main():

    term_structure = TermStructureManager(spot_rate_path='../../databases/di_anual.csv',
                                          term_structure_path='../../databases/economatica.xlsx')()
    vasicek_df = VasicekManager(term_structure=term_structure)()
    vasicek_df = vasicek_df.T

    diff_df = pd.DataFrame()
    for column in vasicek_df.columns:
        diff_df[column] = vasicek_df[column]/vasicek_df[column].shift(1) - 1
    diff_df = diff_df.dropna(axis=0)

    vol_df = pd.DataFrame()
    for column in diff_df.columns:
        vol_df[column] = GARCH()(series=diff_df[column])

    plot_separate(vol_df)
    plot_3d(vol_df)



if __name__ == '__main__':
    main()
