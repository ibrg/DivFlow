import os
from dotenv import load_dotenv

import fmpsdk
import sqlite3

from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY_fmpsdk")
DB_NAME = os.getenv("SQLITE_DB_NAME")
EXCHANGES = ["New York Stock Exchange", "NASDAQ"]


def filter_stock_on_exchanges(
    stock_list: List[Dict], exchanges: List[str] = EXCHANGES
) -> List[Dict]:
    """
    Filters the stock list based on the exchanges.

    :param stock_list: The stock list (list of dict).
    :param exchanges: The list of exchanges  (list of str).
    :return: The filtered list of exchanges.
    """
    logger.info("Filtering stock list")
    return [stock for stock in stock_list if stock.get("exchange") in exchanges]


def fetch_stock_list(api_key: str | None = API_KEY) -> List[Dict]:
    """
    Fetch stock list API fmpsdk and filter by US exchanges.

    :param api_key: API KEY to access fmpsdk.
    :return: The filterd list of stock.
    :raises: Exception if data retrieval failed.
    """
    try:
        if not api_key:
            raise ValueError("API key is missing.")
        response = fmpsdk.symbols_list(apikey=api_key)
        if not response:
            logger.warning("No stocks retrieved from the API.")
            raise ValueError("No stocks retrieved from the API.")
        if not isinstance(response, list):
            raise ValueError(
                "Unexpected API response format: Expected a list of stocks."
            )
        return response
    except Exception as e:
        logger.error(f"Error when receiving data from API: {e}")
        raise


def write_to_db(data: List[Dict]):
    """
    Write the data to the database.

    :param data: The data to write (list of dict).
    """
    if not DB_NAME:
        raise ValueError("DB_NAME is not set in the environment variables.")

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        # Ensure the table exists
        c.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        try:
            for stock in data:
                # Validate that required keys exist and are not empty
                required_keys = {"symbol", "name", "price"}
                if not required_keys.issubset(stock.keys()):
                    logger.warning(f"Skipping invalid stock data (missing keys): {stock}")
                    continue

                # Additional validation for empty or null values
                if not all(stock.get(key) for key in required_keys):
                    logger.warning(f"Skipping stock with empty values: {stock}")
                    continue

                # Check if the stock already exists
                c.execute("SELECT 1 FROM stock WHERE symbol = ?", (stock["symbol"],))
                if c.fetchone() is None:
                    c.execute(
                        """
                        INSERT INTO stock (symbol, name, price, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            stock["symbol"],
                            stock["name"],
                            stock["price"],
                            datetime.now().isoformat(),
                            datetime.now().isoformat(),
                        ),
                    )
            conn.commit()
            logger.info("Data written to the database successfully.")
        except Exception as e:
            logger.error(f"Error when writing to the database: {e}")
            raise

# Main execution
if __name__ == "__main__":
    try:
        stock_list = fetch_stock_list()
        filtered_stocks = filter_stock_on_exchanges(stock_list)
        write_to_db(filtered_stocks)
    except ValueError as ve:
        logger.warning(f"Validation error occurred: {ve}")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
