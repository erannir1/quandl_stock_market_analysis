import quandl
from math import ceil

from data_retriever import DataRetriever
from data_preprocessor import DataPreprocessor
from data_plotter import DataPlotter

from credentials import quandl_api_key

# INSTRUCTIONS:
# Connect and retrieve data from https://www.quandl.com/api/v3/datasets/FSE/BDT_X (Frankfurt Stock Exchange).
# Display the 90,30,7 days moving average on a plot graph.
# Display also the monthly avg price on that graph.
# Detect and present the dates where there are 5 consecutive days of prices going up.
# Detect and present the dates where there are 4 consecutive days of prices going down (different symbol).
# Calculate and show on the graph a regression line for the last 90, 30 and 7 days in the plot.


class MainConfig:
    STOCK_MARKET_URL_PATH = 'https://www.quandl.com/api/v3/datasets/FSE/BDT_X'
    STOCK_MARKET_STRING = "FSE/BDT_X"
    START_DATE = "2020-01-01"
    END_DATE = "2020-12-31"
    COLUMN_TO_ANALYZE = 'Close'
    COLUMN_TO_PLOT = COLUMN_TO_ANALYZE
    MOVING_AVERAGE_NUMBER_LIST = [90, 30, 7]
    REGRESSION_LINE_NUMBERS_LIST = [90, 30, 7]
    CONSECUTIVE_RISE_AMOUNT = 5
    CONSECUTIVE_DROP_AMOUNT = 4
    QUANDL_API_KEY = quandl_api_key  # PLEASE update your own API key in the credentials file


if __name__ == '__main__':

    # Retrieve Data:
    fse_data = DataRetriever(stock_market=MainConfig.STOCK_MARKET_STRING,
                             start_date=MainConfig.START_DATE,
                             end_date=MainConfig.END_DATE,
                             api_key=MainConfig.QUANDL_API_KEY).retrieve_data_from_quandl()

    # Prepare Data:
    # Initialize the data pre processor object
    data_to_process = DataPreprocessor(quandl_df=fse_data, column_to_analyze=MainConfig.COLUMN_TO_ANALYZE)
    # Adds Moving Averages Columns to DataFrame
    data_with_moving_average = data_to_process.add_n_moving_avg_column(MainConfig.MOVING_AVERAGE_NUMBER_LIST)
    # Gets the Monthly Average Price Series
    monthly_price_average = data_to_process.get_price_monthly_avg()

    # Gets the Consecutive Rise Series
    consecutive_rise = \
        data_to_process.get_consecutive_stock_trend(consecutive_amount=MainConfig.CONSECUTIVE_RISE_AMOUNT,
                                                    drop_or_rise='rise')
    # Gets the Consecutive Drop Series
    consecutive_drop = \
        data_to_process.get_consecutive_stock_trend(consecutive_amount=MainConfig.CONSECUTIVE_DROP_AMOUNT,
                                                    drop_or_rise='drop')

    # Adds Consecutive Rise Column to DataFrame
    fse_data[f'{MainConfig.CONSECUTIVE_RISE_AMOUNT} Consecutive Rise'] = consecutive_rise
    fse_data['Rise'] = \
        fse_data[MainConfig.COLUMN_TO_ANALYZE][fse_data[f'{MainConfig.CONSECUTIVE_RISE_AMOUNT} Consecutive Rise'] == True]
    # Adds Consecutive Drop Column to DataFrame
    fse_data[f'{MainConfig.CONSECUTIVE_DROP_AMOUNT} Consecutive Drop'] = consecutive_drop
    fse_data['Drop'] = \
        fse_data[MainConfig.COLUMN_TO_ANALYZE][fse_data[f'{MainConfig.CONSECUTIVE_DROP_AMOUNT} Consecutive Drop'] == True]

    # Plotting Data:
    # Initialize the data plotter object
    data_plot = DataPlotter(df_after_preprocessing=fse_data,
                            stock_market=MainConfig.STOCK_MARKET_STRING,
                            column_to_plot=MainConfig.COLUMN_TO_PLOT)
    # Price, Moving Average and Monthly Average Plot
    data_plot.plot_price_and_moving_avg(num_list=MainConfig.MOVING_AVERAGE_NUMBER_LIST,
                                        monthly_avg=monthly_price_average)
    # Price and Monthly Average Plot
    data_plot.plot_monthly_price_avg(market_str=MainConfig.STOCK_MARKET_STRING,
                                     monthly_average=monthly_price_average)
    # Regression Line Plot
    for index in range(len(MainConfig.REGRESSION_LINE_NUMBERS_LIST)):
        x_tick_visibility = ceil(MainConfig.REGRESSION_LINE_NUMBERS_LIST[index] / 10)
        data_plot.plot_linear_regression(time_span=MainConfig.REGRESSION_LINE_NUMBERS_LIST[index],
                                         tick_vis=x_tick_visibility)
