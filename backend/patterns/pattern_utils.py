import pandas as pd


def calculate_rsi(
    close: pd.Series,
    period: int = 14,
):

    delta = close.diff()

    gain = (
        delta.where(
            delta > 0,
            0,
        )
    )

    loss = (
        -delta.where(
            delta < 0,
            0,
        )
    )

    avg_gain = (
        gain.rolling(period)
        .mean()
    )

    avg_loss = (
        loss.rolling(period)
        .mean()
    )

    rs = (
        avg_gain
        /
        avg_loss
    )

    rsi = (
        100
        -
        (
            100
            /
            (
                1 + rs
            )
        )
    )

    return rsi


def add_filters(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["ema50"] = (
        df["Close"]
        .ewm(span=50)
        .mean()
    )

    df["ema200"] = (
        df["Close"]
        .ewm(span=200)
        .mean()
    )

    df["volume_ma20"] = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["rsi"] = calculate_rsi(
        df["Close"]
    )

    return df