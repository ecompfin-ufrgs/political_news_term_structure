import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from term_structure import TermStructureManager
from vasicek import VasicekManager


def plot_individual_dates(df: pd.DataFrame):
    for column in df.columns:
        series = df[column]
        series = series.dropna()
        plt.plot(series)
    plt.savefig('individual_dates.png')
    plt.clf()


def plot_all_dates(df: pd.DataFrame):

    x = np.array([[column.timestamp() for _ in df.index] for column in df.columns])
    y = np.array([df.index for _ in df.columns])
    z = df.to_numpy().T

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(x, y, z, color='black')
    plt.savefig('all_dates.png')
    plt.clf()


def main():

    term_structure = TermStructureManager(spot_rate_path='../../databases/di_anual.csv',
                                          term_structure_path='../../databases/economatica.xlsx')()
    vasicek_df = VasicekManager(term_structure=term_structure)()

    print(vasicek_df)


if __name__ == '__main__':
    main()
