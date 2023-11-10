from sqlmodel import SQLModel, Field
from datetime import date


class StockBase(SQLModel):
    date: date
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class Stock(StockBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
