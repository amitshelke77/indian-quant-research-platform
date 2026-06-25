import argparse
from pathlib import Path

import pandas as pd

import backend.models

from backend.core.database import SessionLocal
from backend.models.pattern_signal import PatternSignal
from backend.models.symbol import Symbol


def safe_div(a, b):
    if b in (0, None):
        return None
    return a / b


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pattern",
        default="ROUNDING_BOTTOM_V5",
        help="Pattern name or ALL",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Output file",
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:

        query = (
            db.query(
                PatternSignal,
                Symbol.symbol,
            )
            .join(
                Symbol,
                PatternSignal.symbol_id == Symbol.id,
            )
        )

        if args.pattern.upper() != "ALL":

            query = query.filter(
                PatternSignal.pattern_name == args.pattern
            )

        query = query.order_by(
            PatternSignal.trading_date
        )

        rows = query.all()

        if not rows:

            print("No trades found.")
            return

        data = []

        for signal, symbol in rows:

            trend_strength = None

            if (
                signal.ema50
                and signal.ema200
            ):

                trend_strength = (
                    (signal.ema50 - signal.ema200)
                    / signal.ema200
                ) * 100

            risk_pct = None
            reward_pct = None
            rr = None

            if (
                signal.entry_price
                and signal.stop_loss
            ):

                risk_pct = (
                    (signal.entry_price - signal.stop_loss)
                    / signal.entry_price
                ) * 100

            if (
                signal.entry_price
                and signal.target_price
            ):

                reward_pct = (
                    (signal.target_price - signal.entry_price)
                    / signal.entry_price
                ) * 100

            if (
                risk_pct
                and reward_pct
            ):

                rr = reward_pct / risk_pct

            exit_price = None

            if (
                signal.entry_price
                and signal.return_pct is not None
            ):

                exit_price = (
                    signal.entry_price
                    * (
                        1
                        + signal.return_pct / 100
                    )
                )

            data.append(
                {
                    "Symbol": symbol,
                    "Date": signal.trading_date,
                    "Pattern": signal.pattern_name,
                    "Confidence": signal.confidence,
                    "RSI": signal.rsi,
                    "Volume Ratio": signal.volume_ratio,
                    "EMA50": signal.ema50,
                    "EMA200": signal.ema200,
                    "Trend Strength %": trend_strength,
                    "Entry": signal.entry_price,
                    "Stop": signal.stop_loss,
                    "Target": signal.target_price,
                    "Risk %": risk_pct,
                    "Reward %": reward_pct,
                    "Risk:Reward": rr,
                    "Exit": exit_price,
                    "Return %": signal.return_pct,
                    "Holding Days": signal.holding_days,
                    "Outcome": signal.outcome,
                }
            )

        df = pd.DataFrame(data)

        output_dir = Path("research")
        output_dir.mkdir(exist_ok=True)

        if args.output:

            output = Path(args.output)

        else:

            name = (
                args.pattern
                if args.pattern.upper() != "ALL"
                else "ALL"
            )

            output = output_dir / f"trade_ledger_{name}.xlsx"

        csv_output = output.with_suffix(".csv")

        df.to_csv(
            csv_output,
            index=False,
        )

        df.to_excel(
            output,
            index=False,
        )

        print()
        print("=" * 70)
        print("TRADE LEDGER EXPORTED")
        print("=" * 70)
        print(f"Pattern      : {args.pattern}")
        print(f"Trades       : {len(df)}")
        print(f"CSV          : {csv_output}")
        print(f"Excel        : {output}")
        print(
            f"Average Return : {df['Return %'].mean():.2f}%"
        )
        print(
            f"Average Hold   : {df['Holding Days'].mean():.2f} days"
        )
        print("=" * 70)

    finally:

        db.close()


if __name__ == "__main__":
    main()