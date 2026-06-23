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

        rankings = []

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

            structure = (
                latest.structure_score
                or 0
            )

            old_structure = (
                previous.structure_score
                or 0
            )

            momentum = (
                structure
                - old_structure
            )

            trend = (
                latest.trend_state
                or 0
            )

            final_score = (
                structure * 3
                +
                momentum
            )

            rankings.append(
                {
                    "Symbol":
                        symbol.symbol,

                    "Structure":
                        structure,

                    "Momentum":
                        momentum,

                    "Trend":
                        trend,

                    "FinalScore":
                        final_score,
                }
            )

        df = pd.DataFrame(
            rankings
        )

        df = df.sort_values(
            by="FinalScore",
            ascending=False,
        )

        df.insert(
            0,
            "Rank",
            range(
                1,
                len(df) + 1
            ),
        )

        df.to_csv(
            "gann_leaderboard.csv",
            index=False,
        )

        print("\n")
        print("=" * 80)
        print("TOP 25 GANN LEADERBOARD")
        print("=" * 80)

        print(
            df.head(25)
        )

        print("\n")
        print("=" * 80)
        print("BOTTOM 25")
        print("=" * 80)

        print(
            df.tail(25)
        )

        print("\n")
        print("=" * 80)
        print("TOP 10 PICKS")
        print("=" * 80)

        print(
            df.head(10)[
                [
                    "Rank",
                    "Symbol",
                    "Structure",
                    "Momentum",
                    "FinalScore",
                ]
            ]
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()