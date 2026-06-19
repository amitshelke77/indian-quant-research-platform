import pandas as pd

from backend.services.metrics_service import (
    MetricsService,
)


class PortfolioBacktestService:

    def run(
        self,
        scores_df: pd.DataFrame,
        top_n: int = 3,
        initial_capital: float = 100000,
    ) -> dict:

        df = scores_df.copy()

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        dates = sorted(
            df["Date"].unique()
        )

        portfolio_returns = []

        for i in range(
            len(dates) - 1
        ):

            current_date = dates[i]

            next_date = dates[i + 1]

            today = (
                df[
                    df["Date"]
                    == current_date
                ]
                .sort_values(
                    "Score",
                    ascending=False,
                )
            )

            selected = (
                today.head(top_n)
            )

            daily_returns = []

            for _, row in (
                selected.iterrows()
            ):

                symbol = row["Symbol"]

                current_close = (
                    row["Close"]
                )

                next_row = df[
                    (df["Date"] == next_date)
                    &
                    (
                        df["Symbol"]
                        == symbol
                    )
                ]

                if len(next_row) == 0:
                    continue

                next_close = (
                    next_row.iloc[0][
                        "Close"
                    ]
                )

                ret = (
                    next_close
                    / current_close
                    - 1
                )

                daily_returns.append(
                    ret
                )

            if (
                len(daily_returns)
                == 0
            ):
                portfolio_returns.append(
                    0
                )
            else:
                portfolio_returns.append(
                    sum(
                        daily_returns
                    )
                    / len(
                        daily_returns
                    )
                )

        returns = pd.Series(
            portfolio_returns
        )

        equity_curve = (
            initial_capital
            * (
                1
                + returns
            ).cumprod()
        )

        total_return = (
            equity_curve.iloc[-1]
            / equity_curve.iloc[0]
            - 1
        )

        annual_return = (
            MetricsService.calculate_annual_return(
                returns
            )
        )

        cagr = (
            MetricsService.calculate_cagr(
                equity_curve
            )
        )

        sharpe = (
            MetricsService.calculate_sharpe(
                returns
            )
        )

        sortino = (
            MetricsService.calculate_sortino(
                returns
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

        return {
            "total_return": float(
                total_return
            ),
            "annual_return": float(
                annual_return
            ),
            "cagr": float(cagr),
            "sharpe_ratio": float(
                sharpe
            ),
            "sortino_ratio": float(
                sortino
            ),
            "max_drawdown": float(
                max_drawdown
            ),
            "calmar_ratio": float(
                calmar
            ),
            "equity_curve": equity_curve,
        }