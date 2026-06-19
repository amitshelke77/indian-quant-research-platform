import pandas as pd


class GannStructureScoreStrategy:

    def build_signals(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        signals = []

        in_position = False

        for _, row in df.iterrows():

            structure_score = row[
                "structure_score"
            ]

            ema50 = row["ema50"]

            if pd.isna(ema50):
                signals.append(0)
                continue

            # ENTRY

            if (
                not in_position
                and structure_score >= 3
                and row["Close"] > ema50
            ):
                in_position = True

            # EXIT

            elif (
                in_position
                and (
                    structure_score <= 0
                    or row["Close"] < ema50
                )
            ):
                in_position = False

            signals.append(
                1 if in_position else 0
            )

        df["signal"] = signals

        return df