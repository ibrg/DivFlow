from datetime import datetime
from typing import Optional

from sqlmodel import Field

from .base import BaseModel


class Stock(BaseModel, table=True):
    """
    Represents a stock record.

    Attributes:
        symbol (str): The stock ticker symbol.
        name (str): The name of the stock.
        price (float): The current price of the stock.
    """

    symbol: str = Field(max_length=100, index=True, unique=True)
    name: str = Field(max_length=150)
    price: float = Field(default=0.0, max_digits=10, decimal_places=2)


class StockDividend(BaseModel, table=True):
    """
    Represents a stock dividend record.

    Attributes:
        stock (Stock): The stock that issued the dividend.
        dividend_date (datetime): The date when the dividend is paid.
        adjusted_amount (float): The adjusted amount of the dividend.
        amount (float): The amount of the dividend.
        record_date (str): The date when the company records the list of shareholders eligible for the dividend.
        pay_date (str): The date when the dividend is paid.
        declaration_date (str): The date when the dividend is declared.
    """

    stock: str = Field(foreign_key="stock.symbol")

    dividend_date: Optional[datetime]
    adjusted_amount: float
    amount: float
    record_date: str
    pay_date: str
    declaration_date: str
