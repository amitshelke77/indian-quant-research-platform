import backend.models

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol


NIFTY100 = [
    "ABB",
    "ABCAPITAL",
    "ABFRL",
    "ADANIENT",
    "ADANIGREEN",
    "ADANIPORTS",
    "ADANIPOWER",
    "AMBUJACEM",
    "APOLLOHOSP",
    "ASHOKLEY",
    "ASIANPAINT",
    "AUROPHARMA",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJAJFINSV",
    "BAJFINANCE",
    "BANKBARODA",
    "BEL",
    "BERGEPAINT",
    "BHARTIARTL",
    "BOSCHLTD",
    "BPCL",
    "BRITANNIA",
    "CANBK",
    "CGPOWER",
    "CHOLAFIN",
    "CIPLA",
    "COALINDIA",
    "DABUR",
    "DIVISLAB",
    "DLF",
    "DRREDDY",
    "EICHERMOT",
    "ETERNAL",
    "GAIL",
    "GODREJCP",
    "GRASIM",
    "HAL",
    "HAVELLS",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "INDHOTEL",
    "INDIGO",
    "INDUSINDBK",
    "INFY",
    "IOC",
    "IRCTC",
    "ITC",
    "JINDALSTEL",
    "JIOFIN",
    "JSWENERGY",
    "JSWSTEEL",
    "KOTAKBANK",
    "LT",
    "LODHA",
    "LTIM",
    "M&M",
    "MARICO",
    "MARUTI",
    "MAXHEALTH",
    "MOTHERSON",
    "NESTLEIND",
    "NTPC",
    "ONGC",
    "PAYTM",
    "PIDILITIND",
    "PNB",
    "POLYCAB",
    "POWERGRID",
    "RECLTD",
    "RELIANCE",
    "SBICARD",
    "SBILIFE",
    "SBIN",
    "SHREECEM",
    "SHRIRAMFIN",
    "SIEMENS",
    "SUNPHARMA",
    "TATACONSUM",
    "TATAMOTORS",
    "TATAPOWER",
    "TATASTEEL",
    "TCS",
    "TECHM",
    "TITAN",
    "TORNTPHARM",
    "TRENT",
    "TVSMOTOR",
    "ULTRACEMCO",
    "VEDL",
    "WIPRO",
    "ZYDUSLIFE",
]


def main():

    db = SessionLocal()

    try:

        inserted = 0
        skipped = 0

        for symbol_name in NIFTY100:

            existing = (
                db.query(Symbol)
                .filter(
                    Symbol.symbol == symbol_name
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            symbol = Symbol(
                symbol=symbol_name,
                company_name=symbol_name,
                exchange="NSE",
            )

            db.add(symbol)

            inserted += 1

        db.commit()

        print("\n" + "=" * 60)
        print("NIFTY100 SEED COMPLETE")
        print("=" * 60)
        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")

    except Exception as e:

        db.rollback()

        print("\nERROR")
        print(str(e))

    finally:

        db.close()


if __name__ == "__main__":
    main()