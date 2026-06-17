import backend.models

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV

from backend.core.database import SessionLocal
from backend.repositories.ohlcv_repository import OHLCVRepository
from backend.services.market_data_service import MarketDataService

SYMBOL_ID = 1  # update if your RELIANCE id is different


def main():
    db = SessionLocal()

    try:
        repository = OHLCVRepository(db)
        market_data = MarketDataService()

        data = market_data.download_symbol("RELIANCE")

        inserted = 0
        skipped = 0

        for _, row in data.iterrows():

            trading_date = row["Date"].date()

            if repository.exists(
                SYMBOL_ID,
                trading_date,
            ):
                skipped += 1
                continue

            repository.insert(
                symbol_id=SYMBOL_ID,
                trading_date=trading_date,
                open_price=float(row["Open"]),
                high_price=float(row["High"]),
                low_price=float(row["Low"]),
                close_price=float(row["Close"]),
                volume=float(row["Volume"]),
            )

            inserted += 1

        repository.commit()

        print(f"Inserted: {inserted}")
        print(f"Skipped: {skipped}")

    finally:
        db.close()


if __name__ == "__main__":
    main()