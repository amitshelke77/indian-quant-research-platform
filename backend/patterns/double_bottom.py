import pandas as pd


class DoubleBottomDetector:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        signals = []

        COOLDOWN_DAYS = 20
        last_signal_index = -999

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

            low1 = lows.iloc[0]
            low2 = lows.iloc[1]

            difference = abs(
                low1 - low2
            ) / low1

            if difference > 0.03:
                continue

            neckline = (
                window["High"]
                .max()
            )

            close = (
                df.iloc[i]["Close"]
            )

            if close <= neckline:
                continue

            # Cooldown filter
            if (
                i - last_signal_index
                < COOLDOWN_DAYS
            ):
                continue

            last_signal_index = i

            depth = (
                neckline
                - low1
            )

            entry = close

            stop_loss = low1

            target = (
                entry + depth
            )

            breakout_date = (
                df.iloc[i]["Date"]
            )

            signals.append(
                {
                    "date": breakout_date,
                    "pattern": "DOUBLE_BOTTOM",
                    "confidence": 75,
                    "entry": float(entry),
                    "stop_loss": float(stop_loss),
                    "target": float(target),
                }
            )

        return signals