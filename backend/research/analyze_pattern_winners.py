import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV

from backend.models.symbol import Symbol


def main():

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

            bar = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    == signal.symbol_id
                )
                .filter(
                    OHLCV.trading_date
                    == signal.trading_date
                )
                .first()
            )

            symbol = (
                db.query(Symbol)
                .filter(
                    Symbol.id
                    == signal.symbol_id
                )
                .first()
            )

            if not bar:
                continue

            rows.append(
                {
                    "symbol":
                        symbol.symbol,

                    "pattern":
                        signal.pattern_name,

                    "outcome":
                        signal.outcome,

                    "entry":
                        signal.entry_price,

                    "target":
                        signal.target_price,

                    "stop":
                        signal.stop_loss,

                    "return_pct":
                        signal.return_pct,

                    "volume":
                        bar.volume,

                    "close":
                        bar.close,
                }
            )

        df = pd.DataFrame(rows)

        print("\n")
        print("=" * 80)
        print("WIN / LOSS COUNTS")
        print("=" * 80)

        print(
            df.groupby(
                ["pattern", "outcome"]
            )
            .size()
        )

        print("\n")
        print("=" * 80)
        print("AVERAGE RETURNS")
        print("=" * 80)

        print(
            df.groupby(
                ["pattern", "outcome"]
            )["return_pct"]
            .mean()
        )

        print("\n")
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        summary = (
            df.groupby(
                "pattern"
            )
            .agg(
                signals=(
                    "pattern",
                    "count",
                ),

                avg_return=(
                    "return_pct",
                    "mean",
                ),

                avg_volume=(
                    "volume",
                    "mean",
                ),
            )
        )

        print(
            summary.sort_values(
                "avg_return",
                ascending=False,
            )
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()