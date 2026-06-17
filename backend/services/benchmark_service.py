import numpy as np
import pandas as pd


class BenchmarkService:

    @staticmethod
    def buy_and_hold_return(
        close: pd.Series,
    ) -> float:

        if len(close) < 2:
            return 0.0

        return float(
            close.iloc[-1]
            / close.iloc[0]
            - 1
        )

    @staticmethod
    def alpha(
        strategy_return: float,
        benchmark_return: float,
    ) -> float:

        return float(
            strategy_return
            - benchmark_return
        )

    @staticmethod
    def beta(
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series,
    ) -> float:

        strategy_returns = strategy_returns.fillna(0)
        benchmark_returns = benchmark_returns.fillna(0)

        variance = np.var(
            benchmark_returns
        )

        if variance == 0:
            return 0.0

        covariance = np.cov(
            strategy_returns,
            benchmark_returns,
        )[0][1]

        return float(
            covariance / variance
        )

    @staticmethod
    def tracking_error(
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series,
    ) -> float:

        diff = (
            strategy_returns
            - benchmark_returns
        )

        return float(
            diff.std()
            * np.sqrt(252)
        )

    @staticmethod
    def information_ratio(
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series,
    ) -> float:

        diff = (
            strategy_returns
            - benchmark_returns
        )

        tracking_error = (
            diff.std()
            * np.sqrt(252)
        )

        if tracking_error == 0:
            return 0.0

        return float(
            diff.mean()
            * 252
            / tracking_error
        )