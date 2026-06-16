from typing import Optional

from sqlalchemy.orm import Session

from backend.models.symbol import Symbol


class SymbolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_symbol(
        self,
        symbol: str
    ) -> Optional[Symbol]:
        return (
            self.db.query(Symbol)
            .filter(Symbol.symbol == symbol)
            .first()
        )

    def create(
        self,
        symbol: str,
        company_name: str,
        exchange: str
    ) -> Symbol:

        entity = Symbol(
            symbol=symbol,
            company_name=company_name,
            exchange=exchange
        )

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return entity

    def list_all(self) -> list[Symbol]:
        return self.db.query(Symbol).all()