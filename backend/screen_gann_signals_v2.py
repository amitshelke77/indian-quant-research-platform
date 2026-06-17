import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import (
    TechnicalIndicator,
)


def calculate_score(
    close_price,
    ema50,
    rsi14,
    trend_state,
    swing_high_price,
):

    score = 0

    # Trend Score (40)

    if trend_state == 1:
        score += 40

    # EMA Score (30 + bonus)

    if (
        ema50 is not None
        and ema50 > 0
        and close_price > ema50
    ):

        score += 30

        ema_distance = (
            (close_price - ema50)
            / ema50
        ) * 100

        if ema_distance > 10:
            score += 10

        elif ema_distance > 5:
            score += 5

    # RSI Score (20 + bonus)

    if rsi14 is not None:

        if rsi14 >= 60:
            score += 20

        elif rsi14 >= 55:
            score += 15

        elif rsi14 >= 50:
            score += 10

        if rsi14 >= 80:
            score += 10

        elif rsi14 >= 70:
            score += 5

    # Swing Breakout Score (10)

    if (
        swing_high_price is not None
        and close_price > swing_high_price
    ):
        score += 10

    return min(score, 100)


def signal_from_score(
    score,
):

    if score >= 70:
        return "BUY"

    elif score <= 20:
        return "SELL"

    return "HOLD"


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

            score = calculate_score(
                close_price=o.close,
                ema50=t.ema50,
                rsi14=t.rsi14,
                trend_state=g.trend_state,
                swing_high_price=g.swing_high_price,
            )

            signal = signal_from_score(
                score
            )

            ema_distance = None

            if (
                t.ema50 is not None
                and t.ema50 > 0
            ):
                ema_distance = round(
                    (
                        (o.close - t.ema50)
                        / t.ema50
                    ) * 100,
                    2,
                )

            results.append(
                {
                    "Symbol": symbol.symbol,
                    "Close": round(
                        o.close,
                        2,
                    ),
                    "EMA50": round(
                        t.ema50,
                        2,
                    )
                    if t.ema50 is not None
                    else None,
                    "EMA_Diff_%": ema_distance,
                    "RSI": round(
                        t.rsi14,
                        2,
                    )
                    if t.rsi14 is not None
                    else None,
                    "Trend": g.trend_state,
                    "Score": score,
                    "Signal": signal,
                }
            )

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="Score",
            ascending=False,
        )

        print("\n")
        print("=" * 80)
        print("GANN CONFIDENCE SCREENER")
        print("=" * 80)

        print(df)

        print("\n")
        print("=" * 80)
        print("TOP BUY CANDIDATES")
        print("=" * 80)

        buys = (
            df[
                df["Signal"] == "BUY"
            ]
            .sort_values(
                by="Score",
                ascending=False,
            )
        )

        print(buys)

        print("\n")
        print("=" * 80)
        print("TOP 3")
        print("=" * 80)

        print(
            buys.head(3)
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()