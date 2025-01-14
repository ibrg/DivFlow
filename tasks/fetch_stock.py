import os
from dotenv import load_dotenv

import fmpsdk
import sqlite3

from datetime import datetime

from typing import List, Dict


load_dotenv()

API_KEY = os.getenv("API_KEY_fmpsdk")
DB_NAME = os.getenv("SQLITE_DB_NAME")


EXCHANGES = ["New York Stock Exchange", "NASDAQ"]


def filter_stock_on_exchanges(
    stock_list: List[Dict], exchanges: List[str] = EXCHANGES
) -> List[Dict]:
    """
    Filters the stock list based on the exchanges.

    :param stock_list: THe stock list (list of dict).
    :param exchanges: The list of exchanges  (list of str).
    :return: The filtered list of exchanges.
    """
    print("Filtering stock list")
    return [stock for stock in stock_list if stock.get("exchange") in exchanges]


def fetch_stock_list(api_key: str | None = API_KEY) -> List[Dict]:
    """
    Fetch stock list API fmpsdk and filter by US exchanges.

    :param api_key: API KEY to access fmpsdk.
    :return: The filterd list of stock.
    :raises: Exception if data retrieval failed.
    """
    try:
        # Получение данных из API
        if not api_key:
            raise ValueError("API key is missing.")
        response = fmpsdk.symbols_list(apikey=api_key)
        if not isinstance(response, list):
            raise ValueError(
                "Unexpected API response format: Expected a list of stocks."
            )
        print("Fetching data from API")
        return response
    except Exception as e:
        raise Exception(f"Error when receiving data from API: {e}")


def fetch_dividend_data(ticker):
    # Fetch dividend data from yahoo finance
    ...


def write_to_db(data: List[Dict]):
    """
    Write the data to the database.

    :param data: The data to write (list of dict).
    """

    # Connect to the database
    if not DB_NAME:
        raise ValueError("DB_NAME is not set in the environment variables.")
    conn = sqlite3.connect(DB_NAME)

    try:
        c = conn.cursor()
        print("Connected to the database", c)
        for stock in data:
            # Insert the stock data into the database
            if (
                not stock.get("symbol")
                or not stock.get("name")
                or not stock.get("price")
            ):
                print(f"Skipping invalid stock data: {stock}")
                continue
            c.execute(
                "INSERT INTO stock (symbol, name, price, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (
                    stock["symbol"],
                    stock["name"],
                    stock["price"],
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )

    except Exception as e:
        raise Exception(f"Error when connecting to the database: {e}")

    # Commit the changes
    conn.commit()
    print("Data written to the database")
    # Close the connection
    conn.close()


write_to_db(filter_stock_on_exchanges(fetch_stock_list()))
