import pandas as pd

from backend.services.metrics_service import (
    MetricsService,
)


class PortfolioBacktestServiceV2:

    def run(
        self,
        scores_df: pd.DataFrame,
        top_n: int = 10,
        initial_capital: float = 100000,
    ) -> dict:

        df = scores_df.copy()

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        dates = sorted(
            df["Date"].unique()
        )

        holdings = set()

        portfolio_returns = []

        for i in range(
            len(dates) - 1
        ):

            current_date = dates[i]

            next_date = dates[i + 1]

            today = df[
                df["Date"]
                == current_date
            ]

            ranked = (
                today.sort_values(
                    "Score",
                    ascending=False,
                )
            )

            # ONLY BUY STRONG SCORES

            ranked = ranked[
                ranked["Score"] >= 60
            ]

            top_symbols = list(
                ranked.head(top_n)[
                    "Symbol"
                ]
            )

            # REMOVE WEAK HOLDINGS

            remove_list = []

            for symbol in holdings:

                row = today[
                    today["Symbol"]
                    == symbol
                ]

                if len(row) == 0:
                    continue

                row = row.iloc[0]

                if (
                    row["Trend"] != 1
                    or row["Close"]
                    < row["EMA50"]
                ):
                    remove_list.append(
                        symbol
                    )

            for symbol in remove_list:

                holdings.remove(
                    symbol
                )

            # ADD NEW STRONG STOCKS

            for symbol in top_symbols:

                if (
                    len(holdings)
                    >= top_n
                ):
                    break

                holdings.add(
                    symbol
                )

            daily_returns = []

            for symbol in holdings:

                current_row = today[
                    today["Symbol"]
                    == symbol
                ]

                next_row = df[
                    (df["Date"] == next_date)
                    &
                    (
                        df["Symbol"]
                        == symbol
                    )
                ]

                if (
                    len(current_row)
                    == 0
                    or len(next_row)
                    == 0
                ):
                    continue

                current_close = (
                    current_row.iloc[0][
                        "Close"
                    ]
                )

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

            if len(daily_returns):

                portfolio_returns.append(
                    sum(
                        daily_returns
                    )
                    /
                    len(
                        daily_returns
                    )
                )

            else:

                portfolio_returns.append(
                    0
                )

        returns = pd.Series(
            portfolio_returns
        )

        equity_curve = (
            initial_capital
            *
            (
                1
                + returns
            ).cumprod()
        )

        total_return = (
            equity_curve.iloc[-1]
            /
            equity_curve.iloc[0]
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
            "cagr": float(
                cagr
            ),
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
            "equity_curve":
                equity_curve,
        }