import re
from typing import Dict, Any, List

class DataQualityGuardianAgent:
    """
    An AI agent that acts as a guardian for data quality.

    Personality:
    - Meticulous and precise.
    - Focuses on identifying inconsistencies, missing values, and outliers.
    - Provides a clear, quantifiable quality score and a definitive status.
    """

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
        if not isinstance(records, list) or not records:
            return {
                "score": 0.0,
                "status": "REJECTED",
                "details": "Invalid or empty dataset. Expected a dictionary with a 'records' key containing a list.",
            }

        issues: List[Dict[str, Any]] = []
        seen_ids = set()

        # Basic checks: missing values, email format, duplicates
        for i, record in enumerate(records):
            # Check for duplicate IDs
            record_id = record.get("id")
            if record_id is not None:
                if record_id in seen_ids:
                    issues.append({
                        "record_index": i,
                        "field": "id",
                        "issue_type": "DUPLICATE_ID",
                        "value": record_id,
                        "message": f"Duplicate ID '{record_id}' found at record {i+1}."
                    })
                else:
                    seen_ids.add(record_id)

            for key, value in record.items():
                # Check for missing values
                if value is None:
                    issues.append({
                        "record_index": i,
                        "field": key,
                        "issue_type": "MISSING_VALUE",
                        "message": f"Missing value for '{key}' in record {i+1}."
                    })

                # Check email format
                if key == "email" and isinstance(value, str):
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                        issues.append({
                            "record_index": i,
                            "field": "email",
                            "issue_type": "INVALID_FORMAT",
                            "value": value,
                            "message": f"Invalid email format for '{value}' in record {i+1}."
                        })

        # Calculate score
        total_possible_issues = len(records) * len(records[0].keys()) if records else 0
        score = 100.0
        if total_possible_issues > 0:
            # Penalize score more heavily for more issues
            penalty_per_issue = 100.0 / total_possible_issues
            score -= len(issues) * penalty_per_issue
            score = max(0.0, score) # Ensure score doesn't go below 0

        # Determine status
        if score == 100.0:
            status = "APPROVED"
            details = "Dataset passed all quality checks."
        elif score >= 70.0:
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
