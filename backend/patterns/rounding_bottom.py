import pandas as pd


class RoundingBottomDetector:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        signals = []

        COOLDOWN_DAYS = 20
        last_signal_index = -999

        lookback = 120

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            left = (
                window.iloc[:40]["Close"]
                .mean()
            )

            middle = (
                window.iloc[40:80]["Close"]
                .mean()
            )

            right = (
                window.iloc[80:]["Close"]
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

            if close <= neckline:
                continue

            if (
                i - last_signal_index
                < COOLDOWN_DAYS
            ):
                continue

            last_signal_index = i

            low_price = float(
                window["Low"].min()
            )

            depth = (
                neckline
                - low_price
            )

            signals.append(
                {
                    "date":
                        df.iloc[i]["Date"],

                    "pattern":
                        "ROUNDING_BOTTOM",

                    "entry":
                        close,

                    "stop_loss":
                        low_price,

                    "target":
                        close + depth,

                    "confidence":
                        70.0,
                }
            )

        return signals