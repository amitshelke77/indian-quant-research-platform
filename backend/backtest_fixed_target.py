import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV

from sqlalchemy import text


LOOKAHEAD_DAYS = 60

TARGET_PCT = 20.0


def main():

    db = SessionLocal()

    try:

        db.execute(
            text(
                """
                TRUNCATE TABLE trade_engine_results;
                """
            )
        )

        db.commit()

        signals = (
            db.query(
                PatternSignal
            )
            .all()
        )

        print(
            f"Signals: {len(signals)}"
        )

        processed = 0

        for signal in signals:

            entry = (
                signal.entry_price
            )

            stop = (
                signal.stop_loss
            )

            target = (
                entry
                * (
                    1
                    + TARGET_PCT / 100
                )
            )

            future_bars = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    ==
                    signal.symbol_id
                )
                .filter(
                    OHLCV.trading_date
                    >
                    signal.trading_date
                )
                .order_by(
                    OHLCV.trading_date
                )
                .limit(
                    LOOKAHEAD_DAYS
                )
                .all()
            )

            if not future_bars:
                continue

            outcome = None

            exit_price = None

            holding_days = 0

            for i, bar in enumerate(
                future_bars,
                start=1,
            ):

                holding_days = i

                if (
                    bar.high
                    >= target
                ):

                    outcome = "WIN"

                    exit_price = target

                    break

                if (
                    bar.low
                    <= stop
                ):

                    outcome = "LOSS"

                    exit_price = stop

                    break

            if exit_price is None:

                outcome = (
                    "TIME_EXIT"
                )

                exit_price = (
                    future_bars[-1]
                    .close
                )

            return_pct = (
                (
                    exit_price
                    - entry
                )
                /
                entry
            ) * 100

            db.execute(
                text(
                    """
                    INSERT INTO
                    trade_engine_results
                    (
                        signal_id,
                        engine_name,
                        outcome,
                        return_pct,
                        holding_days
                    )
                    VALUES
                    (
                        :signal_id,
                        :engine_name,
                        :outcome,
                        :return_pct,
                        :holding_days
                    )
                    """
                ),
                {
                    "signal_id":
                        signal.id,

                    "engine_name":
                        f"FIXED_{TARGET_PCT}",

                    "outcome":
                        outcome,

                    "return_pct":
                        float(
                            return_pct
                        ),

                    "holding_days":
                        holding_days,
                },
            )

            processed += 1

            if processed % 100 == 0:

                print(
                    f"Processed {processed}"
                )

        db.commit()

        print()
        print("=" * 60)
        print(
            f"Finished {processed}"
        )
        print("=" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()