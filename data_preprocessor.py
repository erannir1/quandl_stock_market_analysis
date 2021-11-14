import numpy as np
import pandas as pd
from pandas import DataFrame


class DataPreprocessor:
    """
    Class purpose: prepare the data for plotting
    """
    def __init__(self, quandl_df: DataFrame, column_to_analyze: str):
        """
        :param quandl_df: DataFrame retrieved from quandl
        :param column_to_analyze: The column you want to work with in the process
        """
        self.quandl_df = quandl_df
        self.column_to_analyze = column_to_analyze

    def add_n_moving_avg_column(self, num_list: list):
        """
        :param num_list: List of numbers that represent the timespan for the moving average
        :return: Returns the df with additional moving averages columns
        """
        for num in num_list:
            # Setting moving average column name:
            ma_str = f'{num} Moving Average'
            # Adding moving average column:
            self.quandl_df[ma_str] = self.quandl_df[self.column_to_analyze].rolling(window=num).mean()
        return self.quandl_df

    def get_price_monthly_avg(self):
        """
        :return: Series of the average price in each month
        """
        # Group data by month:
        df_grouped_by_months = self.quandl_df.groupby(pd.PeriodIndex(self.quandl_df.index, freq="M"))
        # Get the close column mean per month
        price_monthly_avg_series = df_grouped_by_months[self.column_to_analyze].mean()
        return price_monthly_avg_series

    def get_consecutive_stock_trend(self, consecutive_amount: int, drop_or_rise: str):
        """
        :param consecutive_amount: Amount of days with the same trend (drop / rise)
        :param drop_or_rise: What trend you want to check ('drop' / 'rise')
        :return: Series of the of the consecutive trends
        """
        column_data = self.quandl_df[self.column_to_analyze]
        # Rise case
        if drop_or_rise == 'rise':
            consecutive_trend = \
                column_data.rolling(consecutive_amount+1).apply(lambda x: np.all(np.diff(x) > 0)).astype(bool)
        # Drop case:
        elif drop_or_rise == 'drop':
            consecutive_trend = \
                column_data.rolling(consecutive_amount+1).apply(lambda x: np.all(np.diff(x) < 0)).astype(bool)
        else:
            # Error in case of wrong input
            raise ValueError(f"drop_or_rise should be 'drop' or 'rise' not {drop_or_rise}")
        return consecutive_trend
