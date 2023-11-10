from .models import Stock
from typing import Optional
from sqlmodel import select


async def get_symbol(symbol, database) -> Optional[Stock]:
    result = database.execute(select(Stock).where(Stock.ticker == symbol))
    return result.scalars().all()