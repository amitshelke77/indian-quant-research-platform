import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis

from backend.services.gann_strategy_service import (
    GannStrategyService,
)

from backend.services.gann_backtest_service import (
    GannBacktestService,
)

from backend.repositories.backtest_repository import (
    BacktestRepository,
)


STRATEGY_NAME = "GANN_SWING_BREAKOUT"
SYMBOL_NAME = "RELIANCE"


def main():

    db = SessionLocal()

    try:

        symbol = (
            db.query(Symbol)
            .filter(
                Symbol.symbol == SYMBOL_NAME
            )
            .first()
        )

        if symbol is None:
            print("Symbol not found")
            return

        rows = (
            db.query(
                OHLCV,
                GannAnalysis,
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
            print("No data found")
            return

        df = pd.DataFrame(
            [
                {
                    "Date": o.trading_date,
                    "Close": o.close,
                    "High": o.high,
                    "Low": o.low,

                    "swing_high_flag":
                        g.swing_high_flag,

                    "swing_low_flag":
                        g.swing_low_flag,

                    "swing_high_price":
                        g.swing_high_price,

                    "swing_low_price":
                        g.swing_low_price,
                }
                for o, g in rows
            ]
        )

        df = (
            GannStrategyService()
            .build_signals(df)
        )

        results = (
            GannBacktestService()
            .run(df)
        )

        print("\nBacktest Results")
        print("=" * 50)

        for k, v in results.items():
            print(f"{k}: {v}")

        repo = BacktestRepository(db)

        repo.insert(
            strategy_name=STRATEGY_NAME,
            symbol_id=symbol.id,
            **results,
        )

        repo.commit()

        print("\nBacktest saved.")

    finally:
        db.close()


if __name__ == "__main__":
    main()