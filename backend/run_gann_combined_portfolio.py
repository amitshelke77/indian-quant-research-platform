import pandas as pd

import backend.models

from backend.core.database import (
    SessionLocal,
)

from backend.models.symbol import (
    Symbol,
)

from backend.models.ohlcv import (
    OHLCV,
)

from backend.models.gann_analysis import (
    GannAnalysis,
)

from backend.services.portfolio_backtest_service_v2 import (
    PortfolioBacktestServiceV2,
)

from backend.services.combined_score_service import (
    CombinedScoreService,
)


def main():

    db = SessionLocal()

    try:

        rows = (
            db.query(
                Symbol,
                OHLCV,
                GannAnalysis,
            )
            .join(
                OHLCV,
                Symbol.id
                == OHLCV.symbol_id,
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
            .all()
        )

        data = []

        for (
            symbol,
            ohlcv,
            gann,
        ) in rows:

            score = (
                CombinedScoreService.calculate(
                    gann.structure_score,
                    gann.recent_structure_score,
                )
            )

            data.append(
                {
                    "Date":
                        ohlcv.trading_date,

                    "Symbol":
                        symbol.symbol,

                    "Close":
                        ohlcv.close,

                    "Score":
                        score,

                    "Trend":
                        gann.trend_state,

                    "EMA50":
                        0,
                }
            )

        scores_df = pd.DataFrame(
            data
        )

        print()
        print("=" * 60)
        print("DATASET")
        print("=" * 60)
        print(
            f"Rows: {len(scores_df)}"
        )
        print(
            f"Symbols: {scores_df['Symbol'].nunique()}"
        )

        results = (
            PortfolioBacktestServiceV2()
            .run(
                scores_df,
                top_n=10,
            )
        )

        print()
        print("=" * 60)
        print("COMBINED GANN RESULTS")
        print("=" * 60)

        for k, v in (
            results.items()
        ):

            if (
                k
                == "equity_curve"
            ):
                continue

            print(
                f"{k}: {v}"
            )

        print()
        print("=" * 60)
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