import pandas as pd


class RoundingBottomDetectorV2:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        signals = []

        COOLDOWN_DAYS = 20
        last_signal_index = -999

        lookback = 100

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            left = (
                window.iloc[:30]["Close"]
                .mean()
            )

            middle = (
                window.iloc[30:70]["Close"]
                .mean()
            )

            right = (
                window.iloc[70:]["Close"]
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
                        "ROUNDING_BOTTOM_V2",

                    "entry":
                        close,

                    "stop_loss":
                        low_price,

                    "target":
                        close + depth,

                    "confidence":
                        80.0,
                }
            )

        return signals