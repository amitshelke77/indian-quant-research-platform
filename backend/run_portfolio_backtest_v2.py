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

from backend.models.technical_indicator import (
    TechnicalIndicator,
)

from backend.services.portfolio_backtest_service_v2 import (
    PortfolioBacktestServiceV2,
)

from backend.services.score_service import (
    ScoreService,
)


def main():

    db = SessionLocal()

    try:

        rows = (
            db.query(
                Symbol,
                OHLCV,
                TechnicalIndicator,
                GannAnalysis,
            )
            .join(
                OHLCV,
                Symbol.id
                == OHLCV.symbol_id,
            )
            .join(
                TechnicalIndicator,
                (
                    OHLCV.symbol_id
                    ==
                    TechnicalIndicator.symbol_id
                )
                &
                (
                    OHLCV.trading_date
                    ==
                    TechnicalIndicator.trading_date
                )
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
            indicator,
            gann,
        ) in rows:

            score = (
                ScoreService
                .calculate_score(
                    close_price=ohlcv.close,
                    ema50=indicator.ema50,
                    rsi14=indicator.rsi14,
                    trend_state=gann.trend_state,
                    swing_high_price=gann.swing_high_price,
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

                    "EMA50":
                        indicator.ema50,

                    "Trend":
                        gann.trend_state,

                    "StructureScore":
                        gann.structure_score,
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
                top_n=20,
            )
        )

        print()
        print("=" * 60)
        print("PORTFOLIO RESULTS V2")
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