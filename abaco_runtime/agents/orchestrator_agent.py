from typing import Dict, Any
from .data_quality_guardian_ai import DataQualityGuardianAgent
from .data_cleaning_agent import DataCleaningAgent
from .reporting_agent import ReportingAgent

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
        self.reporter = ReportingAgent()

    def run(self, context: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the data processing pipeline.

        1. Assesses data quality.
        2. If quality is low, triggers the cleaning agent and verifies the result.
        3. Returns the final, processed data and a summary of actions.

        Args:
            context: The initial execution context.
            data: The raw dataset to be processed.

        Returns:
            A dictionary with the final data and a log of the orchestration steps.
        """
        # Centralized configuration for the workflow
        config = {
            "quality_thresholds": {
                "warning": 85.0,
                "reject": 70.0
            }
        }
        # The context will carry the configuration for other agents
        run_context = {**context, **config}

        orchestration_log = []

        # Step 1: Run the Data Quality Guardian
        orchestration_log.append("Action: Performing initial data quality assessment.")
        quality_report = self.quality_guardian.run(run_context, data)
        orchestration_log.append(f"  > Result: Initial status is {quality_report['status']} with score {quality_report['score']}.")

        processed_data = data

        # Step 2: Decide whether to trigger the Data Cleaning Agent
        if quality_report["score"] < config["quality_thresholds"]["warning"]:
            orchestration_log.append("Action: Triggering Data Cleaning Agent due to low quality.")
            cleaning_report = self.data_cleaner.run(quality_report.get("issues", []), processed_data)
            processed_data = {"records": cleaning_report.get("records")}
            orchestration_log.append(f"  > Result: Data cleaning complete. {len(cleaning_report.get('log',[]))} issues addressed.")

            # Step 3: Verify cleaning by running quality check again
            orchestration_log.append("Action: Verifying data quality post-cleaning.")
            final_quality_report = self.quality_guardian.run(run_context, processed_data)
            orchestration_log.append(f"  > Result: Final status is {final_quality_report['status']} with score {final_quality_report['score']}.")
        else:
            orchestration_log.append("Action: Data quality approved. No cleaning needed.")

        # Step 4: Generate final report
        orchestration_log.append("Action: Generating final report.")
        final_report = self.reporter.run(run_context, orchestration_log)

        return {
            "final_data": processed_data,
            "log": orchestration_log,
            "human_readable_report": final_report
        }