from typing import Dict, Any
from .data_quality_guardian_ai import DataQualityGuardianAgent
from .data_cleaning_agent import DataCleaningAgent

class OrchestratorAgent:
    """
    An AI agent that orchestrates workflows by triggering other agents.

    Personality:
    - A manager or director.
    - Decisive and goal-oriented.
    - Understands the capabilities of other agents and delegates tasks accordingly.
    """

    def __init__(self):
        """Initializes the orchestrator with the agents it can command."""
        self.quality_guardian = DataQualityGuardianAgent()
        self.data_cleaner = DataCleaningAgent()

    def run(self, context: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the data processing pipeline.

        1. Assesses data quality.
        2. If quality is low, triggers the cleaning agent.
        3. Returns the final, processed data and a summary of actions.

        Args:
            context: The initial execution context.
            data: The raw dataset to be processed.

        Returns:
            A dictionary with the final data and a log of the orchestration steps.
        """
        orchestration_log = []

        # Step 1: Run the Data Quality Guardian
        orchestration_log.append("Action: Assessing data quality.")
        quality_report = self.quality_guardian.run(context, data)
        orchestration_log.append(f"Result: Quality status is {quality_report['status']} with score {quality_report['score']}.")

        final_data = data

        # Step 2: Decide whether to trigger the Data Cleaning Agent
        if quality_report["status"] in ["WARNING", "REJECTED"]:
            orchestration_log.append("Action: Triggering Data Cleaning Agent due to low quality.")
            cleaning_context = {"issues": quality_report.get("issues", [])}
            cleaning_report = self.data_cleaner.run(cleaning_context, data)
            final_data = {"records": cleaning_report.get("records")}
            orchestration_log.append("Result: Data cleaning complete.")
            orchestration_log.extend(cleaning_report.get("log", []))
        else:
            orchestration_log.append("Result: Data quality approved. No cleaning needed.")

        return {"final_data": final_data, "log": orchestration_log}