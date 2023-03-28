#!/usr/bin/env python3
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, ForeignKey, String, DateTime, func, Text, UniqueConstraint
from models.base import Base


class Ticker(Base):
    __tablename__ = "financial_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String())
    date: Mapped[str] = mapped_column(DateTime(), index=True)
    open_price: Mapped[float] = mapped_column(Float(precision=2))
    close_price: Mapped[float] = mapped_column(Float(precision=2))
    volume: Mapped[str] = mapped_column(String())

    __table_args__ = (UniqueConstraint(
        "symbol", "date", name="symbol_date_uc"),)

    def __repr__(self) -> str:
        return f"{self.__name__}(id={repr(self.id)}, symbol={repr(self.symbol)}, date={repr(self.date)}, open_price={repr(self.open_price)}, close_price={repr(self.close_price)}, volume={repr(self.volume)})"
