import pandas as pd


class GannStrategyService:

    def build_signals(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        latest_swing_high = None
        latest_swing_low = None

        signals = []

        in_position = False

        for _, row in df.iterrows():

            if (
                row["swing_high_flag"] == 1
                and pd.notna(
                    row["swing_high_price"]
                )
            ):
                latest_swing_high = (
                    row["swing_high_price"]
                )

            if (
                row["swing_low_flag"] == 1
                and pd.notna(
                    row["swing_low_price"]
                )
            ):
                latest_swing_low = (
                    row["swing_low_price"]
                )

            ema50 = row["ema50"]

            trend_state = row[
                "trend_state"
            ]

            # ENTRY
            if (
                not in_position
                and trend_state == 1
                and latest_swing_high is not None
                and row["Close"]
                > latest_swing_high
                and row["Close"]
                > ema50
            ):
                in_position = True

            # EXIT
            elif (
                in_position
                and (
                    trend_state == -1
                    or
                    (
                        latest_swing_low
                        is not None
                        and row["Close"]
                        < latest_swing_low
                    )
                    or
                    (
                        row["Close"]
                        < ema50
                    )
                )
            ):
                in_position = False

            signals.append(
                1 if in_position else 0
            )

        df["signal"] = signals

        return df