import backend.models

from sqlalchemy import text

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
            .all()
        )

        print(
            f"Signals: {len(signals)}"
        )

        processed = 0

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

            entry = (
                signal.entry_price
            )

            stop = (
                signal.stop_loss
            )

            target = (
                signal.target_price
            )

            risk = (
                entry
                - stop
            )

            if risk <= 0:
                continue

            breakeven_trigger = entry + (risk * 0.5)

            moved_to_breakeven = False

            outcome = None

            exit_price = None

            holding_days = 0

            for i, bar in enumerate(
                future_bars,
                start=1,
            ):

                holding_days = i

                #
                # Move stop to entry
                #
                if (
                    not moved_to_breakeven
                    and
                    bar.high
                    >= breakeven_trigger
                ):

                    stop = entry

                    moved_to_breakeven = True

                #
                # Target hit
                #
                if (
                    bar.high
                    >= target
                ):

                    outcome = "WIN"

                    exit_price = target

                    break

                #
                # Stop hit
                #
                if (
                    bar.low
                    <= stop
                ):

                    if moved_to_breakeven:

                        outcome = (
                            "BREAKEVEN"
                        )

                    else:

                        outcome = (
                            "LOSS"
                        )

                    exit_price = stop

                    break

            if exit_price is None:

                outcome = "TIME_EXIT"

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
                        "BREAKEVEN_V1",

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

        print("\n")
        print("=" * 60)
        print(
            f"FINISHED {processed}"
        )
        print("=" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()