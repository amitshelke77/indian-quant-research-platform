import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV


LOOKAHEAD_DAYS = 60


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

        results = []

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

            lowest_low = min(
                x.low
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

            max_drawdown_pct = (
                (
                    lowest_low
                    - entry
                )
                /
                entry
            ) * 100

            results.append(
                {
                    "signal_id":
                        signal.id,

                    "max_gain_pct":
                        max_gain_pct,

                    "max_drawdown_pct":
                        max_drawdown_pct,

                    "target_pct":
                        (
                            (
                                signal.target_price
                                - entry
                            )
                            /
                            entry
                        )
                        * 100,
                }
            )

        df = pd.DataFrame(results)

        print("\n")
        print("=" * 80)

        print(
            "AVERAGE MAX GAIN:"
        )

        print(
            round(
                df[
                    "max_gain_pct"
                ].mean(),
                2,
            )
        )

        print("\n")

        print(
            "AVERAGE MAX DRAWDOWN:"
        )

        print(
            round(
                df[
                    "max_drawdown_pct"
                ].mean(),
                2,
            )
        )

        print("\n")

        print(
            "AVERAGE TARGET:"
        )

        print(
            round(
                df[
                    "target_pct"
                ].mean(),
                2,
            )
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()