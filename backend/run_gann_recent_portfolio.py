import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis

from backend.services.portfolio_backtest_service_v2 import (
    PortfolioBacktestServiceV2,
)


def main():

    db = SessionLocal()

    try:

        rows = (
            db.query(
                Symbol.symbol,
                OHLCV.trading_date,
                OHLCV.close,
                GannAnalysis.recent_structure_score,
                GannAnalysis.trend_state,
            )
            .join(
                OHLCV,
                Symbol.id == OHLCV.symbol_id,
            )
            .join(
                GannAnalysis,
                (OHLCV.symbol_id == GannAnalysis.symbol_id)
                &
                (
                    OHLCV.trading_date
                    ==
                    GannAnalysis.trading_date
                )
            )
            .all()
        )

        data = []

        for r in rows:

            score = (
                r.recent_structure_score
                if r.recent_structure_score
                is not None
                else 0
            )

            data.append(
                {
                    "Date": r.trading_date,
                    "Symbol": r.symbol,
                    "Close": r.close,
                    "Score": score,
                    "Trend": r.trend_state,
                    "EMA50": r.close,
                }
            )

        df = pd.DataFrame(data)

        print("\n" + "=" * 60)
        print("DATASET")
        print("=" * 60)
        print("Rows:", len(df))
        print(
            "Symbols:",
            df["Symbol"].nunique(),
        )

        results = (
            PortfolioBacktestServiceV2()
            .run(
                scores_df=df,
                top_n=10,
            )
        )

        print("\n" + "=" * 60)
        print("RECENT GANN RESULTS")
        print("=" * 60)

        for k, v in results.items():

            if k != "equity_curve":

                print(
                    f"{k}: {v}"
                )

        print("\n" + "=" * 60)
        print("FINAL EQUITY")
        print("=" * 60)

        print(
            results[
                "equity_curve"
            ].tail()
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()
    