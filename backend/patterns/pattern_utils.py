import pandas as pd


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

    return df