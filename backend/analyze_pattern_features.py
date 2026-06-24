import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV


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


def main():

    pd.set_option(
        "display.max_columns",
        None,
    )

    pd.set_option(
        "display.width",
        2000,
    )

    pd.set_option(
        "display.max_rows",
        500,
    )

    db = SessionLocal()

    try:

        signals = (
            db.query(PatternSignal)
            .filter(
                PatternSignal.outcome.in_(
                    ["WIN", "LOSS"]
                )
            )
            .all()
        )

        rows = []

        for signal in signals:

            bars = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    == signal.symbol_id
                )
                .order_by(
                    OHLCV.trading_date
                )
                .all()
            )

            if len(bars) < 250:
                continue

            df = pd.DataFrame(
                [
                    {
                        "Date":
                            b.trading_date,

                        "Close":
                            b.close,

                        "High":
                            b.high,

                        "Low":
                            b.low,

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

            volume_ratio = None

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

            expected_return = (
                (
                    signal.target_price
                    -
                    signal.entry_price
                )
                /
                signal.entry_price
            ) * 100

            risk_pct = (
                (
                    signal.entry_price
                    -
                    signal.stop_loss
                )
                /
                signal.entry_price
            ) * 100

            rows.append(
                {
                    "pattern":
                        signal.pattern_name,

                    "outcome":
                        signal.outcome,

                    "rsi":
                        float(
                            row["RSI"]
                        ),

                    "volume_ratio":
                        float(
                            volume_ratio
                        )
                        if volume_ratio
                        else None,

                    "trend":
                        1
                        if row["EMA50"]
                        >
                        row["EMA200"]
                        else 0,

                    "expected_return":
                        float(
                            expected_return
                        ),

                    "risk_pct":
                        float(
                            risk_pct
                        ),
                }
            )

        result = pd.DataFrame(
            rows
        )

        print("\n")
        print("=" * 100)
        print(
            "FEATURE ANALYSIS"
        )
        print("=" * 100)

        summary = (
            result.groupby(
                [
                    "pattern",
                    "outcome",
                ]
            )
            .agg(
                avg_rsi=(
                    "rsi",
                    "mean",
                ),

                avg_volume_ratio=(
                    "volume_ratio",
                    "mean",
                ),

                trend_pct=(
                    "trend",
                    "mean",
                ),

                avg_expected_return=(
                    "expected_return",
                    "mean",
                ),

                avg_risk_pct=(
                    "risk_pct",
                    "mean",
                ),
            )
        )

        print(
            summary.round(2)
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()