import pandas as pd

from backend.services.metrics_service import (
    MetricsService,
)

from backend.services.benchmark_service import (
    BenchmarkService,
)


class BacktestService:

    def run_sma_strategy(
        self,
        df: pd.DataFrame,
        fast_column: str,
        slow_column: str,
    ) -> dict:

        df = df.copy()

        # Remove rows where indicators aren't available yet

        df = df.dropna(
            subset=[
                fast_column,
                slow_column,
            ]
        )

        if len(df) < 50:

            return {
                "total_return": 0.0,
                "annual_return": 0.0,
                "cagr": 0.0,
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
                "calmar_ratio": 0.0,
                "max_drawdown": 0.0,
                "benchmark_return": 0.0,
                "alpha": 0.0,
                "beta": 0.0,
                "tracking_error": 0.0,
                "information_ratio": 0.0,
            }

        df["signal"] = 0

        df.loc[
            df[fast_column]
            > df[slow_column],
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

        annual_return = (
            MetricsService.calculate_annual_return(
                df["strategy_returns"]
            )
        )

        cagr = (
            MetricsService.calculate_cagr(
                equity_curve
            )
        )

        sharpe = (
            MetricsService.calculate_sharpe(
                df["strategy_returns"]
            )
        )

        sortino = (
            MetricsService.calculate_sortino(
                df["strategy_returns"]
            )
        )

        max_drawdown = (
            MetricsService.calculate_max_drawdown(
                equity_curve
            )
        )

        calmar = (
            MetricsService.calculate_calmar(
                cagr,
                max_drawdown,
            )
        )

        benchmark_return = (
            BenchmarkService.buy_and_hold_return(
                df["Close"]
            )
        )

        alpha = (
            BenchmarkService.alpha(
                total_return,
                benchmark_return,
            )
        )

        beta = (
            BenchmarkService.beta(
                df["strategy_returns"],
                df["returns"],
            )
        )

        tracking_error = (
            BenchmarkService.tracking_error(
                df["strategy_returns"],
                df["returns"],
            )
        )

        information_ratio = (
            BenchmarkService.information_ratio(
                df["strategy_returns"],
                df["returns"],
            )
        )

        return {
            "total_return": float(total_return),
            "annual_return": float(annual_return),
            "cagr": float(cagr),
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "calmar_ratio": float(calmar),
            "max_drawdown": float(max_drawdown),
            "benchmark_return": float(benchmark_return),
            "alpha": float(alpha),
            "beta": float(beta),
            "tracking_error": float(tracking_error),
            "information_ratio": float(information_ratio),
        }