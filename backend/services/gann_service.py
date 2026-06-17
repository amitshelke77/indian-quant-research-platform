import pandas as pd


class GannService:

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

        swing_highs = self.calculate_swing_high(
            df["High"]
        )

        swing_lows = self.calculate_swing_low(
            df["Low"]
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

        # Placeholder values
        # We'll replace these with proper Gann math later

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