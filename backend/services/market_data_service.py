import yfinance as yf
import pandas as pd


class MarketDataService:
    def download_symbol(self, symbol: str) -> pd.DataFrame:

        ticker = f"{symbol}.NS"

        data = yf.download(
            ticker,
            period="1y",
            auto_adjust=True,
            progress=False
        )

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        return data.reset_index()