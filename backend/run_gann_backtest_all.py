import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import (
    TechnicalIndicator,
)

from backend.services.gann_strategy_service import (
    GannStrategyService,
)

from backend.services.gann_backtest_service import (
    GannBacktestService,
)

from backend.repositories.backtest_repository import (
    BacktestRepository,
)


STRATEGY_NAME = "GANN_STRUCTURE_EMA50"


def main():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        repo = BacktestRepository(db)

        summary = []

        for symbol in symbols:

            print("\n" + "=" * 60)
            print(f"Processing {symbol.symbol}")
            print("=" * 60)

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
                    OHLCV.trading_date
                )
                .all()
            )

            if not rows:
                print("No data")
                continue

            df = pd.DataFrame(
                [
                    {
                        "Date": o.trading_date,

                        "Close": o.close,
                        "High": o.high,
                        "Low": o.low,

                        # Indicators

                        "ema50": t.ema50,
                        "rsi14": t.rsi14,

                        # Gann Structure

                        "trend_state":
                            g.trend_state,

                        "swing_high_flag":
                            g.swing_high_flag,

                        "swing_low_flag":
                            g.swing_low_flag,

                        "swing_high_price":
                            g.swing_high_price,

                        "swing_low_price":
                            g.swing_low_price,
                    }
                    for o, t, g in rows
                ]
            )

            if len(df) == 0:
                print("Empty dataframe")
                continue

            df = (
                GannStrategyService()
                .build_signals(df)
            )

            results = (
                GannBacktestService()
                .run(df)
            )

            repo.insert(
                strategy_name=STRATEGY_NAME,
                symbol_id=symbol.id,
                **results,
            )

            summary.append(
                {
                    "symbol":
                        symbol.symbol,

                    "cagr":
                        results["cagr"],

                    "sharpe":
                        results["sharpe_ratio"],

                    "alpha":
                        results["alpha"],

                    "max_dd":
                        results["max_drawdown"],
                }
            )

            print(
                f"CAGR={results['cagr']:.4f} "
                f"Sharpe={results['sharpe_ratio']:.4f}"
            )

        repo.commit()

        result_df = pd.DataFrame(summary)

        print("\n")
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(result_df)

        print("\n")
        print("=" * 80)
        print("AVERAGES")
        print("=" * 80)

        print(
            "Average CAGR:",
            result_df["cagr"].mean()
        )

        print(
            "Average Sharpe:",
            result_df["sharpe"].mean()
        )

        print(
            "Average Alpha:",
            result_df["alpha"].mean()
        )

        print(
            "Average Max DD:",
            result_df["max_dd"].mean()
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()