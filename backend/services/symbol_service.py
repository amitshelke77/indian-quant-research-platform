from sqlalchemy.orm import Session

from backend.repositories.symbol_repository import SymbolRepository


class SymbolService:
    def __init__(self, db: Session):
        self.repository = SymbolRepository(db)

    def create_symbol(
        self,
        symbol: str,
        company_name: str,
        exchange: str
    ):
        existing = self.repository.get_by_symbol(symbol)

        if existing:
            return existing

        return self.repository.create(
            symbol=symbol,
            company_name=company_name,
            exchange=exchange
        )