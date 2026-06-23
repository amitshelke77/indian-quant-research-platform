from datetime import date

from sqlalchemy import (
    Date,
    Float,
    ForeignKey,
    Integer,
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

    # Swing flags

    swing_high_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    swing_low_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Swing prices

    swing_high_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    swing_low_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Market Structure

    higher_high_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    higher_low_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    lower_high_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    lower_low_flag: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Trend State
    # 1 = Uptrend
    # 0 = Sideways
    # -1 = Downtrend

    trend_state: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    
    structure_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    recent_structure_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
  )
   

    # Gann Angles

    angle_1x1: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    angle_2x1: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    angle_1x2: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Time Cycles

    cycle_45: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    cycle_90: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    cycle_180: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )