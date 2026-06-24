from datetime import date

from sqlalchemy import (
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from backend.core.base import Base


class PatternSignal(Base):

    __tablename__ = "pattern_signals"

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "trading_date",
            "pattern_name",
            name="uq_pattern_signal",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    symbol_id: Mapped[int] = mapped_column(
        ForeignKey("symbols.id"),
        index=True,
    )

    trading_date: Mapped[date] = mapped_column(
        Date,
        index=True,
    )

    pattern_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    entry_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    stop_loss: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    target_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    rsi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    volume_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ema50: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ema200: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    outcome: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    return_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    holding_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )