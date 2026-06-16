from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.base import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id: Mapped[int] = mapped_column(primary_key=True)

    symbol: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True
    )

    company_name: Mapped[str] = mapped_column(
        String(255)
    )

    exchange: Mapped[str] = mapped_column(
        String(20)
    )