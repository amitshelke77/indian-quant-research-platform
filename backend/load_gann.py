import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV

from backend.services.gann_service import (
    GannService,
)

from backend.repositories.gann_repository import (
    GannRepository,
)


def safe_float(value):

    if pd.isna(value):
        return None

    return float(value)


def main():

    db = SessionLocal()

    try:

        repo = GannRepository(db)

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        service = GannService()

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
                    }
                    for r in rows
                ]
            )

            df = service.generate_gann_features(df)

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

                    swing_high_flag=int(
                        row["swing_high_flag"]
                    ),

                    swing_low_flag=int(
                        row["swing_low_flag"]
                    ),

                    swing_high_price=safe_float(
                        row["swing_high_price"]
                    ),

                    swing_low_price=safe_float(
                        row["swing_low_price"]
                    ),

                    angle_1x1=safe_float(
                        row["angle_1x1"]
                    ),

                    angle_2x1=safe_float(
                        row["angle_2x1"]
                    ),

                    angle_1x2=safe_float(
                        row["angle_1x2"]
                    ),

                    cycle_45=safe_float(
                        row["cycle_45"]
                    ),

                    cycle_90=safe_float(
                        row["cycle_90"]
                    ),

                    cycle_180=safe_float(
                        row["cycle_180"]
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