from typing import Dict, Any, List

class DataCleaningAgent:
    """
    An AI agent responsible for cleaning and repairing data.

    Personality:
    - Diligent and methodical.
    - Focuses on fixing specific, identified issues in a dataset.
    - Aims to improve data quality to an acceptable standard.
    """

    def run(self, context: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans the provided dataset based on a list of identified issues.

        Args:
            context: The execution context, containing the list of issues to fix.
            data: The dataset to be cleaned.

        Returns:
            A dictionary containing the cleaned dataset.
        """
        records = data.get("records", [])
        issues = context.get("issues", [])

        if not records or not issues:
            # Nothing to clean or no instructions on what to clean
            return data
        
        # Create a deep copy to avoid modifying the original data
        cleaned_records = [record.copy() for record in records]
        cleaning_log = []
        
        # Process each issue identified by the guardian
        for issue in issues:
            record_index = issue.get("record_index")
            field = issue.get("field")
            issue_type = issue.get("issue_type")
            
            if record_index is None or field is None:
                continue
                
            record_to_clean = cleaned_records[record_index]
            
            if issue_type == "MISSING_VALUE":
                record_to_clean[field] = "N/A" # Use a standard placeholder
                cleaning_log.append(f"Fixed: Filled missing value in record {record_index} for field '{field}'.")
            elif issue_type == "INVALID_FORMAT" and field == "email":
                record_to_clean[field] = None # Nullify invalid emails
                cleaning_log.append(f"Fixed: Nullified invalid email in record {record_index}.")
            # Note: DUPLICATE_ID is not handled here as it may require business logic to resolve.
            
        return {"records": cleaned_records, "status": "cleaned", "log": cleaning_log}