class ScoreService:

    @staticmethod
    def calculate_score(
        close_price,
        ema50,
        rsi14,
        trend_state,
        structure_score,
        swing_high_price,
    ):

        score = 0

        # Trend

        if trend_state == 1:
            score += 40

        # EMA

        if (
            ema50 is not None
            and ema50 > 0
            and close_price > ema50
        ):

            score += 20

            ema_distance = (
                (close_price - ema50)
                / ema50
            ) * 100

            if ema_distance > 10:
                score += 10

            elif ema_distance > 5:
                score += 5

        # RSI

        if rsi14 is not None:

            if rsi14 >= 60:
                score += 10

            elif rsi14 >= 50:
                score += 5

        # Structure Score

        if structure_score is not None:

            if structure_score >= 8:
                score += 20

            elif structure_score >= 6:
                score += 15

            elif structure_score >= 3:
                score += 10

            elif structure_score <= -6:
                score -= 15

        # Breakout

        if (
            swing_high_price is not None
            and close_price > swing_high_price
        ):
            score += 10

        return max(
            min(score, 100),
            0,
        )