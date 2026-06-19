import pandas as pd


class GannStrategyService:

    def build_signals(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Original strategy:
        GANN_STRUCTURE_EMA50
        """

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

    def build_signals_rsi(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        New strategy:
        GANN_STRUCTURE_EMA50_RSI
        """

        df = df.copy()

        signals = []

        in_position = False

        for _, row in df.iterrows():

            trend_state = row[
                "trend_state"
            ]

            ema50 = row["ema50"]

            rsi14 = row["rsi14"]

            # ENTRY

            if (
                not in_position
                and trend_state == 1
                and pd.notna(ema50)
                and pd.notna(rsi14)
                and row["Close"] > ema50
                and rsi14 > 55
            ):
                in_position = True

            # EXIT

            elif (
                in_position
                and (
                    trend_state == -1
                    or
                    row["Close"] < ema50
                )
            ):
                in_position = False

            signals.append(
                1 if in_position else 0
            )

        df["signal"] = signals

        return df