import pandas as pd

import backend.models

from backend.core.database import SessionLocal
from backend.models.pattern_signal import PatternSignal
from backend.models.ohlcv import OHLCV

from sqlalchemy import text

LOOKAHEAD_DAYS = 60


def atr(df, period=14):

    high_low = df["High"] - df["Low"]

    high_close = (
        df["High"] - df["Close"].shift()
    ).abs()

    low_close = (
        df["Low"] - df["Close"].shift()
    ).abs()

    tr = pd.concat(
        [
            high_low,
            high_close,
            low_close,
        ],
        axis=1,
    ).max(axis=1)

    return tr.rolling(period).mean()


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

            history = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    == signal.symbol_id
                )
                .filter(
                    OHLCV.trading_date
                    <= signal.trading_date
                )
                .order_by(
                    OHLCV.trading_date
                )
                .all()
            )

            if len(history) < 30:
                continue

            hist_df = pd.DataFrame(
                [
                    {
                        "High": x.high,
                        "Low": x.low,
                        "Close": x.close,
                    }
                    for x in history
                ]
            )

            hist_df["ATR"] = atr(hist_df)

            atr_value = (
                hist_df["ATR"]
                .iloc[-1]
            )

            if pd.isna(atr_value):
                continue

            entry = signal.entry_price

            stop = (
                entry
                - (2 * atr_value)
            )

            risk = (
                entry
                - stop
            )

            target = (
                entry
                + (risk * 2)
            )

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
                    INSERT INTO trade_engine_results
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
                    "signal_id": signal.id,
                    "engine_name": "ATR_2R",
                    "outcome": outcome,
                    "return_pct": float(
                        return_pct
                    ),
                    "holding_days": holding_days,
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