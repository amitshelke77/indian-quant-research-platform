import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import (
    TechnicalIndicator,
)


def main():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        results = []

        for symbol in symbols:

            rows = (
                db.query(
                    OHLCV,
                    TechnicalIndicator,
                    GannAnalysis,
                )
                .join(
                    TechnicalIndicator,
                    (
                        OHLCV.symbol_id
                        == TechnicalIndicator.symbol_id
                    )
                    &
                    (
                        OHLCV.trading_date
                        == TechnicalIndicator.trading_date
                    )
                )
                .join(
                    GannAnalysis,
                    (
                        OHLCV.symbol_id
                        == GannAnalysis.symbol_id
                    )
                    &
                    (
                        OHLCV.trading_date
                        == GannAnalysis.trading_date
                    )
                )
                .filter(
                    OHLCV.symbol_id
                    == symbol.id
                )
                .order_by(
                    OHLCV.trading_date.desc()
                )
                .limit(1)
                .all()
            )

            if not rows:
                continue

            o, t, g = rows[0]

            signal = "HOLD"

            if (
                g.trend_state == 1
                and o.close > t.ema50
            ):
                signal = "BUY"

            elif (
                g.trend_state == -1
                and o.close < t.ema50
            ):
                signal = "SELL"

            results.append(
                {
                    "Symbol": symbol.symbol,
                    "Close": round(o.close, 2),
                    "EMA50": round(t.ema50, 2),
                    "Trend": g.trend_state,
                    "Signal": signal,
                }
            )

        df = pd.DataFrame(results)

        print("\n")
        print("=" * 80)
        print("TODAY'S GANN SIGNALS")
        print("=" * 80)

        print(
            df.sort_values(
                ["Signal", "Symbol"]
            )
        )

        print("\n")
        print("=" * 80)
        print("BUY CANDIDATES")
        print("=" * 80)

        print(
            df[
                df["Signal"] == "BUY"
            ]
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()