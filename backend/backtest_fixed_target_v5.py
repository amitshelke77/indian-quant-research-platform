import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import (
    PatternSignal,
)

from backend.models.ohlcv import OHLCV

from sqlalchemy import text


LOOKAHEAD_DAYS = 60

TAKE_PROFIT = 20.0

STOP_LOSS = 7.0


def main():

    db = SessionLocal()

    try:

        db.execute(
            text(
                """
                TRUNCATE TABLE
                trade_engine_results;
                """
            )
        )

        db.commit()

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

        processed = 0

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

            target = (
                entry
                * (
                    1
                    + TAKE_PROFIT / 100
                )
            )

            stop = (
                entry
                * (
                    1
                    - STOP_LOSS / 100
                )
            )

            outcome = None

            exit_price = None

            holding_days = 0

            for i, bar in enumerate(
                future,
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

                outcome = "TIME_EXIT"

                exit_price = (
                    future[-1].close
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
                        "V5_TP15_SL7",

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

        db.commit()

        print(
            f"Finished: {processed}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()