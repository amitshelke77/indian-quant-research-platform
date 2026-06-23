class CombinedScoreService:

    @staticmethod
    def calculate(
        structure_score,
        recent_structure_score,
    ):

        structure_score = (
            structure_score
            if structure_score is not None
            else 0
        )

        recent_structure_score = (
            recent_structure_score
            if recent_structure_score is not None
            else 0
        )

        return (
            structure_score * 2
            +
            recent_structure_score * 5
        )