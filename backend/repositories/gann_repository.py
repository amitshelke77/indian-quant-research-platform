from datetime import date

from sqlalchemy.orm import Session

from backend.models.gann_analysis import (
    GannAnalysis,
)


class GannRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def exists(
        self,
        symbol_id: int,
        trading_date: date,
    ) -> bool:

        return (
            self.db.query(
                GannAnalysis
            )
            .filter(
                GannAnalysis.symbol_id
                == symbol_id,
                GannAnalysis.trading_date
                == trading_date,
            )
            .first()
            is not None
        )

    def insert(
        self,
        **kwargs,
    ):

        row = GannAnalysis(
            **kwargs
        )

        self.db.add(row)

    def commit(self):

        self.db.commit()