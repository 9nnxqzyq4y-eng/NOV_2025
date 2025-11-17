import re
import math
from typing import Dict, Any, List

class DataQualityGuardianAgent:
    """
    An AI agent that acts as a guardian for data quality.

    Personality:
    - Meticulous and precise.
    - Focuses on identifying inconsistencies, missing values, and outliers.
    - Provides a clear, quantifiable quality score and a definitive status.
    """

    def _validate_records(self, records: Any) -> bool:
        """Checks if the records object is a non-empty list."""
        return isinstance(records, list) and records

    def _find_issues(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Iterates through records to find all data quality issues."""
        issues: List[Dict[str, Any]] = []
        seen_ids = set()

        for i, record in enumerate(records):
            # Check for duplicate IDs
            record_id = record.get("id")
            if record_id is not None:
                if record_id in seen_ids:
                    issues.append({
                        "record_index": i, "field": "id", "issue_type": "DUPLICATE_ID",
                        "value": record_id, "message": f"Duplicate ID '{record_id}' found at record {i+1}."
                    })
                else:
                    seen_ids.add(record_id)

            # Check for issues in each field
            for key, value in record.items():
                if value is None:
                    issues.append({
                        "record_index": i, "field": key, "issue_type": "MISSING_VALUE",
                        "message": f"Missing value for '{key}' in record {i+1}."
                    })
                elif key == "email" and isinstance(value, str) and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    issues.append({
                        "record_index": i, "field": "email", "issue_type": "INVALID_FORMAT",
                        "value": value, "message": f"Invalid email format for '{value}' in record {i+1}."
                    })
        return issues

    def _calculate_score(self, records: List[Dict[str, Any]], issues: List[Dict[str, Any]]) -> float:
        """Calculates a quality score based on the number of issues found."""
        total_possible_issues = len(records) * len(records[0].keys()) if records else 0
        if total_possible_issues == 0:
            return 100.0
        
        penalty_per_issue = 100.0 / total_possible_issues
        score = 100.0 - (len(issues) * penalty_per_issue)
        return max(0.0, score)

    def run(self, context: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the data quality assessment on the given dataset.

        In a real implementation, this method would contain logic to:
        1. Check for missing values.
        2. Validate data types and formats (e.g., emails, dates).
        3. Detect outliers.
        4. Check for inconsistencies or duplicates.
        5. Calculate a composite quality score based on these checks.

        Args:
            context: The execution context, which might contain configuration
                     or metadata.
            data: The dataset to be analyzed, typically a dictionary or a
                  list of dictionaries.

        Returns:
            A dictionary containing the quality score, a status, and details.
        """
        records = data.get("records")
        # Return early to avoid deep nesting (Guard Clause)
        if not self._validate_records(records):
            return {
                "score": 0.0,
                "status": "REJECTED",
                "details": "Invalid or empty dataset. Expected a dictionary with a 'records' key containing a list.",
            }

        issues = self._find_issues(records)
        score = self._calculate_score(records, issues)
        
        # Get thresholds from context, with sensible defaults
        thresholds = context.get("quality_thresholds", {
            "warning": 85.0,
            "reject": 70.0
        })

        # Determine status
        if math.isclose(score, 100.0):
            status = "APPROVED"
            details = "Dataset passed all quality checks."
        elif score >= thresholds["reject"]:
            status = "WARNING"
            details = "Dataset has minor quality issues."
        else:
            status = "REJECTED"
            details = "Dataset has major quality issues."

        return {
            "score": round(score, 2),
            "status": status,
            "details": details,
            "issues": issues,
        }
