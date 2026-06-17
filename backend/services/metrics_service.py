import numpy as np
import pandas as pd


class MetricsService:

    @staticmethod
    def calculate_cagr(
        equity_curve: pd.Series,
    ) -> float:

        years = len(
            equity_curve
        ) / 252

        if years <= 0:
            return 0.0

        start = equity_curve.iloc[0]
        end = equity_curve.iloc[-1]

        if start <= 0:
            return 0.0

        return (
            (end / start)
            ** (1 / years)
            - 1
        )

    @staticmethod
    def calculate_sharpe(
        returns: pd.Series,
        risk_free_rate: float = 0.0,
    ) -> float:

        excess = (
            returns
            - risk_free_rate / 252
        )

        std = excess.std()

        if std == 0:
            return 0.0

        return (
            np.sqrt(252)
            * excess.mean()
            / std
        )

    @staticmethod
    def calculate_sortino(
        returns: pd.Series,
    ) -> float:

        downside = returns[
            returns < 0
        ]

        downside_std = downside.std()

        if (
            downside_std is None
            or downside_std == 0
        ):
            return 0.0

        return (
            np.sqrt(252)
            * returns.mean()
            / downside_std
        )

    @staticmethod
    def calculate_max_drawdown(
        equity_curve: pd.Series,
    ) -> float:

        running_max = (
            equity_curve.cummax()
        )

        drawdown = (
            equity_curve
            - running_max
        ) / running_max

        return float(
            drawdown.min()
        )

    @staticmethod
    def calculate_calmar(
        cagr: float,
        max_drawdown: float,
    ) -> float:

        if max_drawdown == 0:
            return 0.0

        return (
            cagr
            / abs(max_drawdown)
        )

    @staticmethod
    def calculate_annual_return(
        returns: pd.Series,
    ) -> float:

        return (
            (1 + returns.mean())
            ** 252
            - 1
        )