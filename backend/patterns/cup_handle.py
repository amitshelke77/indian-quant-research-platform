import pandas as pd


class CupHandleDetector:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        signals = []

        lookback = 150

        cooldown = 30

        last_signal = -999

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            cup_left = (
                window.iloc[:50]
                ["Close"]
                .mean()
            )

            cup_middle = (
                window.iloc[50:100]
                ["Close"]
                .mean()
            )

            cup_right = (
                window.iloc[100:130]
                ["Close"]
                .mean()
            )

            if not (
                cup_middle < cup_left
                and cup_middle < cup_right
            ):
                continue

            handle = (
                window.iloc[130:]
            )

            handle_high = (
                handle["High"].max()
            )

            handle_low = (
                handle["Low"].min()
            )

            handle_depth = (
                handle_high
                - handle_low
            ) / handle_high

            if handle_depth > 0.10:
                continue

            close = float(
                df.iloc[i]["Close"]
            )

            breakout_level = float(
                handle_high
            )

            if close <= breakout_level:
                continue

            if (
                i - last_signal
                < cooldown
            ):
                continue

            last_signal = i

            cup_low = float(
                window["Low"].min()
            )

            depth = (
                breakout_level
                - cup_low
            )

            signals.append(
                {
                    "date":
                        df.iloc[i]["Date"],

                    "pattern":
                        "CUP_HANDLE",

                    "confidence":
                        80,

                    "entry":
                        close,

                    "stop_loss":
                        handle_low,

                    "target":
                        close + depth,
                }
            )

        return signals