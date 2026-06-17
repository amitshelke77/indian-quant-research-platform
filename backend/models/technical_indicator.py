from datetime import date

from sqlalchemy import (
    Date,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.base import Base


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "trading_date",
            name="uq_indicator_symbol_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    symbol_id: Mapped[int] = mapped_column(
        ForeignKey("symbols.id"),
        index=True,
    )

    trading_date: Mapped[date] = mapped_column(
        Date,
        index=True,
    )

    sma20: Mapped[float | None] = mapped_column(Float, nullable=True)
    sma50: Mapped[float | None] = mapped_column(Float, nullable=True)

    ema20: Mapped[float | None] = mapped_column(Float, nullable=True)
    ema50: Mapped[float | None] = mapped_column(Float, nullable=True)

    rsi14: Mapped[float | None] = mapped_column(Float, nullable=True)

    atr14: Mapped[float | None] = mapped_column(Float, nullable=True)

    macd: Mapped[float | None] = mapped_column(Float, nullable=True)
    macd_signal: Mapped[float | None] = mapped_column(Float, nullable=True)
    macd_histogram: Mapped[float | None] = mapped_column(Float, nullable=True)

    bb_upper: Mapped[float | None] = mapped_column(Float, nullable=True)
    bb_middle: Mapped[float | None] = mapped_column(Float, nullable=True)
    bb_lower: Mapped[float | None] = mapped_column(Float, nullable=True)