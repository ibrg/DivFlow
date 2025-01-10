import fmpsdk

from typing import List, Dict

from env import API_KEY


EXCHANGES = ["New York Stock Exchange", "NASDAQ"]


def filter_stock_on_exchanges(stock_list: List[Dict], exchanges: List[str]=EXCHANGES) -> List[Dict]:
    """
    Filters the stock list based on the exchanges.
    
    :param stock_list: THe stock list (list of dict).
    :param exchanges: The list of exchanges  (list of str).
    :return: The filtered list of exchanges.
    """
    return [stock for stock in stock_list if stock.get("exchange") in exchanges]


def fetch_filtered_stock_list(api_key: str = API_KEY) -> List[Dict]:
    """
    Fetch stock list API fmpsdk and filter by US exchanges.

    :param api_key: API KEY to access fmpsdk.
    :return: The filterd list of stock.
    :raises: Exception if data retrieval failed.
    """
    usa_exchanges = ["New York Stock Exchange", "NASDAQ"]
    try:
        # Получение данных из API
        if not api_key:
            raise ValueError("API key is missing.")
        response = fmpsdk.symbols_list(apikey=api_key)
        if not isinstance(response, list):
            raise ValueError("Unexpected API response format: Expected a list of stocks.")
        return  filter_stock_on_exchanges(response, usa_exchanges)
    except Exception as e:
        raise Exception(f"Error when receiving data from API: {e}")


def fetch_dividend_data(ticker):
    # Fetch dividend data from yahoo finance
    ...

