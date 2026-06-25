import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV


LOOKAHEAD_DAYS = 60


BUCKETS = [
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

        counts = {
            x: 0
            for x in BUCKETS
        }

        over_30 = 0

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

            mfe = (
                (
                    highest_high
                    - entry
                )
                /
                entry
            ) * 100

            for bucket in BUCKETS:

                if mfe >= bucket:
                    counts[bucket] += 1

            if mfe >= 30:
                over_30 += 1

        total = len(signals)

        print("\n")
        print("=" * 80)
        print("MFE DISTRIBUTION")
        print("=" * 80)

        for bucket in BUCKETS:

            pct = (
                counts[bucket]
                / total
            ) * 100

            print(
                f"{bucket}% : "
                f"{counts[bucket]}"
                f"/{total}"
                f" ({pct:.2f}%)"
            )

        print(
            f"30%+ : "
            f"{over_30}/{total}"
            f" ({(over_30/total)*100:.2f}%)"
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()