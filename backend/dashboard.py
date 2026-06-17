import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd

import backend.models

from backend.core.database import SessionLocal

from backend.models.symbol import Symbol
from backend.models.ohlcv import OHLCV
from backend.models.gann_analysis import GannAnalysis
from backend.models.technical_indicator import TechnicalIndicator
from backend.models.backtest_result import BacktestResult


st.set_page_config(
    page_title="Indian Quant Research Platform",
    layout="wide",
)


def calculate_score(
    close_price,
    ema50,
    rsi14,
    trend_state,
    swing_high_price,
):

    score = 0

    if trend_state == 1:
        score += 40

    if (
        ema50 is not None
        and ema50 > 0
        and close_price > ema50
    ):

        score += 30

        ema_distance = (
            (close_price - ema50)
            / ema50
        ) * 100

        if ema_distance > 10:
            score += 10

        elif ema_distance > 5:
            score += 5

    if rsi14 is not None:

        if rsi14 >= 60:
            score += 20

        elif rsi14 >= 55:
            score += 15

        elif rsi14 >= 50:
            score += 10

        if rsi14 >= 80:
            score += 10

        elif rsi14 >= 70:
            score += 5

    if (
        swing_high_price is not None
        and close_price > swing_high_price
    ):
        score += 10

    return min(score, 100)


def signal_from_score(score):

    if score >= 70:
        return "BUY"

    elif score <= 20:
        return "SELL"

    return "HOLD"


@st.cache_data(ttl=60)
def load_screener():

    db = SessionLocal()

    try:

        symbols = (
            db.query(Symbol)
            .order_by(Symbol.symbol)
            .all()
        )

        results = []

        for symbol in symbols:

            rows = (
                db.query(
                    OHLCV,
                    TechnicalIndicator,
                    GannAnalysis,
                )
                .join(
                    TechnicalIndicator,
                    (
                        OHLCV.symbol_id
                        == TechnicalIndicator.symbol_id
                    )
                    &
                    (
                        OHLCV.trading_date
                        == TechnicalIndicator.trading_date
                    )
                )
                .join(
                    GannAnalysis,
                    (
                        OHLCV.symbol_id
                        == GannAnalysis.symbol_id
                    )
                    &
                    (
                        OHLCV.trading_date
                        == GannAnalysis.trading_date
                    )
                )
                .filter(
                    OHLCV.symbol_id
                    == symbol.id
                )
                .order_by(
                    OHLCV.trading_date.desc()
                )
                .limit(1)
                .all()
            )

            if not rows:
                continue

            o, t, g = rows[0]

            score = calculate_score(
                o.close,
                t.ema50,
                t.rsi14,
                g.trend_state,
                g.swing_high_price,
            )

            signal = signal_from_score(
                score
            )

            results.append(
                {
                    "Symbol": symbol.symbol,
                    "Close": round(o.close, 2),
                    "EMA50": round(t.ema50, 2)
                    if t.ema50
                    else None,
                    "RSI": round(t.rsi14, 2)
                    if t.rsi14
                    else None,
                    "Trend": g.trend_state,
                    "Score": score,
                    "Signal": signal,
                }
            )

        return pd.DataFrame(results)

    finally:
        db.close()


@st.cache_data(ttl=60)
def load_strategy_stats():

    db = SessionLocal()

    try:

        rows = (
            db.query(
                BacktestResult.strategy_name,
            )
            .all()
        )

        if not rows:
            return pd.DataFrame()

        query = """
        SELECT
            strategy_name,
            AVG(cagr) AS avg_cagr,
            AVG(sharpe_ratio) AS avg_sharpe,
            AVG(alpha) AS avg_alpha,
            AVG(max_drawdown) AS avg_drawdown
        FROM backtest_results
        GROUP BY strategy_name
        ORDER BY avg_sharpe DESC
        """

        return pd.read_sql(
            query,
            db.bind,
        )

    finally:
        db.close()


st.title(
    "Indian Quant Research Platform"
)

st.markdown("---")

screener_df = load_screener()

buy_count = len(
    screener_df[
        screener_df["Signal"] == "BUY"
    ]
)

sell_count = len(
    screener_df[
        screener_df["Signal"] == "SELL"
    ]
)

hold_count = len(
    screener_df[
        screener_df["Signal"] == "HOLD"
    ]
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "BUY Signals",
    buy_count,
)

c2.metric(
    "HOLD Signals",
    hold_count,
)

c3.metric(
    "SELL Signals",
    sell_count,
)

st.markdown("---")

st.header(
    "Current Screener"
)

st.dataframe(
    screener_df.sort_values(
        "Score",
        ascending=False,
    ),
    width="stretch",
)

st.markdown("---")

st.header(
    "Top Buy Candidates"
)

st.dataframe(
    screener_df[
        screener_df["Signal"] == "BUY"
    ]
    .sort_values(
        "Score",
        ascending=False,
    ),
    width="stretch",
)

st.markdown("---")

st.header(
    "Strategy Rankings"
)

strategy_df = load_strategy_stats()

if not strategy_df.empty:

    st.dataframe(
        strategy_df,
        width="stretch",
    )

else:

    st.info(
        "No backtest results found."
    )

st.markdown("---")

st.success(
    "Dashboard connected to PostgreSQL successfully."
)