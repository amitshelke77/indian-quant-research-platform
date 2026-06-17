from sqlalchemy.orm import Session

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol


SYMBOLS = [
    ("RELIANCE", "Reliance Industries Ltd", "NSE"),
    ("TCS", "Tata Consultancy Services Ltd", "NSE"),
    ("INFY", "Infosys Ltd", "NSE"),
    ("HDFCBANK", "HDFC Bank Ltd", "NSE"),
    ("ICICIBANK", "ICICI Bank Ltd", "NSE"),
    ("SBIN", "State Bank of India", "NSE"),
    ("LT", "Larsen & Toubro Ltd", "NSE"),
    ("ITC", "ITC Ltd", "NSE"),
    ("BHARTIARTL", "Bharti Airtel Ltd", "NSE"),
    ("KOTAKBANK", "Kotak Mahindra Bank Ltd", "NSE"),
]


def seed() -> None:
    db: Session = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for symbol_code, company_name, exchange in SYMBOLS:

            existing = (
                db.query(Symbol)
                .filter(Symbol.symbol == symbol_code)
                .first()
            )

            if existing:
                skipped += 1
                continue

            symbol = Symbol(
                symbol=symbol_code,
                company_name=company_name,
                exchange=exchange,
            )

            db.add(symbol)
            inserted += 1

        db.commit()

        print(f"Inserted: {inserted}")
        print(f"Skipped : {skipped}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()