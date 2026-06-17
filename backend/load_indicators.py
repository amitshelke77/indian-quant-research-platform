import pandas as pd

import backend.models

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV

from backend.services.indicator_service import (
    IndicatorService,
)

from backend.repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)


def safe_float(value):

    if pd.isna(value):
        return None

    return float(value)


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
                print("No OHLCV data")
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

                    # SMA

                    sma10=safe_float(row["sma10"]),
                    sma20=safe_float(row["sma20"]),
                    sma50=safe_float(row["sma50"]),
                    sma100=safe_float(row["sma100"]),
                    sma200=safe_float(row["sma200"]),

                    # EMA

                    ema10=safe_float(row["ema10"]),
                    ema20=safe_float(row["ema20"]),
                    ema50=safe_float(row["ema50"]),
                    ema100=safe_float(row["ema100"]),
                    ema200=safe_float(row["ema200"]),

                    # RSI

                    rsi14=safe_float(row["rsi14"]),

                    # ATR

                    atr14=safe_float(row["atr14"]),

                    # MACD

                    macd=safe_float(row["macd"]),
                    macd_signal=safe_float(
                        row["macd_signal"]
                    ),
                    macd_histogram=safe_float(
                        row["macd_histogram"]
                    ),

                    # Bollinger Bands

                    bb_upper=safe_float(
                        row["bb_upper"]
                    ),
                    bb_middle=safe_float(
                        row["bb_middle"]
                    ),
                    bb_lower=safe_float(
                        row["bb_lower"]
                    ),
                )

                inserted += 1

            repo.commit()

            total_inserted += inserted

            print(
                f"Inserted {inserted}"
            )

        print("\nDone")
        print(
            f"Total Inserted: {total_inserted}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()