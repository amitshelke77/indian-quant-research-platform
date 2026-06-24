import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.symbol import Symbol


def pattern_score(
    pattern_name,
):

    scores = {

        "ROUNDING_BOTTOM_V3": 100,

        "ROUNDING_BOTTOM_V2": 90,

        "ROUNDING_BOTTOM": 80,

        "DOUBLE_BOTTOM": 75,

        "CUP_HANDLE": 50,

        "BULL_FLAG": 40,
    }

    return scores.get(
        pattern_name,
        0,
    )


def main():

    pd.set_option(
        "display.max_columns",
        None,
    )

    pd.set_option(
        "display.width",
        2000,
    )

    db = SessionLocal()

    try:

        signals = (
            db.query(
                PatternSignal
            )
            .filter(
                PatternSignal.trading_date
                >= "2026-05-01"
            )
            .all()
        )

        rows = []

        for signal in signals:

            symbol = (
                db.query(Symbol)
                .filter(
                    Symbol.id
                    ==
                    signal.symbol_id
                )
                .first()
            )

            expected_return = (
                (
                    signal.target_price
                    -
                    signal.entry_price
                )
                /
                signal.entry_price
            ) * 100

            rows.append(
                {
                    "symbol":
                        symbol.symbol,

                    "pattern":
                        signal.pattern_name,

                    "trading_date":
                        signal.trading_date,

                    "score":
                        pattern_score(
                            signal.pattern_name
                        ),

                    "expected_return":
                        round(
                            expected_return,
                            2,
                        ),
                }
            )

        df = pd.DataFrame(
            rows
        )

        grouped = []

        for symbol in (
            df["symbol"]
            .unique()
        ):

            stock_df = (
                df[
                    df["symbol"]
                    ==
                    symbol
                ]
            )

            best_row = (
                stock_df
                .sort_values(
                    "score",
                    ascending=False,
                )
                .iloc[0]
            )

            unique_patterns = (
                stock_df[
                    "pattern"
                ]
                .nunique()
            )

            pattern_bonus = (
                (
                    unique_patterns
                    - 1
                )
                * 15
            )

            final_score = (
                best_row["score"]
                +
                pattern_bonus
            )

            grouped.append(
                {
                    "symbol":
                        symbol,

                    "best_pattern":
                        best_row[
                            "pattern"
                        ],

                    "patterns":
                        unique_patterns,

                    "score":
                        int(
                            final_score
                        ),

                    "expected_return":
                        best_row[
                            "expected_return"
                        ],

                    "signal_date":
                        best_row[
                            "trading_date"
                        ],
                }
            )

        result = (
            pd.DataFrame(
                grouped
            )
            .sort_values(
                [
                    "score",
                    "expected_return",
                ],
                ascending=False,
            )
        )

        print("\n")
        print("=" * 100)
        print(
            "TOP STOCKS"
        )
        print("=" * 100)

        print(
            result.head(20)
            .to_string(
                index=False
            )
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()