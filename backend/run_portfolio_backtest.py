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

from backend.services.portfolio_backtest_service import (
    PortfolioBacktestService,
)


def calculate_score(
    close_price,
    ema50,
    rsi14,
    trend_state,
):

    score = 0

    if trend_state == 1:
        score += 40

    if (
        ema50 is not None
        and close_price > ema50
    ):
        score += 30

    if (
        rsi14 is not None
        and rsi14 >= 60
    ):
        score += 20

    elif (
        rsi14 is not None
        and rsi14 >= 50
    ):
        score += 10

    return score


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

            score = calculate_score(
                ohlcv.close,
                indicator.ema50,
                indicator.rsi14,
                gann.trend_state,
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
                }
            )

        scores_df = pd.DataFrame(
            data
        )

        results = (
            PortfolioBacktestService()
            .run(
                scores_df,
                top_n=3,
            )
        )

        print()
        print("=" * 60)
        print("PORTFOLIO RESULTS")
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

    finally:

        db.close()


if __name__ == "__main__":
    main()