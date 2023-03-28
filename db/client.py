#!/usr/bin/env python3
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import Env
from typing import AsyncGenerator

engine = create_async_engine(
    Env.DATABASE_CONNECTIONSTRING, echo=True, future=True)


def get_session_base() -> async_sessionmaker[AsyncSession]:
    """For scripting"""
    async_session = async_sessionmaker(
        engine,
        # expire_on_commit=False
    )
    return async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_session_base()
    async with async_session() as session:
        yield session
