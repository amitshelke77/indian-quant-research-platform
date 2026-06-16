from datetime import date

from sqlalchemy.orm import Session

from backend.models.ohlcv import OHLCV


class OHLCVRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists(
        self,
        symbol_id: int,
        trading_date: date,
    ) -> bool:

        return (
            self.db.query(OHLCV)
            .filter(
                OHLCV.symbol_id == symbol_id,
                OHLCV.trading_date == trading_date,
            )
            .first()
            is not None
        )

    def insert(
        self,
        symbol_id: int,
        trading_date: date,
        open_price: float,
        high_price: float,
        low_price: float,
        close_price: float,
        volume: float,
    ):

        row = OHLCV(
            symbol_id=symbol_id,
            trading_date=trading_date,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=volume,
        )

        self.db.add(row)

    def commit(self):
        self.db.commit()