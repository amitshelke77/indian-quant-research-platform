import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.pattern_signal import (
    PatternSignal,
)


LOOKAHEAD_DAYS = 60


def main():

    db = SessionLocal()

    try:

        signals = (
            db.query(PatternSignal)
            .filter(
                PatternSignal.outcome == None
            )
            .all()
        )

        print(
            f"Signals found: {len(signals)}"
        )

        updated = 0

        for signal in signals:

            future_bars = (
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

            if len(future_bars) == 0:
                continue

            outcome = "OPEN"

            exit_price = None

            holding_days = 0

            for i, bar in enumerate(
                future_bars,
                start=1,
            ):

                holding_days = i

                if (
                    bar.high
                    >= signal.target_price
                ):

                    outcome = "WIN"

                    exit_price = (
                        signal.target_price
                    )

                    break

                if (
                    bar.low
                    <= signal.stop_loss
                ):

                    outcome = "LOSS"

                    exit_price = (
                        signal.stop_loss
                    )

                    break

            if exit_price is None:

                outcome = "TIME_EXIT"

                exit_price = (
                    future_bars[-1].close
                )

            return_pct = (
                (
                    exit_price
                    - signal.entry_price
                )
                /
                signal.entry_price
            ) * 100

            signal.outcome = outcome

            signal.return_pct = float(
                return_pct
            )

            signal.holding_days = (
                holding_days
            )

            updated += 1

            if updated % 100 == 0:

                print(
                    f"Processed {updated}"
                )

        db.commit()

        print("\n")
        print("=" * 60)
        print(
            f"UPDATED {updated}"
        )
        print("=" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()