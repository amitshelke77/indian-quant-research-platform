import pandas as pd

import backend.models

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.services.indicator_service import IndicatorService
from backend.repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)


def main():

    db = SessionLocal()

    try:

        repo = TechnicalIndicatorRepository(db)

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        service = IndicatorService()

        total_inserted = 0

        for symbol in symbols:

            print(f"\nProcessing {symbol.symbol}")

            rows = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id == symbol.id
                )
                .order_by(
                    OHLCV.trading_date
                )
                .all()
            )

            if not rows:
                continue

            df = pd.DataFrame(
                [
                    {
                        "Date": r.trading_date,
                        "Open": r.open,
                        "High": r.high,
                        "Low": r.low,
                        "Close": r.close,
                        "Volume": r.volume,
                    }
                    for r in rows
                ]
            )

            df = service.generate_indicators(df)

            inserted = 0

            for _, row in df.iterrows():

                if repo.exists(
                    symbol.id,
                    row["Date"],
                ):
                    continue

                repo.insert(
                    symbol_id=symbol.id,
                    trading_date=row["Date"],
                    sma20=None if pd.isna(row["sma20"]) else float(row["sma20"]),
                    sma50=None if pd.isna(row["sma50"]) else float(row["sma50"]),
                    ema20=None if pd.isna(row["ema20"]) else float(row["ema20"]),
                    ema50=None if pd.isna(row["ema50"]) else float(row["ema50"]),
                    rsi14=None if pd.isna(row["rsi14"]) else float(row["rsi14"]),
                    atr14=None if pd.isna(row["atr14"]) else float(row["atr14"]),
                    macd=None if pd.isna(row["macd"]) else float(row["macd"]),
                    macd_signal=None if pd.isna(row["macd_signal"]) else float(row["macd_signal"]),
                    macd_histogram=None if pd.isna(row["macd_histogram"]) else float(row["macd_histogram"]),
                    bb_upper=None if pd.isna(row["bb_upper"]) else float(row["bb_upper"]),
                    bb_middle=None if pd.isna(row["bb_middle"]) else float(row["bb_middle"]),
                    bb_lower=None if pd.isna(row["bb_lower"]) else float(row["bb_lower"]),
                )

                inserted += 1

            repo.commit()

            total_inserted += inserted

            print(f"Inserted {inserted}")

        print("\nDone")
        print(f"Total Inserted: {total_inserted}")

    finally:
        db.close()


if __name__ == "__main__":
    main()