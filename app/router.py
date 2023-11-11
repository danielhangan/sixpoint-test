from fastapi import Depends, APIRouter, BackgroundTasks
from typing import List
from sqlmodel import Session
from . import validator, services, models
import db

router = APIRouter(tags=["Stocks"], prefix="/stocks")


@router.get("/{symbol}", response_model=List[models.StockBase])
async def get_symbol(
    symbol: str,
    background_tasks: BackgroundTasks,
    database: Session = Depends(db.get_session),
):
    if len(symbol) < 3:
        return {"detail": "Symbol must be at least 3 characters long."}

    # Upper case symbol
    symbol = symbol.upper()

    # check if symbol exists in database
    symmbol_db_data = await validator.get_symbol(symbol, database)

    # fecth symbol data
    symbol_api_data = await services.get_symbol_data(symbol)

    if not symmbol_db_data:
        background_tasks.add_task(
            services.insert_symbol_data, symbol_api_data, database
        )
    else:
        new_data = services.get_new_data(symbol_api_data, symmbol_db_data)
        if new_data:
            background_tasks.add_task(services.insert_symbol_data, new_data, database)

    return symbol_api_data


@router.get("/symbols/unique")
async def get_all_symbols(database: Session = Depends(db.get_session)):
    return await services.get_unique_symbols(database)


# suggestions:
# function that gets all symbol in database and updates data them every day. Run with a cron job.
# Cache the results with fastapi-redis
