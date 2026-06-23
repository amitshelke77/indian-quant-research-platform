import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import (
    TechnicalIndicator,
)

from backend.services.score_service import (
    ScoreService,
)

from backend.services.market_screener_service import (
    MarketScreenerService,
)


def safe_sort(records):

    df = pd.DataFrame(records)

    if df.empty:
        return df

    return df.sort_values(
        by="Score",
        ascending=False,
    )


def main():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        elite = []
        leaders = []
        mid_term = []
        breakouts = []
        watchlist = []
        avoid = []

        for symbol in symbols:

            row = (
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
                .first()
            )

            if not row:
                continue

            o, t, g = row

            score = (
                ScoreService.calculate_score(
                    close_price=o.close,
                    ema50=t.ema50,
                    rsi14=t.rsi14,
                    trend_state=g.trend_state,
                    structure_score=g.structure_score,
                    swing_high_price=g.swing_high_price,
                )
            )

            category = (
                MarketScreenerService.classify(
                    close_price=o.close,
                    ema50=t.ema50,
                    trend_state=g.trend_state,
                    structure_score=g.structure_score,
                    swing_high_price=g.swing_high_price,
                    score=score,
                )
            )

            record = {
                "Symbol": symbol.symbol,
                "Category": category,
                "Score": score,
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
                "RSI": round(
                    t.rsi14,
                    2,
                )
                if t.rsi14 is not None
                else None,
                "Trend": g.trend_state,
                "Structure": g.structure_score,
            }

            if category == "ELITE_LEADER":

                elite.append(
                    record
                )

            elif category == "LONG_TERM_LEADER":

                leaders.append(
                    record
                )

            elif category == "MID_TERM_OPPORTUNITY":

                mid_term.append(
                    record
                )

            elif category == "SHORT_TERM_BREAKOUT":

                breakouts.append(
                    record
                )

            elif category == "AVOID":

                avoid.append(
                    record
                )

            else:

                watchlist.append(
                    record
                )

        elite_df = safe_sort(
            elite
        )

        leaders_df = safe_sort(
            leaders
        )

        mid_df = safe_sort(
            mid_term
        )

        breakout_df = safe_sort(
            breakouts
        )

        watchlist_df = safe_sort(
            watchlist
        )

        avoid_df = safe_sort(
            avoid
        )

        elite_df.to_csv(
            "elite_leaders.csv",
            index=False,
        )

        leaders_df.to_csv(
            "long_term_leaders.csv",
            index=False,
        )

        mid_df.to_csv(
            "mid_term_opportunities.csv",
            index=False,
        )

        breakout_df.to_csv(
            "short_term_breakouts.csv",
            index=False,
        )

        watchlist_df.to_csv(
            "watchlist.csv",
            index=False,
        )

        avoid_df.to_csv(
            "avoid.csv",
            index=False,
        )

        print("\n")
        print("=" * 80)
        print("ELITE LEADERS")
        print("=" * 80)
        print(elite_df)

        print("\n")
        print("=" * 80)
        print("LONG TERM LEADERS")
        print("=" * 80)
        print(leaders_df)

        print("\n")
        print("=" * 80)
        print("MID TERM OPPORTUNITIES")
        print("=" * 80)
        print(mid_df)

        print("\n")
        print("=" * 80)
        print("SHORT TERM BREAKOUTS")
        print("=" * 80)
        print(breakout_df)

        print("\n")
        print("=" * 80)
        print("WATCHLIST")
        print("=" * 80)
        print(watchlist_df)

        print("\n")
        print("=" * 80)
        print("AVOID")
        print("=" * 80)
        print(avoid_df)

        print("\n")
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(
            f"Elite Leaders     : {len(elite)}"
        )

        print(
            f"Long Term Leaders : {len(leaders)}"
        )

        print(
            f"Mid Term          : {len(mid_term)}"
        )

        print(
            f"Breakouts         : {len(breakouts)}"
        )

        print(
            f"Watchlist         : {len(watchlist)}"
        )

        print(
            f"Avoid             : {len(avoid)}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()