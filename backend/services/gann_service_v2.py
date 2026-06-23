import pandas as pd


class GannServiceV2:

    @staticmethod
    def calculate_swing_high(
        high: pd.Series,
        window: int = 3,
    ) -> pd.Series:

        return (
            high.rolling(
                window=window * 2 + 1,
                center=True,
            ).max()
            == high
        )

    @staticmethod
    def calculate_swing_low(
        low: pd.Series,
        window: int = 3,
    ) -> pd.Series:

        return (
            low.rolling(
                window=window * 2 + 1,
                center=True,
            ).min()
            == low
        )

    def generate_gann_features(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        swing_highs = (
            self.calculate_swing_high(
                df["High"]
            )
        )

        swing_lows = (
            self.calculate_swing_low(
                df["Low"]
            )
        )

        df["swing_high_flag"] = (
            swing_highs.astype(int)
        )

        df["swing_low_flag"] = (
            swing_lows.astype(int)
        )

        df["swing_high_price"] = None
        df["swing_low_price"] = None

        df.loc[
            swing_highs,
            "swing_high_price",
        ] = df["High"]

        df.loc[
            swing_lows,
            "swing_low_price",
        ] = df["Low"]

        # Structure columns

        df["higher_high_flag"] = 0
        df["higher_low_flag"] = 0
        df["lower_high_flag"] = 0
        df["lower_low_flag"] = 0

        # Original lifetime score

        df["structure_score"] = 0

        # New rolling score

        df["recent_structure_score"] = 0

        df["trend_state"] = 0

        previous_swing_high = None
        previous_swing_low = None

        structure_score = 0

        recent_signals = []

        current_trend = 0

        for idx, row in df.iterrows():

            signal = 0

            # ------------------------
            # Swing High Analysis
            # ------------------------

            if row["swing_high_flag"] == 1:

                current_high = (
                    row["swing_high_price"]
                )

                if (
                    previous_swing_high
                    is not None
                ):

                    if (
                        current_high
                        > previous_swing_high
                    ):

                        df.at[
                            idx,
                            "higher_high_flag",
                        ] = 1

                        structure_score += 1

                        signal += 1

                    elif (
                        current_high
                        < previous_swing_high
                    ):

                        df.at[
                            idx,
                            "lower_high_flag",
                        ] = 1

                        structure_score -= 1

                        signal -= 1

                previous_swing_high = (
                    current_high
                )

            # ------------------------
            # Swing Low Analysis
            # ------------------------

            if row["swing_low_flag"] == 1:

                current_low = (
                    row["swing_low_price"]
                )

                if (
                    previous_swing_low
                    is not None
                ):

                    if (
                        current_low
                        > previous_swing_low
                    ):

                        df.at[
                            idx,
                            "higher_low_flag",
                        ] = 1

                        structure_score += 1

                        signal += 1

                    elif (
                        current_low
                        < previous_swing_low
                    ):

                        df.at[
                            idx,
                            "lower_low_flag",
                        ] = 1

                        structure_score -= 1

                        signal -= 1

                previous_swing_low = (
                    current_low
                )

            # ------------------------
            # Rolling Structure Score
            # ------------------------

            if signal != 0:

                recent_signals.append(
                    signal
                )

            rolling_score = sum(
                recent_signals[-20:]
            )

            # ------------------------
            # Trend State
            # ------------------------

            if rolling_score >= 4:

                current_trend = 1

            elif rolling_score <= -4:

                current_trend = -1

            else:

                current_trend = 0

            df.at[
                idx,
                "structure_score",
            ] = structure_score

            df.at[
                idx,
                "recent_structure_score",
            ] = rolling_score

            df.at[
                idx,
                "trend_state",
            ] = current_trend

        # Placeholder Gann values

        df["angle_1x1"] = (
            df["Close"].shift(1)
            + 1
        )

        df["angle_2x1"] = (
            df["Close"].shift(1)
            + 2
        )

        df["angle_1x2"] = (
            df["Close"].shift(1)
            + 0.5
        )

        df["cycle_45"] = (
            df["Close"].shift(45)
        )

        df["cycle_90"] = (
            df["Close"].shift(90)
        )

        df["cycle_180"] = (
            df["Close"].shift(180)
        )

        return df