import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.gann_analysis import (
    GannAnalysis,
)


LOOKBACK_DAYS = 20


def main():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        results = []

        for symbol in symbols:

            rows = (
                db.query(
                    GannAnalysis
                )
                .filter(
                    GannAnalysis.symbol_id
                    == symbol.id
                )
                .order_by(
                    GannAnalysis.trading_date
                )
                .all()
            )

            if len(rows) < LOOKBACK_DAYS:
                continue

            latest = rows[-1]

            previous = rows[
                -LOOKBACK_DAYS
            ]

            current_structure = (
                latest.structure_score
                or 0
            )

            old_structure = (
                previous.structure_score
                or 0
            )

            momentum = (
                current_structure
                - old_structure
            )

            results.append(
                {
                    "Symbol":
                        symbol.symbol,

                    "Current":
                        current_structure,

                    "Previous":
                        old_structure,

                    "Momentum":
                        momentum,

                    "Trend":
                        latest.trend_state,
                }
            )

        df = pd.DataFrame(
            results
        )

        df = df.sort_values(
            by="Momentum",
            ascending=False,
        )

        df.to_csv(
            "gann_structure_momentum.csv",
            index=False,
        )

        print("\n")
        print("=" * 80)
        print("TOP 20 IMPROVING")
        print("=" * 80)

        print(
            df.head(20)
        )

        print("\n")
        print("=" * 80)
        print("TOP 20 WEAKENING")
        print("=" * 80)

        print(
            df.tail(20)
        )

        print("\n")
        print("=" * 80)
        print("BIGGEST WINNER")
        print("=" * 80)

        print(
            df.iloc[0]
        )

        print("\n")
        print("=" * 80)
        print("BIGGEST LOSER")
        print("=" * 80)

        print(
            df.iloc[-1]
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()