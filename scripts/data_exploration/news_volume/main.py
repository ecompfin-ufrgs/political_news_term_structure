import matplotlib.pyplot as plt
import pandas as pd

from news_volume import NewsManager


def plot_news_volume(news_series_dict: dict[str, pd.Series]
                     ) -> None:
    for news_portal_name, daily_volume_series in news_series_dict.items():
        plt.plot(daily_volume_series, label=news_portal_name)
    plt.legend()
    plt.savefig('daily_news_volume.png')
    plt.clf()

    for news_portal_name, daily_volume_series in news_series_dict.items():
        plt.plot(daily_volume_series)
        plt.savefig(f'{news_portal_name}.png')
        plt.clf()


def main():

    news_series_dict = dict(g1=NewsManager(db_path='../../../databases/g1.db',
                                           table='g1')(),
                            minas=NewsManager(db_path='../../../databases/minas.db',
                                              table='minas7')())
    plot_news_volume(news_series_dict=news_series_dict)


if __name__ == '__main__':
    main()
