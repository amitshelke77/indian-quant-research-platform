from datetime import timedelta

import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.pattern_signal import PatternSignal


INITIAL_CAPITAL = 1_000_000

POSITION_SIZE = 50_000

PATTERN = "ROUNDING_BOTTOM_V5"


def main():

    db = SessionLocal()

    try:

        trades = (
            db.query(PatternSignal)
            .filter(
                PatternSignal.pattern_name == PATTERN
            )
            .filter(
                PatternSignal.return_pct != None
            )
            .order_by(
                PatternSignal.trading_date
            )
            .all()
        )

        print(f"Trades loaded: {len(trades)}")

        cash = INITIAL_CAPITAL

        open_positions = []

        completed = []

        for trade in trades:

            current_date = trade.trading_date

            # Close finished trades
            still_open = []

            for pos in open_positions:

                if pos["exit_date"] <= current_date:

                    cash += pos["exit_value"]

                    completed.append(pos)

                else:

                    still_open.append(pos)

            open_positions = still_open

            # Skip if insufficient cash
            if cash < POSITION_SIZE:

                continue

            cash -= POSITION_SIZE

            exit_value = POSITION_SIZE * (
                1 + trade.return_pct / 100
            )

            exit_date = (
                trade.trading_date
                + timedelta(days=trade.holding_days)
            )

            open_positions.append(
                {
                    "entry_date": trade.trading_date,
                    "exit_date": exit_date,
                    "invested": POSITION_SIZE,
                    "exit_value": exit_value,
                    "return_pct": trade.return_pct,
                }
            )

        # Close remaining positions
        for pos in open_positions:

            cash += pos["exit_value"]

            completed.append(pos)

        df = pd.DataFrame(completed)

        total_return = (
            (cash - INITIAL_CAPITAL)
            / INITIAL_CAPITAL
        ) * 100

        winners = (
            df["return_pct"] > 0
        ).sum()

        losers = (
            df["return_pct"] <= 0
        ).sum()

        print()
        print("=" * 70)
        print("PORTFOLIO BACKTEST V1")
        print("=" * 70)
        print(f"Pattern            : {PATTERN}")
        print(f"Trades             : {len(df)}")
        print(f"Winners            : {winners}")
        print(f"Losers             : {losers}")
        print(f"Initial Capital    : ₹{INITIAL_CAPITAL:,.0f}")
        print(f"Final Capital      : ₹{cash:,.2f}")
        print(f"Total Return       : {total_return:.2f}%")
        print(f"Average Trade      : {df['return_pct'].mean():.2f}%")
        print("=" * 70)

    finally:

        db.close()


if __name__ == "__main__":
    main()