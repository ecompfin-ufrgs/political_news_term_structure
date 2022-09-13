import matplotlib.pyplot as plt

from term_structure import SpotRate, TermStructure


def main():

    spot_s = SpotRate(spot_rate_path='../../../databases/di_anual.csv')()
    term_df = TermStructure(term_structure_path='../../../databases/economatica.xlsx',
                            spot_rate_index=spot_s.index)()

    for index, row in term_df.iterrows():
        row = row.dropna()
        plt.plot(row)
    plt.savefig('future.png')
    plt.clf()


if __name__ == '__main__':
    main()
