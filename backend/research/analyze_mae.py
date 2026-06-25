import numpy as np

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import (
    OHLCV,
)


LOOKAHEAD_DAYS = 60


def percentile(values, p):

    return round(
        np.percentile(
            values,
            p,
        ),
        2,
    )


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

        maes = []

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

            lowest_low = min(
                bar.low
                for bar in future
            )

            mae = (
                (
                    lowest_low
                    - entry
                )
                /
                entry
            ) * 100

            maes.append(mae)

        if len(maes) == 0:

            print(
                "No MAE values found."
            )

            return

        print("\n")
        print("=" * 80)
        print("MAE ANALYSIS")
        print("=" * 80)

        print(
            f"Average MAE : {np.mean(maes):.2f}%"
        )

        print(
            f"Worst MAE   : {min(maes):.2f}%"
        )

        print(
            f"5th Percentile MAE  : {percentile(maes, 5)}%"
        )

        print(
            f"10th Percentile MAE : {percentile(maes, 10)}%"
        )

        print(
            f"25th Percentile MAE : {percentile(maes, 25)}%"
        )

        print(
            f"Median MAE          : {percentile(maes, 50)}%"
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()