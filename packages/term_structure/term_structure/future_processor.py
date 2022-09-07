import multiprocessing as mp
import time
import tqdm

import pandas as pd
from pandas import DatetimeIndex
from workalendar.america.brazil import BrazilSaoPauloCity


class FutureProcessor:

    def __call__(self,
                 dataframe: pd.DataFrame
                 ) -> pd.DataFrame:
        """
        Loads term structure data and process it so it has, for each day, the time to expiration of each contract with the
        correspondent price of the contract.
        """
        dataframe.columns = self.original_columns_to_datetime(dataframe_columns=dataframe.columns.to_list())
        dataframe.columns = self.fix_day_in_columns_datetime(dataframe_columns=dataframe.columns)
        dataframe = self.days_expiration_mp(dataframe=dataframe)
        return dataframe

    @staticmethod
    def original_columns_to_datetime(dataframe_columns: list
                                     ) -> pd.DatetimeIndex:
        """
        Converts the original column names of the term structure dataframe to datetime objects.

        Column names start with the letter of the month of the expiration of the contract. This letter
        if followed by the last two digits of the year of the expiration of the contract.
        """
        asset_symbol_to_month = {'F': '01', 'G': '02', 'H': '03', 'J': '04', 'K': '05', 'M': '06',
                                 'N': '07', 'Q': '08', 'U': '09', 'V': '10', 'X': '11', 'Z': '12'}
        date_index = [f'20{asset_symbol[-2:]}-{asset_symbol_to_month[asset_symbol[-3]]}' for asset_symbol in dataframe_columns]
        date_index = pd.to_datetime(date_index, format='%Y-%m')
        return date_index

    @staticmethod
    def fix_day_in_columns_datetime(dataframe_columns
                                    ) -> DatetimeIndex:
        """
        Sets the day for each column datetime to the first working day of the respective month.

        All column datetime are at day 1 of each month.
        """
        sao_paulo_calendar = BrazilSaoPauloCity()
        dates = []
        for date in dataframe_columns:
            dates.append(sao_paulo_calendar.find_following_working_day(date))
        dates = pd.to_datetime(dates)
        return dates

    def days_expiration_mp(self,
                           dataframe: pd.DataFrame
                           ) -> pd.DataFrame:
        sao_paulo_calendar = BrazilSaoPauloCity()
        df = pd.DataFrame()
        mp_iter = [{'df': df, 'sao_paulo_calendar': sao_paulo_calendar, 'index': index, 'row': row} for index, row in dataframe.iterrows()]
        df = pd.DataFrame(mp.Pool().map(self.process_row, tqdm.tqdm(mp_iter)))
        return df

    @staticmethod
    def process_row(info: dict):
        row = info['row'].dropna()
        date_dictionary = {}
        for contract_expiration_date, price_of_contract in row.iteritems():
            if type(price_of_contract) == float:
                date_dictionary[
                    info['sao_paulo_calendar'].get_working_days_delta(info['index'], contract_expiration_date)] = price_of_contract
        date_series = pd.Series(date_dictionary, name=info['index'], dtype=float)
        return date_series
