from sqlalchemy.orm import Session

from backend.models.pattern_signal import (
    PatternSignal,
)


class PatternSignalRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def exists(
        self,
        symbol_id,
        trading_date,
        pattern_name,
    ):

        return (
            self.db.query(
                PatternSignal
            )
            .filter(
                PatternSignal.symbol_id
                == symbol_id,
                PatternSignal.trading_date
                == trading_date,
                PatternSignal.pattern_name
                == pattern_name,
            )
            .first()
            is not None
        )

    def insert(
        self,
        **kwargs,
    ):

        signal = PatternSignal(
            **kwargs
        )

        self.db.add(signal)

        return signal

    def commit(self):

        self.db.commit()