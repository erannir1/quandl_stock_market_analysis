import quandl


class DataRetriever:
    def __init__(self, stock_market: str, start_date: str, end_date: str, api_key: str):
        """
        :param stock_market: String of the stock market
        :param start_date: string of the start date of the data to retrieve
        :param end_date: string of the end date of the data to retrieve
        :param api_key: Your API Key - please put your API key in the credentials file
        """
        self.stock_market = stock_market
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key

    def retrieve_data_from_quandl(self):
        """
        :return: Retrieved stocks dataframe from quandl of the chosen stock market
        """
        data = quandl.get(self.stock_market, start_date=self.start_date, end_date=self.end_date, api_key=self.api_key)
        return data
