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

from backend.repositories.backtest_repository import (
    BacktestRepository,
)


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

        if not symbol:
            print("RELIANCE not found")
            return

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
                ),
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
            print("No data found")
            return

        df = pd.DataFrame(
            [
                {
                    "Date": o.trading_date,
                    "Close": o.close,
                    "sma20": i.sma20,
                    "sma50": i.sma50,
                }
                for o, i in rows
            ]
        )

        result = (
            BacktestService()
            .run_sma_strategy(
                df,
                "sma20",
                "sma50",
    )
)

        repo = BacktestRepository(db)

        repo.insert(
            strategy_name="SMA20_SMA50_CROSSOVER",
            symbol_id=symbol.id,

            total_return=result["total_return"],
            annual_return=result["annual_return"],
            cagr=result["cagr"],

            sharpe_ratio=result["sharpe_ratio"],
            sortino_ratio=result["sortino_ratio"],
            calmar_ratio=result["calmar_ratio"],

            max_drawdown=result["max_drawdown"],

            alpha=result["alpha"],
            beta=result["beta"],
            tracking_error=result["tracking_error"],
            information_ratio=result["information_ratio"],

            benchmark_return=result["benchmark_return"],
            transaction_costs=0.0,
        )

        repo.commit()

        print("\nBacktest Results")
        print("=" * 50)

        for key, value in result.items():
            print(f"{key}: {value}")

        print("\nBacktest saved to database.")

    finally:
        db.close()


if __name__ == "__main__":
    main()