#!/usr/bin/env python3
from datetime import date
from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import Float, func, select, cast
from db.client import get_session
from typing import Annotated
from fastapi import Depends
import io

from sqlalchemy.ext.asyncio import AsyncSession

from models import Ticker


app = FastAPI()

# requires latest python to annotate dep inject
Session = Annotated[AsyncSession, Depends(get_session)]


@app.get("/")
async def root():
    return {"message": "Hello World"}


class PaginationData(BaseModel):
    """Encapsulate pagination data to make less ugly"""

    count: int
    page: int
    limit: int
    pages: int


@app.get("/api/financial_data")
async def get_stock_data(
    session: Session,
    limit: int = Query(5, ge=1),
    page: int = Query(1, ge=1),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    symbol: str | None = Query(None),
):
    errors = io.StringIO()

    # make and get query
    query = select(Ticker)
    if start_date:
        query = query.where(Ticker.date >= start_date.isoformat())
    if end_date:
        query = query.where(Ticker.date <= end_date.isoformat())
    if symbol:
        query = query.where(Ticker.symbol == symbol)
    res = await session.execute(query)
    count = len(res.scalars().all())

    # continue query to paginate
    offset = (page - 1) * limit
    query = query.limit(limit).offset(offset)
    res = await session.execute(query)
    data = res.scalars().all()

    pagination = PaginationData(
        count=count, page=page, limit=limit, pages=(
            (count + limit - 1) // limit)
    )

    # handle errors
    symbol_count_query = select(Ticker.symbol).where(
        Ticker.symbol == symbol).distinct()
    symbol_count_result = await session.execute(symbol_count_query)
    symbol_count = symbol_count_result.scalars().all()

    if not symbol:
        errors.write("No symbol given, ")
    if not start_date:
        errors.write("No start_date given, ")
    if not end_date:
        errors.write("No end_date given, ")
    if not symbol_count:
        errors.write("Symbol not found, ")
    if not symbol_count and count <= 0:
        errors.write("No data found for date range, ")

    # create result
    result = {
        "data": data,
        "pagination": pagination.dict(),
        "info": {"error": errors.getvalue()},
    }

    return result


@app.get("/api/statistics")
async def get_stock_stats(
    session: Session,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    symbol: str | None = Query(None),
):
    errors = io.StringIO()

    # make and get query
    query = select(
        cast(func.avg(Ticker.open_price), Float).label(
            "average_daily_open_price"),
        cast(func.avg(Ticker.close_price), Float).label(
            "average_daily_close_price"),
        cast(func.avg(Ticker.volume), Float).label("average_daily_volume"),
    ).where(Ticker.symbol == symbol)
    if start_date:
        query = query.where(Ticker.date >= start_date.isoformat())
    if end_date:
        query = query.where(Ticker.date <= end_date.isoformat())
    data = await session.execute(query)
    averages = data.first()

    # handle errors
    symbol_count_query = select(Ticker.symbol).where(
        Ticker.symbol == symbol).distinct()
    symbol_count_result = await session.execute(symbol_count_query)
    symbol_count = symbol_count_result.scalars().all()

    if None in averages:
        errors.write("No average data found for the date range, ")
    if not symbol_count:
        errors.write("Symbol not found, ")
    if not symbol:
        errors.write("No symbol given, ")
    if not start_date:
        errors.write("No start_date given, ")
    if not end_date:
        errors.write("No end_date given, ")

    # create result
    result = {
        "data": {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "average_daily_open_price": averages[0] or 0,
            "average_daily_close_price": averages[1] or 0,
            "average_daily_volume": averages[2] or 0,
        },
        "errors": errors.getvalue(),
    }
    return result
