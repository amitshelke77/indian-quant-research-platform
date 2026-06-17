import sys

import backend.models

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV

from backend.core.database import SessionLocal
from backend.repositories.ohlcv_repository import OHLCVRepository
from backend.services.market_data_service import MarketDataService


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.load_symbol SYMBOL")
        return

    symbol = sys.argv[1].upper()

    db = SessionLocal()

    try:
        symbol_row = (
            db.query(Symbol)
            .filter(Symbol.symbol == symbol)
            .first()
        )

        if not symbol_row:
            print(f"Symbol '{symbol}' not found in database.")
            print("Add it to the symbols table first.")
            return

        repository = OHLCVRepository(db)
        market_data = MarketDataService()

        data = market_data.download_symbol(symbol)

        if data.empty:
            print(f"No data returned for {symbol}")
            return

        inserted = 0
        skipped = 0

        for _, row in data.iterrows():

            trading_date = row["Date"].date()

            if repository.exists(
                symbol_row.id,
                trading_date,
            ):
                skipped += 1
                continue

            repository.insert(
                symbol_id=symbol_row.id,
                trading_date=trading_date,
                open_price=float(row["Open"]),
                high_price=float(row["High"]),
                low_price=float(row["Low"]),
                close_price=float(row["Close"]),
                volume=float(row["Volume"]),
            )

            inserted += 1

        repository.commit()

        print("\nLoad Complete")
        print(f"Symbol   : {symbol}")
        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()