import pandas as pd


class BullFlagDetector:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        signals = []

        lookback = 60

        cooldown = 20

        last_signal = -999

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            pole = window.iloc[:30]

            flag = window.iloc[30:]

            pole_start = float(
                pole.iloc[0]["Close"]
            )

            pole_end = float(
                pole.iloc[-1]["Close"]
            )

            pole_return = (
                pole_end
                - pole_start
            ) / pole_start

            if pole_return < 0.20:
                continue

            flag_high = float(
                flag["High"].max()
            )

            flag_low = float(
                flag["Low"].min()
            )

            flag_depth = (
                flag_high
                - flag_low
            ) / flag_high

            if flag_depth > 0.15:
                continue

            close = float(
                df.iloc[i]["Close"]
            )

            if close <= flag_high:
                continue

            if (
                i - last_signal
                < cooldown
            ):
                continue

            last_signal = i

            depth = (
                flag_high
                - flag_low
            )

            signals.append(
                {
                    "date":
                        df.iloc[i]["Date"],

                    "pattern":
                        "BULL_FLAG",

                    "confidence":
                        85,

                    "entry":
                        close,

                    "stop_loss":
                        flag_low,

                    "target":
                        close + depth,
                }
            )

        return signals