"""Data Cleaning Agent for fixing identified data quality issues."""

from typing import Dict, Any, List
class DataCleaningAgent:
    """
    An AI agent responsible for cleaning and repairing data.
    Personality:
    - Diligent and methodical.
    - Focuses on fixing specific, identified issues in a dataset.
    - Aims to improve data quality to an acceptable standard.
    def __init__(self):
        """Initializes the agent and maps issue types to handler methods."""
        self.issue_handlers = {
            "MISSING_VALUE": self._fix_missing_value,
            "INVALID_FORMAT": self._fix_invalid_format,
        }
    def _fix_missing_value(self, record: Dict[str, Any], field: str, record_index: int) -> str:
        """Fills a missing value with a standard placeholder."""
        record[field] = "N/A"
        return f"Fixed: Filled missing value in record {record_index} for field '{field}'."
    def _fix_invalid_format(self, record: Dict[str, Any], field: str, record_index: int) -> str:
        """Handles invalid data formats. Currently nullifies invalid emails."""
        if field == "email":
            record[field] = None
            return f"Fixed: Nullified invalid email in record {record_index}."
        return (f"Info: No fix applied for invalid format on field '{field}' "
                f"in record {record_index}.")
    def run(self, issues: List[Dict[str, Any]], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans the provided dataset based on a list of identified issues.
        Args:
            issues: A list of dictionaries describing the issues to fix.
            data: The dataset to be cleaned.
        Returns:
            A dictionary containing the cleaned dataset.
        records = data.get("records", [])
        if not records or not issues:
            # Nothing to clean or no instructions on what to clean
            return data
        # Create a deep copy to avoid modifying the original data
        cleaned_records = [record.copy() for record in records]
        cleaning_log = []
        # Process each issue identified by the guardian
        for issue in issues:
            if (
                not (record_index := issue.get("record_index")) or
                not isinstance(field := issue.get("field"), str) or
                not (issue_type := issue.get("issue_type"))
            ):
                continue
            handler = self.issue_handlers.get(issue_type)
            if handler:
                log_message = handler(cleaned_records[record_index], field, record_index)
                cleaning_log.append(log_message)
        return {
            "records": cleaned_records,
            "status": "cleaned",
            "log": cleaning_log,
