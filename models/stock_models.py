from datetime import datetime
from typing import Optional

from sqlmodel import Field

from .base import BaseModel


class Stock(BaseModel):
    """
    Represents a stock dividend record.

    Attributes:
        symbol (str): The stock ticker symbol.
        dividend_date (datetime): The date when the dividend is paid.
        adjusted_amount (float): The adjusted amount of the dividend.
        amount (float): The amount of the dividend.
        record_date (str): The date when the company records the list of shareholders eligible for the dividend.
        pay_date (str): The date when the dividend is paid.
        declaration_date (str): The date when the dividend is declared.
    """

    symbol: str = Field(max_length=100, index=True)
    dividend_date: Optional[datetime]
    adjusted_amount: float
    amount: float
    record_date: str
    pay_date: str
    declaration_date: str
