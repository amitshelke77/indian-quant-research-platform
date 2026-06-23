class MarketScreenerService:

    @staticmethod
    def classify(
        close_price,
        ema50,
        trend_state,
        structure_score,
        swing_high_price,
        score=None,
    ):

        structure_score = (
            structure_score
            if structure_score is not None
            else 0
        )

        # ELITE LEADERS

        if (
            trend_state == 1
            and structure_score >= 40
            and (
                score is None
                or score >= 80
            )
        ):
            return "ELITE_LEADER"

        # LONG TERM LEADERS

        if (
            trend_state == 1
            and structure_score >= 20
            and ema50 is not None
            and close_price > ema50
        ):
            return "LONG_TERM_LEADER"

        # MID TERM

        if (
            trend_state == 1
            and structure_score >= 10
            and ema50 is not None
            and close_price > ema50
        ):
            return "MID_TERM_OPPORTUNITY"

        # BREAKOUT

        if (
            swing_high_price is not None
            and close_price > swing_high_price
        ):
            return "SHORT_TERM_BREAKOUT"

        # AVOID

        if (
            trend_state == -1
            and structure_score < 0
        ):
            return "AVOID"

        return "WATCHLIST"