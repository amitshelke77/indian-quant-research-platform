import pandas as pd


class IndicatorService:

    @staticmethod
    def calculate_sma(
        series: pd.Series,
        period: int,
    ) -> pd.Series:
        return series.rolling(period).mean()

    @staticmethod
    def calculate_ema(
        series: pd.Series,
        period: int,
    ) -> pd.Series:
        return series.ewm(
            span=period,
            adjust=False,
        ).mean()

    @staticmethod
    def calculate_rsi(
        series: pd.Series,
        period: int = 14,
    ) -> pd.Series:

        delta = series.diff()

        gain = delta.where(
            delta > 0,
            0,
        )

        loss = -delta.where(
            delta < 0,
            0,
        )

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (
            100 / (1 + rs)
        )

        return rsi

    @staticmethod
    def calculate_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14,
    ) -> pd.Series:

        prev_close = close.shift(1)

        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()

        true_range = pd.concat(
            [tr1, tr2, tr3],
            axis=1,
        ).max(axis=1)

        atr = true_range.rolling(period).mean()

        return atr

    @staticmethod
    def calculate_macd(
        series: pd.Series,
    ):

        ema12 = series.ewm(
            span=12,
            adjust=False,
        ).mean()

        ema26 = series.ewm(
            span=26,
            adjust=False,
        ).mean()

        macd = ema12 - ema26

        signal = macd.ewm(
            span=9,
            adjust=False,
        ).mean()

        histogram = macd - signal

        return (
            macd,
            signal,
            histogram,
        )

    @staticmethod
    def calculate_bollinger_bands(
        series: pd.Series,
        period: int = 20,
        std_multiplier: float = 2.0,
    ):

        middle = series.rolling(period).mean()

        std = series.rolling(period).std()

        upper = middle + (
            std_multiplier * std
        )

        lower = middle - (
            std_multiplier * std
        )

        return (
            upper,
            middle,
            lower,
        )

    def generate_indicators(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        df["sma20"] = self.calculate_sma(close, 20)
        df["sma50"] = self.calculate_sma(close, 50)

        df["ema20"] = self.calculate_ema(close, 20)
        df["ema50"] = self.calculate_ema(close, 50)

        df["rsi14"] = self.calculate_rsi(close)

        df["atr14"] = self.calculate_atr(
            high,
            low,
            close,
        )

        (
            df["macd"],
            df["macd_signal"],
            df["macd_histogram"],
        ) = self.calculate_macd(close)

        (
            df["bb_upper"],
            df["bb_middle"],
            df["bb_lower"],
        ) = self.calculate_bollinger_bands(close)

        return df