from sqlalchemy.orm import Session

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol


def seed() -> None:
    db: Session = SessionLocal()

    try:
        symbol = Symbol(
            symbol="RELIANCE",
            company_name="Reliance Industries Ltd",
            exchange="NSE"
        )

        db.add(symbol)
        db.commit()

        print("Symbol Inserted")

    finally:
        db.close()


if __name__ == "__main__":
    seed()