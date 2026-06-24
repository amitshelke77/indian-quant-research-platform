from datetime import date

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

        "ROUNDING_BOTTOM_V2": 95,

        "ROUNDING_BOTTOM": 85,

        "DOUBLE_BOTTOM": 80,

        "CUP_HANDLE": 50,

        "BULL_FLAG": 40,
    }

    return scores.get(
        pattern_name,
        0,
    )


def recency_bonus(
    signal_date,
):

    days_old = (
        date.today()
        -
        signal_date
    ).days

    if days_old <= 5:
        return 30

    if days_old <= 10:
        return 20

    if days_old <= 20:
        return 10

    return 0


def expected_return_bonus(
    expected_return,
):

    if expected_return >= 40:
        return 40

    if expected_return >= 30:
        return 30

    if expected_return >= 20:
        return 20

    if expected_return >= 10:
        return 10

    return 0


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

                    "expected_return":
                        round(
                            expected_return,
                            2,
                        ),

                    "pattern_score":
                        pattern_score(
                            signal.pattern_name
                        ),

                    "recency_bonus":
                        recency_bonus(
                            signal.trading_date
                        ),

                    "return_bonus":
                        expected_return_bonus(
                            expected_return
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
                    [
                        "pattern_score",
                        "expected_return",
                    ],
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

            agreement_bonus = (
                (
                    unique_patterns
                    - 1
                )
                * 15
            )

            final_score = (

                best_row[
                    "pattern_score"
                ]

                +

                best_row[
                    "recency_bonus"
                ]

                +

                best_row[
                    "return_bonus"
                ]

                +

                agreement_bonus
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

                    "expected_return":
                        best_row[
                            "expected_return"
                        ],

                    "score":
                        int(
                            final_score
                        ),

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
            "TOP STOCKS V2"
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