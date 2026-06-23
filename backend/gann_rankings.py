import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import (
    GannAnalysis,
)


def safe_sort(records):

    df = pd.DataFrame(records)

    if df.empty:
        return df

    return df.sort_values(
        by=[
            "Structure",
            "Trend",
        ],
        ascending=False,
    )


def classify(
    trend_state,
    structure_score,
):

    structure_score = (
        structure_score
        if structure_score is not None
        else 0
    )

    if (
        trend_state == 1
        and structure_score >= 30
    ):
        return "LONG_TERM_LEADER"

    if (
        trend_state == 1
        and structure_score >= 10
    ):
        return "EMERGING_LEADER"

    if trend_state == 0:
        return "NEUTRAL"

    if trend_state == -1:
        return "DOWNTREND"

    return "UNKNOWN"


def main():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        leaders = []
        emerging = []
        neutral = []
        downtrend = []

        for symbol in symbols:

            row = (
                db.query(
                    OHLCV,
                    GannAnalysis,
                )
                .join(
                    GannAnalysis,
                    (
                        OHLCV.symbol_id
                        ==
                        GannAnalysis.symbol_id
                    )
                    &
                    (
                        OHLCV.trading_date
                        ==
                        GannAnalysis.trading_date
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

            o, g = row

            category = classify(
                g.trend_state,
                g.structure_score,
            )

            record = {
                "Symbol":
                    symbol.symbol,

                "Close":
                    round(
                        o.close,
                        2,
                    ),

                "Trend":
                    g.trend_state,

                "Structure":
                    g.structure_score,

                "Category":
                    category,
            }

            if (
                category
                == "LONG_TERM_LEADER"
            ):
                leaders.append(
                    record
                )

            elif (
                category
                == "EMERGING_LEADER"
            ):
                emerging.append(
                    record
                )

            elif (
                category
                == "NEUTRAL"
            ):
                neutral.append(
                    record
                )

            elif (
                category
                == "DOWNTREND"
            ):
                downtrend.append(
                    record
                )

        leaders_df = safe_sort(
            leaders
        )

        emerging_df = safe_sort(
            emerging
        )

        neutral_df = safe_sort(
            neutral
        )

        downtrend_df = safe_sort(
            downtrend
        )

        leaders_df.to_csv(
            "gann_long_term_leaders.csv",
            index=False,
        )

        emerging_df.to_csv(
            "gann_emerging_leaders.csv",
            index=False,
        )

        neutral_df.to_csv(
            "gann_neutral.csv",
            index=False,
        )

        downtrend_df.to_csv(
            "gann_downtrend.csv",
            index=False,
        )

        print("\n")
        print("=" * 80)
        print("TOP 20 GANN LEADERS")
        print("=" * 80)

        print(
            leaders_df.head(20)
        )

        print("\n")
        print("=" * 80)
        print("EMERGING LEADERS")
        print("=" * 80)

        print(
            emerging_df.head(20)
        )

        print("\n")
        print("=" * 80)
        print("DOWNTRENDS")
        print("=" * 80)

        print(
            downtrend_df.head(20)
        )

        print("\n")
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(
            f"Long Term Leaders : {len(leaders)}"
        )

        print(
            f"Emerging Leaders  : {len(emerging)}"
        )

        print(
            f"Neutral           : {len(neutral)}"
        )

        print(
            f"Downtrends        : {len(downtrend)}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()