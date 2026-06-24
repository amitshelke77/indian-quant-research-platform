import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV

from backend.models.symbol import Symbol


def calculate_rsi(
    close,
    period=14,
):

    delta = close.diff()

    gain = (
        delta.where(
            delta > 0,
            0,
        )
        .rolling(period)
        .mean()
    )

    loss = (
        -delta.where(
            delta < 0,
            0,
        )
        .rolling(period)
        .mean()
    )

    rs = gain / loss

    return (
        100
        -
        (
            100
            /
            (
                1 + rs
            )
        )
    )


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
                >=
                (
                    pd.Timestamp.today()
                    -
                    pd.Timedelta(
                        days=30
                    )
                )
            )
            .all()
        )

        ranked = []

        for signal in signals:

            bars = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    ==
                    signal.symbol_id
                )
                .order_by(
                    OHLCV.trading_date
                )
                .all()
            )

            if len(bars) < 250:
                continue

            symbol = (
                db.query(Symbol)
                .filter(
                    Symbol.id
                    ==
                    signal.symbol_id
                )
                .first()
            )

            df = pd.DataFrame(
                [
                    {
                        "Date":
                            b.trading_date,

                        "Close":
                            b.close,

                        "Volume":
                            b.volume,
                    }
                    for b in bars
                ]
            )

            df["EMA50"] = (
                df["Close"]
                .ewm(span=50)
                .mean()
            )

            df["EMA200"] = (
                df["Close"]
                .ewm(span=200)
                .mean()
            )

            df["RSI"] = (
                calculate_rsi(
                    df["Close"]
                )
            )

            df["VOL20"] = (
                df["Volume"]
                .rolling(20)
                .mean()
            )

            row = df[
                df["Date"]
                ==
                signal.trading_date
            ]

            if len(row) == 0:
                continue

            row = row.iloc[0]

            score = (
                pattern_score(
                    signal.pattern_name
                )
            )

            if (
                pd.notna(
                    row["VOL20"]
                )
                and
                row["VOL20"] > 0
            ):

                volume_ratio = (
                    row["Volume"]
                    /
                    row["VOL20"]
                )

                if volume_ratio > 2:

                    score += 20

                elif volume_ratio > 1.5:

                    score += 10

            else:

                volume_ratio = 0

            if row["RSI"] > 75:

                score += 15

            elif row["RSI"] > 70:

                score += 10

            elif row["RSI"] > 60:

                score += 5

            if (
                row["EMA50"]
                >
                row["EMA200"]
            ):

                score += 10

            expected_return = (
                (
                    signal.target_price
                    -
                    signal.entry_price
                )
                /
                signal.entry_price
            ) * 100

            if expected_return > 30:

                score += 25

            elif expected_return > 20:

                score += 15

            elif expected_return > 10:

                score += 5

            ranked.append(
                {
                    "symbol":
                        symbol.symbol,

                    "pattern":
                        signal.pattern_name,

                    "score":
                        round(
                            score,
                            2,
                        ),

                    "rsi":
                        round(
                            float(
                                row["RSI"]
                            ),
                            2,
                        ),

                    "volume_ratio":
                        round(
                            float(
                                volume_ratio
                            ),
                            2,
                        ),

                    "expected_return":
                        round(
                            expected_return,
                            2,
                        ),
                }
            )

        result = (
            pd.DataFrame(
                ranked
            )
            .sort_values(
                "score",
                ascending=False,
            )
        )

        print("\n")
        print("=" * 100)
        print("TOP SIGNALS")
        print("=" * 100)

        print(
            result.head(20)
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()