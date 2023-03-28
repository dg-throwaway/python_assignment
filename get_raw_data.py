#!/usr/bin/env python3
import datetime
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from config import Env
from db.client import get_session_base
from models import Ticker


async def insert_data(session: AsyncSession, symbol: str, date: str, data: dict):
    """Insert data into database action"""
    open = data.get("1. open")
    close = data.get("4. close")
    volume = data.get("6. volume")
    parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    if open and close and volume:
        ticker = Ticker(
            symbol=symbol,
            date=parsed_date,
            open_price=open,
            close_price=close,
            volume=volume,
        )
        session.add(ticker)
        await session.commit()
        await session.refresh(ticker)
    else:
        raise Exception(
            "ERROR: Could not get open, close, or volume from API.")


async def get_data(symbol: str, days_back: int):
    """Gets"""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={Env.VANTAGE_API_KEY}&datatype=json"
    res = httpx.get(url)
    data = res.json()
    daily_data = data.get("Time Series (Daily)")

    if daily_data:
        async_session = get_session_base()
        async with async_session() as session:
            for date in sorted(daily_data.keys(), reverse=True)[:days_back]:
                await insert_data(session, symbol, date, daily_data[date])
    else:
        api_err = data.get("Error Message")
        if api_err:
            raise Exception(api_err)
        raise Exception("ERROR: Something went wrong with grabbing from API.")


if __name__ == "__main__":
    symbols = ["IBM", "AAPL"]
    days_back = 14
    for symbol in symbols:
        asyncio.run(get_data(symbol, days_back))
