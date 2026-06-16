from backend.core.database import engine

with engine.connect() as connection:
    print("Database Connected")