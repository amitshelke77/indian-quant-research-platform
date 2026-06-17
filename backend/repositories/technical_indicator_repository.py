from datetime import date

from sqlalchemy.orm import Session

from backend.models.technical_indicator import TechnicalIndicator


class TechnicalIndicatorRepository:

    def __init__(self, db: Session):
        self.db = db

    def exists(
        self,
        symbol_id: int,
        trading_date: date,
    ) -> bool:

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.symbol_id == symbol_id,
                TechnicalIndicator.trading_date == trading_date,
            )
            .first()
            is not None
        )

    def insert(
        self,
        **kwargs,
    ):
        row = TechnicalIndicator(**kwargs)
        self.db.add(row)

    def commit(self):
        self.db.commit()