from datetime import date

from sqlalchemy import (
    Date,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from backend.core.base import Base


class GannAnalysis(Base):

    __tablename__ = "gann_analysis"

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "trading_date",
            name="uq_gann_symbol_date",
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

    gann_angle_1x1: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    gann_angle_2x1: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    gann_angle_1x2: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    square_of_9_level: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    time_cycle_45: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    time_cycle_90: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    time_cycle_180: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )