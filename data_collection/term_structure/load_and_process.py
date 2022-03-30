import datetime as dt

import pandas as pd


def load_term_structure_data(dataframe_name: str) -> pd.DataFrame:
    """
    Loads term structure data from .xlsx file, setting the header row and selecting useful
    columns.
    """
    return pd.read_excel(dataframe_name, header=3, index_col=0).iloc[:, :1]


def original_columns_to_datetime(dataframe_columns: list) -> pd.Series:
    """
    Converts the original column names of the term structure dataframe to datetime objects.

    Column names start with the letter of the month of the expiration of the contract. This letter
    if followed by the last two digits of the year of the expiration of the contract.
    """
    asset_symbol_to_month = {'F': '01', 'G': '02', 'H': '03', 'J': '04', 'K': '05', 'M': '06',
                             'N': '07', 'Q': '08', 'U': '09', 'V': '10', 'X': '11', 'Z': '12'}
    date_index = ['01/2000', '01/2000'] + [f'{asset_symbol_to_month[column[:1]]}/20{column[1:-3]}'
                                           for column in dataframe_columns]
    date_index = pd.to_datetime(date_index, format='%m/%Y')
    return date_index


def fix_day_in_columns_datetime(dataframe_columns) -> pd.Series:
    """
    Sets the day for each column datetime to the first working day of the respective month.

    All column datetime are at day 1 of each month.
    """
    work_calendar = Brazil
    dates = []
    for date in dataframe_columns:
        while not work_calendar.is_working_day(date):
            date += dt.timedelta(days=1)
        dates.append(date)
    dates = pd.to_datetime(dates)
    return dates


def process_columns(dataframe_columns: list) -> pd.Series:
    """
    Converts the original column names to the day of expiration of each contract.
    """
    dataframe_columns = original_columns_to_datetime(dataframe_columns=dataframe_columns)
    dataframe_columns = fix_day_in_columns_datetime(dataframe_columns=dataframe_columns)
    return dataframe_columns


def create_dataframe_with_columns_as_days_to_expiration(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Creates dataframe where each row is a trading date and each column in the number of days until
    a contract's expiration.
    """
    df = pd.DataFrame()
    for date_index in dataframe.index:
        date_dictionary = {}
        for contract_expiration_date in dataframe.columns:
            price_of_contract = data[contract_expiration_date][date_index]
            if type(price_of_contract) == float:
                date_dictionary[contract_expiration_date - date_index] = price_of_contract
                # TODO: it seems like the algorithm is calculating the date difference on calendar days instead of
                #       working days
        date_series = pd.Series(date_dictionary, name=index)
        df = df.append(date_series)
    df = df.reindex(sorted(df.columns), axis=1)
    return df

def load_and_process_term_structure_data(dataframe_name: str) -> pd.DataFrame:
    """
    Loads term structure data and process it so it has, for each day, the time to expiration of each contract with the
    correspondent price of the contract.
    """
    dataframe = load_term_structure_data(dataframe_name=dataframe_name)
    dataframe.columns = process_columns(dataframe_columns=dataframe.columns)
    dataframe = create_dataframe_with_columns_as_days_to_expiration(dataframe=dataframe)
    return dataframe
