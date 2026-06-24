import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV

from backend.patterns.double_bottom import DoubleBottomDetector
from backend.patterns.rounding_bottom import (
    RoundingBottomDetector,
)

from backend.patterns.rounding_bottom_v5 import (
    RoundingBottomDetectorV5,
)

from backend.patterns.double_bottom import (
    DoubleBottomDetector,
)

from backend.patterns.rounding_bottom_v2 import (
    RoundingBottomDetectorV2,
)

from backend.patterns.cup_handle import (
    CupHandleDetector,
)

from backend.patterns.bull_flag import (
    BullFlagDetector,
)

from backend.repositories.pattern_signal_repository import (
    PatternSignalRepository,
)

from backend.patterns.true_rounding_bottom import (
    TrueRoundingBottomDetector,
)

from backend.patterns.rounding_bottom_v4 import (
    RoundingBottomDetectorV4,
)

from backend.patterns.rounding_bottom_v3 import (
    RoundingBottomDetectorV3,
)

def safe_float(value):
    
    if pd.isna(value):
        return None

    return float(value)


def main():

    db = SessionLocal()

    try:

        detectors = [

            RoundingBottomDetector(),

            RoundingBottomDetectorV2(),

            DoubleBottomDetector(),

            RoundingBottomDetectorV3(),
            
            CupHandleDetector(),

            TrueRoundingBottomDetector(),
            
            RoundingBottomDetectorV5(),

            RoundingBottomDetectorV4(),

            BullFlagDetector(),
        ]

        repo = (
            PatternSignalRepository(
                db
            )
        )

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        total_signals = 0

        for symbol in symbols:

            print(
                f"\nScanning {symbol.symbol}"
            )

            rows = (
                db.query(OHLCV)
                .filter(
                    OHLCV.symbol_id
                    == symbol.id
                )
                .order_by(
                    OHLCV.trading_date
                )
                .all()
            )

            if len(rows) < 150:

                print(
                    "Not enough data"
                )

                continue

            df = pd.DataFrame(
                [
                    {
                        "Date":
                            r.trading_date,
                        "Open":
                            r.open,
                        "High":
                            r.high,
                        "Low":
                            r.low,
                        "Close":
                            r.close,
                        "Volume":
                            r.volume,
                    }
                    for r in rows
                ]
            )

            signals = []

            for detector in detectors:

                detector_signals = (
                    detector.detect(df)
                )

                signals.extend(
                    detector_signals
                )

            inserted = 0

            for signal in signals:

                try:

                    if repo.exists(
                        symbol.id,
                        signal["date"],
                        signal["pattern"],
                    ):
                        continue

                except TypeError:

                    if repo.exists(
                        symbol.id,
                        signal["date"],
                    ):
                        continue

                repo.insert(

                    symbol_id=symbol.id,

                    trading_date=
                    signal["date"],

                    pattern_name=
                    signal["pattern"],

                    confidence=
                    safe_float(
                        signal["confidence"]
                    ),

                    entry_price=
                    safe_float(
                        signal["entry"]
                    ),

                    stop_loss=
                    safe_float(
                        signal["stop_loss"]
                    ),

                    target_price=
                    safe_float(
                        signal["target"]
                    ),

                    rsi=
                    safe_float(
                        signal.get("rsi")
                    ),

                     volume_ratio=
                     safe_float(
                         signal.get(
                             "volume_ratio"
                         )
                    ),

                    ema50=
                    safe_float(
                        signal.get("ema50")
                    ),

                    ema200=
                    safe_float(
                        signal.get("ema200")
                    ),


                )

                inserted += 1

            repo.commit()

            total_signals += inserted

            print(
                f"Inserted: {inserted}"
            )

        print("\n")
        print("=" * 80)
        print(
            f"TOTAL SIGNALS INSERTED: {total_signals}"
        )
        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()