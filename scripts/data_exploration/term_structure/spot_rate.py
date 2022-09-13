import matplotlib.pyplot as plt

from term_structure import SpotRate


def main():

    spot_s = SpotRate(spot_rate_path='../../../databases/di_anual.csv')()

    plt.plot(spot_s)
    plt.savefig('spot_rate.png')
    plt.clf()


if __name__ == '__main__':
    main()
