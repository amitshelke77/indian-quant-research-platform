import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.technical_indicator import (
    TechnicalIndicator,
)

from backend.services.backtest_service import (
    BacktestService,
)


PAIRS = [

    ("sma10", "sma20"),
    ("sma10", "sma50"),
    ("sma10", "sma100"),

    ("sma20", "sma50"),
    ("sma20", "sma100"),
    ("sma20", "sma200"),

    ("sma50", "sma100"),
    ("sma50", "sma200"),

    ("ema10", "ema20"),
    ("ema10", "ema50"),
    ("ema20", "ema50"),
    ("ema50", "ema200"),
]


def main():

    db = SessionLocal()

    try:

        symbol = (
            db.query(Symbol)
            .filter(
                Symbol.symbol == "RELIANCE"
            )
            .first()
        )

        rows = (
            db.query(
                OHLCV,
                TechnicalIndicator,
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
            .filter(
                OHLCV.symbol_id
                == symbol.id
            )
            .order_by(
                OHLCV.trading_date
            )
            .all()
        )

        df = pd.DataFrame(
            [
                {
                    "Date": o.trading_date,
                    "Close": o.close,

                    "sma10": i.sma10,
                    "sma20": i.sma20,
                    "sma50": i.sma50,
                    "sma100": i.sma100,
                    "sma200": i.sma200,

                    "ema10": i.ema10,
                    "ema20": i.ema20,
                    "ema50": i.ema50,
                    "ema100": i.ema100,
                    "ema200": i.ema200,
                }
                for o, i in rows
            ]
        )

        results = []

        service = BacktestService()

        for fast, slow in PAIRS:

            result = (
                service.run_sma_strategy(
                    df,
                    fast,
                    slow,
                )
            )

            results.append(
                {
                    "strategy": f"{fast}_{slow}",
                    "cagr": result["cagr"],
                    "sharpe": result["sharpe_ratio"],
                    "alpha": result["alpha"],
                    "max_dd": result["max_drawdown"],
                }
            )

        result_df = pd.DataFrame(results)

        result_df = (
            result_df
            .sort_values(
                "sharpe",
                ascending=False,
            )
        )

        print("\n")
        print("=" * 80)
        print("TOP STRATEGIES")
        print("=" * 80)

        print(result_df)

    finally:
        db.close()


if __name__ == "__main__":
    main()