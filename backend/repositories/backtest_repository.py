from sqlalchemy.orm import Session

from backend.models.backtest_result import (
    BacktestResult,
)


class BacktestRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def insert(
        self,
        **kwargs,
    ) -> BacktestResult:

        result = BacktestResult(
            **kwargs
        )

        self.db.add(result)

        return result

    def commit(
        self,
    ) -> None:

        self.db.commit()