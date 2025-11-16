import os
from pathlib import Path

# List of file patterns and directories that usually do NOT belong in a clean production repository
SUSPICIOUS_PATTERNS = [
    ".ipynb_checkpoints", ".vscode", ".idea", ".pytest_cache", "__pycache__", "node_modules",
    ".DS_Store", "*.swp", "*.bak", "*.tmp", "*.log", "*.orig", "*.rej", "*.pyc", "*.pyo",
    "*.egg-info", ".env.local.backup", ".envrc", ".coverage", ".mypy_cache", ".tox", ".cache",
    "test*", "sample*", "demo*", "dummy*", "example*", "backup*", "old*", "junk*", "trash*",
    "hello.txt", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Dockerfile-checkpoint",
    "CLEANUP_REPORT-checkpoint.md", "components-checkpoint.json", "fix_merge_conflicts-checkpoint.sh"
]

def is_suspicious(file_path: Path) -> bool:
    # Check against directory patterns
    for part in file_path.parts:
        if part in [".ipynb_checkpoints", ".vscode", ".idea", ".pytest_cache", "__pycache__", "node_modules", ".cache", ".tox", ".mypy_cache"]:
             return True

    name = file_path.name.lower()
    # Check against file name patterns
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        elif pattern.endswith("*"):
            if name.startswith(pattern[:-1]):
                return True
        elif pattern == name:
            return True
    return False

def main():
    repo_root = Path(__file__).parent.parent
    print("🔎 Scanning for suspicious or out-of-place files in the repository...\n")
    suspicious = []
    for root, dirs, files in os.walk(repo_root):
        # Check directories
        for d in dirs:
            dir_path = Path(root) / d
            if is_suspicious(dir_path):
                suspicious.append(str(dir_path.relative_to(repo_root)))

        # Check files
        for f in files:
            file_path = Path(root) / f
            if is_suspicious(file_path):
                suspicious.append(str(file_path.relative_to(repo_root)))

    if suspicious:
        print("⚠️  The following files/folders may not belong in this repository:")
        # Use a set to get unique entries and then sort them
        for item in sorted(list(set(suspicious))):
            print(f"  - {item}")
        print("\nReview and remove these files if they are not needed for production.")
    else:
        print("✅ No suspicious or out-of-place files found. Repository looks clean.")

if __name__ == "__main__":
    main()