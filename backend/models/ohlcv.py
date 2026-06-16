from datetime import date

from sqlalchemy import Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.base import Base


class OHLCV(Base):
    __tablename__ = "ohlcv"

    id: Mapped[int] = mapped_column(primary_key=True)

    symbol_id: Mapped[int] = mapped_column(
        ForeignKey("symbols.id"),
        index=True
    )

    trading_date: Mapped[date] = mapped_column(
        Date,
        index=True
    )

    open: Mapped[float] = mapped_column(Float)

    high: Mapped[float] = mapped_column(Float)

    low: Mapped[float] = mapped_column(Float)

    close: Mapped[float] = mapped_column(Float)

    volume: Mapped[float] = mapped_column(Float)