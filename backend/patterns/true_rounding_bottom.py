import pandas as pd
import numpy as np

from backend.patterns.pattern_utils import (
    add_filters,
)


class TrueRoundingBottomDetector:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        df = add_filters(df)

        signals = []

        lookback = 120

        cooldown = 40

        last_signal = -999

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ].copy()

            prices = (
                window["Close"]
                .values
            )

            x = np.arange(
                len(prices)
            )

            lowest_idx = int(
                np.argmin(
                    prices
                )
            )

            # Bottom must be near center
            if (
                lowest_idx < 35
                or lowest_idx > 85
            ):
                continue

            left_lip = float(
                prices[0]
            )

            right_lip = float(
                prices[-1]
            )

            lowest_price = float(
                prices.min()
            )

            # Lips must be similar
            lip_diff = abs(
                left_lip
                - right_lip
            ) / left_lip

            if lip_diff > 0.15:
                continue

            # Cup depth
            depth = (
                left_lip
                - lowest_price
            ) / left_lip

            if depth < 0.15:
                continue

            # Fit parabola
            y_norm = (
                prices
                - prices.min()
            ) / (
                prices.max()
                - prices.min()
                + 1e-9
            )

            coeffs = np.polyfit(
                x,
                y_norm,
                2,
            )

            parabola = np.poly1d(
                coeffs
            )

            y_pred = parabola(
                x
            )

            ss_res = np.sum(
                (
                    y_norm
                    - y_pred
                ) ** 2
            )

            ss_tot = np.sum(
                (
                    y_norm
                    - np.mean(
                        y_norm
                    )
                ) ** 2
            )

            r_squared = (
                1
                - ss_res
                / ss_tot
            )

            if r_squared < 0.75:
                continue

            # Neckline
            neckline = max(
                left_lip,
                right_lip,
            )

            close = float(
                df.iloc[i][
                    "Close"
                ]
            )

            # Real breakout
            if (
                close
                <
                neckline
                * 1.02
            ):
                continue

            # Trend filter
            if (
                df.iloc[i][
                    "ema50"
                ]
                <=
                df.iloc[i][
                    "ema200"
                ]
            ):
                continue

            # Volume filter
            if (
                df.iloc[i][
                    "Volume"
                ]
                <
                df.iloc[i][
                    "volume_ma20"
                ]
                * 1.5
            ):
                continue

            if (
                i
                - last_signal
                < cooldown
            ):
                continue

            last_signal = i

            breakout_date = (
                df.iloc[i][
                    "Date"
                ]
            )

            entry = close

            stop_loss = float(
                window["Low"]
                .tail(20)
                .min()
            )

            risk = (
                entry
                - stop_loss
            )

            if risk <= 0:
                continue

            # 2R target
            target = (
                entry
                + (risk * 2)
            )

            confidence = min(
                95,
                int(
                    70
                    + (
                        r_squared
                        * 20
                    )
                ),
            )

            signals.append(
                {
                    "date":
                        breakout_date,

                    "pattern":
                        "TRUE_ROUNDING_BOTTOM",

                    "entry":
                        float(
                            entry
                        ),

                    "stop_loss":
                        float(
                            stop_loss
                        ),

                    "target":
                        float(
                            target
                        ),

                    "confidence":
                        float(
                            confidence
                        ),
                }
            )

        return signals