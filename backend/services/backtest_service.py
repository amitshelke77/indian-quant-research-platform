import pandas as pd

from backend.services.metrics_service import (
    MetricsService,
)


class BacktestService:

    def run_sma_strategy(
        self,
        df: pd.DataFrame,
    ) -> dict:

        df = df.copy()

        df["signal"] = 0

        df.loc[
            df["sma20"] > df["sma50"],
            "signal",
        ] = 1

        df["returns"] = (
            df["Close"]
            .pct_change()
            .fillna(0)
        )

        df["strategy_returns"] = (
            df["signal"]
            .shift(1)
            .fillna(0)
            * df["returns"]
        )

        equity_curve = (
            100000
            * (
                1
                + df["strategy_returns"]
            ).cumprod()
        )

        total_return = (
            equity_curve.iloc[-1]
            / equity_curve.iloc[0]
            - 1
        )

        cagr = MetricsService.calculate_cagr(
            equity_curve
        )

        sharpe = MetricsService.calculate_sharpe(
            df["strategy_returns"]
        )

        sortino = MetricsService.calculate_sortino(
            df["strategy_returns"]
        )

        max_dd = MetricsService.calculate_max_drawdown(
            equity_curve
        )

        calmar = MetricsService.calculate_calmar(
            cagr,
            max_dd,
        )

        annual_return = (
            MetricsService.calculate_annual_return(
                df["strategy_returns"]
            )
        )

        return {
            "total_return": float(total_return),
            "annual_return": float(annual_return),
            "cagr": float(cagr),
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "calmar_ratio": float(calmar),
            "max_drawdown": float(max_dd),
        }