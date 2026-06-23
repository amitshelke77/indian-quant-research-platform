import pandas as pd

from backend.patterns.pattern_utils import (
    add_filters,
)


class DoubleBottomDetectorV2:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        df = add_filters(df)

        signals = []

        cooldown = 20

        last_signal = -999

        lookback = 80

        for i in range(
            lookback,
            len(df),
        ):

            window = df.iloc[
                i - lookback:i
            ]

            lows = (
                window["Low"]
                .nsmallest(2)
            )

            if len(lows) < 2:
                continue

            low_indexes = (
                lows.index.tolist()
            )

            if abs(
                low_indexes[0]
                -
                low_indexes[1]
            ) < 15:
                continue

            low1 = lows.iloc[0]
            low2 = lows.iloc[1]

            difference = (
                abs(low1 - low2)
                / low1
            )

            if difference > 0.015:
                continue

            neckline = (
                window["High"]
                .max()
            )

            close = (
                df.iloc[i]["Close"]
            )

            if (
                close
                <
                neckline * 1.01
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

            if (
                i - last_signal
                < cooldown
            ):
                continue

            last_signal = i

            depth = (
                neckline
                - low1
            )

            entry = close

            stop_loss = low1

            target = (
                entry + depth
            )

            signals.append(
                {
                    "date":
                        df.iloc[i]["Date"],

                    "pattern":
                        "DOUBLE_BOTTOM_V2",

                    "confidence":
                        85,

                    "entry":
                        float(entry),

                    "stop_loss":
                        float(stop_loss),

                    "target":
                        float(target),
                }
            )

        return signals