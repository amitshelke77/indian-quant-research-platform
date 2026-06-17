from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from backend.core.base import Base


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    strategy_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    symbol_id: Mapped[int] = mapped_column(
        ForeignKey("symbols.id"),
        index=True,
    )

    total_return: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    annual_return: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    cagr: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sharpe_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sortino_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    calmar_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    max_drawdown: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    alpha: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    beta: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    tracking_error: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    information_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    benchmark_return: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    transaction_costs: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )