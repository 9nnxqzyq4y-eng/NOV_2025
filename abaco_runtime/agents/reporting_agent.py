"""Reporting Agent for generating human-readable summaries."""

from typing import List
class ReportingAgent:
    """
    An AI agent that summarizes process logs into human-readable reports.
    Personality:
    - A clear and concise communicator.
    - Focuses on summarizing results and actions for human review.
    - Translates technical logs into business-friendly summaries.
    def run(self, data: List[str]) -> str:
        """
        Generates a human-readable report from a log of actions.
        Args:
            data: A list of log strings from the orchestration process.
        Returns:
            A formatted string report.
        report_lines = ["# Data Processing Report", "---"]
        initial_assessment = next((line for line in data if "Initial status" in line), None)
        final_assessment = next((line for line in data if "Final status" in line), None)
        cleaning_action = next((line for line in data if "Data cleaning complete" in line), None)
        if initial_assessment:
            report_lines.append(f"## 1. Initial Quality Assessment\n- {initial_assessment.strip()}")
        if cleaning_action:
            report_lines.append(f"\n## 2. Cleaning Action\n- {cleaning_action.strip()}")
        if final_assessment:
            report_lines.append(f"\n## 3. Final Quality Verification\n- {final_assessment.strip()}")
        report_lines.append("\n---\n**End of Report.**")
        return "\n".join(report_lines)
