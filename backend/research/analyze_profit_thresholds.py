import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV


LOOKAHEAD_DAYS = 60

THRESHOLDS = [
    5,
    10,
    15,
    20,
    25,
    30,
]


def main():

    db = SessionLocal()

    try:

        signals = (
            db.query(PatternSignal)
            .filter(
                PatternSignal.pattern_name
                == "ROUNDING_BOTTOM_V5"
            )
            .all()
        )

        print(
            f"Signals: {len(signals)}"
        )

        results = {
            t: 0
            for t in THRESHOLDS
        }

        for signal in signals:

            future = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    == signal.symbol_id
                )
                .filter(
                    OHLCV.trading_date
                    > signal.trading_date
                )
                .order_by(
                    OHLCV.trading_date
                )
                .limit(
                    LOOKAHEAD_DAYS
                )
                .all()
            )

            if not future:
                continue

            entry = signal.entry_price

            highest_high = max(
                x.high
                for x in future
            )

            max_gain_pct = (
                (
                    highest_high
                    - entry
                )
                /
                entry
            ) * 100

            for threshold in THRESHOLDS:

                if (
                    max_gain_pct
                    >= threshold
                ):
                    results[
                        threshold
                    ] += 1

        print("\n")
        print("=" * 80)
        print(
            "PROFIT THRESHOLD ANALYSIS"
        )
        print("=" * 80)

        total = len(signals)

        for threshold in THRESHOLDS:

            count = results[
                threshold
            ]

            pct = (
                count
                /
                total
            ) * 100

            print(
                f"{threshold}% : "
                f"{count} / {total} "
                f"({pct:.2f}%)"
            )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()