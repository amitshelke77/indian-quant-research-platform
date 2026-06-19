import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import (
    TechnicalIndicator,
)

from backend.services.gann_backtest_service import (
    GannBacktestService,
)

from backend.services.gann_structure_score_strategy import (
    GannStructureScoreStrategy,
)

from backend.repositories.backtest_repository import (
    BacktestRepository,
)


STRATEGY_NAME = "GANN_STRUCTURE_SCORE"


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
                continue

            df = pd.DataFrame(
                [
                    {
                        "Date": o.trading_date,
                        "Close": o.close,
                        "High": o.high,
                        "Low": o.low,

                        "ema50": t.ema50,

                        "structure_score":
                            g.structure_score,
                    }
                    for o, t, g in rows
                ]
            )

            df = (
                GannStructureScoreStrategy()
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
                }
            )

            print(
                f"CAGR={results['cagr']:.4f} "
                f"Sharpe={results['sharpe_ratio']:.4f}"
            )

        repo.commit()

        print("\n")
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(
            pd.DataFrame(summary)
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()