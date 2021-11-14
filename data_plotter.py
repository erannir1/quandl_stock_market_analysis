import numpy as np
from pandas import DataFrame, Series
import seaborn as sns
import matplotlib.pyplot as plt


class DataPlotterConfig:
    DROP_MARKER = 'v'
    DROP_MARKER_COLOR = 'red'
    RISE_MARKER = '^'
    RISE_MARKER_COLOR = 'green'
    X_TICKS_ROTATION = 40
    REGRESSION_LINE_MARKER = '+'
    REGRESSION_LINE_MARKER_COLOR = 'red'


class DataPlotter:
    def __init__(self, df_after_preprocessing: DataFrame, stock_market: str, column_to_plot: str):
        """
        :param df_after_preprocessing: Quandl dataframe after being processed
        :param stock_market: String of the stock market
        :param column_to_plot: Name of the column you analyzed
        """
        self.df = df_after_preprocessing
        self.stock_market = stock_market
        self.column_to_plot = column_to_plot

    def plot_price_and_moving_avg(self, num_list: list, monthly_avg):
        """
        :param num_list: List of numbers that represent the amount of moving averages
        :param monthly_avg: Series of the monthly average prices
        :return:
        """
        plt.plot(self.df[self.column_to_plot], label=self.column_to_plot)
        for num in num_list:
            num_ma_str = f'{num} Moving Average'                    # Set moving average string
            num_label_str = f'MA {num} days'                        # Set label string
            plt.plot(self.df[num_ma_str], label=num_label_str)
        plt.plot(monthly_avg, label='Monthly Average', marker='o')
        plt.legend(loc='best')
        plt.plot(self.df['Rise'], marker=DataPlotterConfig.RISE_MARKER, color=DataPlotterConfig.RISE_MARKER_COLOR)
        plt.plot(self.df['Drop'], marker=DataPlotterConfig.DROP_MARKER, color=DataPlotterConfig.DROP_MARKER_COLOR)
        plt.title(f'{self.stock_market}\n{self.column_to_plot}, Monthly Average and Moving Averages')
        plt.ylabel(f'{self.column_to_plot} Price')                  # Set the Y axis label
        plt.xlabel('Date')                                          # Set the X axis label
        plt.xticks(rotation=DataPlotterConfig.X_TICKS_ROTATION)     # Set the x axis ticks
        plt.show()

    def plot_linear_regression(self, time_span: int, tick_vis: int):
        """
        :param time_span: Timespan integer that determines how far back to use the data
        :param tick_vis: Integer that helps set the amount of x ticks visible
        :return:
        """
        df = self.df.tail(time_span)
        num_days = len(df)
        x = np.array(range(len(df.index)))
        y = df[self.column_to_plot].values
        p = sns.regplot(x, y,
                        marker=DataPlotterConfig.REGRESSION_LINE_MARKER,
                        color=DataPlotterConfig.REGRESSION_LINE_MARKER_COLOR)
        p.set_title(f'{num_days} Days Regression Line')                     # Set title
        p.set_ylabel(f'{self.column_to_plot} Price')                        # Set the Y axis label
        p.set_xlabel('Date')                                                # Set the X axis label
        dates = [i.date() for i in list(df.index)]                          # Get list of the dates
        plt.xticks(x, dates, rotation=DataPlotterConfig.X_TICKS_ROTATION)   # Set the x axis ticks to be the dates
        for ind, label in enumerate(p.get_xticklabels()):                   # Show x tick only if condition
            if ind % tick_vis == 0:  # every 10th label is kept
                label.set_visible(True)
            else:
                label.set_visible(False)
        plt.show()

    def plot_monthly_price_avg(self, monthly_average: Series, market_str: str):
        plt.plot(self.df[self.column_to_plot], label=self.column_to_plot)
        plt.plot(monthly_average, label='Monthly Price Average', marker='o', color='red')
        plt.ylabel(f'{self.column_to_plot} Price')
        plt.xlabel('Date')
        plt.xticks(rotation=DataPlotterConfig.X_TICKS_ROTATION)
        plt.legend(loc='best')
        plt.title(f'{market_str}\n{self.column_to_plot} and Monthly Price Average')
        plt.show()
