import sys
import subprocess

from backend.core.database import SessionLocal
from backend.models.symbol import Symbol


def main():
    db = SessionLocal()

    try:
        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        print(f"Found {len(symbols)} symbols\n")

        success = 0
        failed = 0

        for symbol in symbols:

            print("=" * 60)
            print(f"Loading {symbol.symbol}")
            print("=" * 60)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "backend.load_symbol",
                    symbol.symbol,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                success += 1
                print(result.stdout)
            else:
                failed += 1
                print(result.stderr)

        print("\n" + "=" * 60)
        print("LOAD COMPLETE")
        print("=" * 60)
        print(f"Successful: {success}")
        print(f"Failed    : {failed}")

    finally:
        db.close()


if __name__ == "__main__":
    main()