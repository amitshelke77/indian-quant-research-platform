import pandas as pd

from backend.patterns.pattern_utils import (
    add_filters,
)


class RoundingBottomDetectorV4:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        df = add_filters(df)

        signals = []

        lookback = 120

        cooldown = 30

        last_signal = -999

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            left = (
                window.iloc[:40]
                ["Close"]
                .mean()
            )

            middle = (
                window.iloc[40:80]
                ["Close"]
                .mean()
            )

            right = (
                window.iloc[80:]
                ["Close"]
                .mean()
            )

            if not (
                middle < left
                and middle < right
            ):
                continue

            neckline = float(
                window["High"].max()
            )

            close = float(
                df.iloc[i]["Close"]
            )

            if (
                close
                < neckline * 1.01
            ):
                continue

            if (
                df.iloc[i]["ema50"]
                <=
                df.iloc[i]["ema200"]
            ):
                continue

            if (
                df.iloc[i]["Volume"]
                <
                df.iloc[i]["volume_ma20"]
                * 1.5
            ):
                continue

            rsi = float(
                df.iloc[i]["rsi"]
            )

            # NEW FILTER
            if rsi < 70:
                continue

            if (
                i - last_signal
                < cooldown
            ):
                continue

            last_signal = i

            low_price = float(
                window["Low"].min()
            )

            depth = (
                neckline
                - low_price
            )

            volume_ratio = (
                float(
                    df.iloc[i]["Volume"]
                )
                /
                float(
                    df.iloc[i]["volume_ma20"]
                )
            )

            signals.append(
                {
                    "date":
                        df.iloc[i]["Date"],

                    "pattern":
                        "ROUNDING_BOTTOM_V4",

                    "entry":
                        close,

                    "stop_loss":
                        low_price,

                    "target":
                        close + depth,

                    "confidence":
                        90,

                    "rsi":
                        rsi,

                    "volume_ratio":
                        volume_ratio,

                    "ema50":
                        float(
                            df.iloc[i]["ema50"]
                        ),

                    "ema200":
                        float(
                            df.iloc[i]["ema200"]
                        ),
                }
            )

        return signals