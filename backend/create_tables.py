from backend.core.base import Base
from backend.core.database import engine

# Import models
from backend.models.symbol import Symbol

Base.metadata.create_all(bind=engine)

print("Tables Created")