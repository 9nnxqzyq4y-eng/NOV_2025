from typing import Dict, Any

class DataQualityGuardianAgent:
    """
    An AI agent for assessing data quality.
    """

    def run(self, context: Dict[str, Any], data: Dict[str, Any]) -> str:
        """
        Runs the data quality check.
        """
        # For demo purposes, we'll return a hardcoded quality score.
        # In a real implementation, this would involve more complex logic.
        return "quality score: 87.5/100 - APPROVED"
