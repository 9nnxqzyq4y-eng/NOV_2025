# Python Development Guide

## Overview

This is a **Next.js/TypeScript-first project** where Python support is optional for:

- Streamlit dashboards
- ML/AI feature exploration
- Data analysis and processing

## Project Status

| Component           | Status         | Notes                 |
| ------------------- | -------------- | --------------------- |
| Next.js/TypeScript  | ✅ Primary     | Fully configured      |
| Python/Streamlit    | ⚠️ Optional    | Manual setup required |
| Virtual Environment | ❌ Not created | User-managed          |
| VS Code Linting     | 🔇 Disabled    | Prevents conflicts    |

## Why Virtual Environment is Not Pre-created

Per **Copilot Instructions** (`/.github/copilot-instructions.md`):

 Python dependencies are managed **separately** in a virtual environment, isolated from the Node.js development environment.

This design choice provides:

- ✅ Complete isolation between Python and Node.js
- ✅ Cleaner development workflow
- ✅ No conflicting dependency versions
- ✅ Simplified CI/CD pipelines
- ✅ User controls when to activate Python

## Setting Up Python (When Needed)

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv streamlit_env

# Verify creation
ls -la streamlit_env/
# Should show: bin/, lib/, pyvenv.cfg

### Step 2: Activate Virtual Environment

# macOS/Linux
source streamlit_env/bin/activate

# Windows
streamlit_env\Scripts\activate

# Verify activation (prompt should show "(streamlit_env)")
which python
python --version

### Step 3: Install Dependencies

# From requirements file
pip install -r streamlit_requirements.txt

# Or manually
pip install streamlit pandas plotly supabase python-dotenv

### Step 4: Verify Installation

# Check if tools are available
which flake8
which pylint
which black
which pytest

# Run a quick test
python -c "import streamlit; print(streamlit.__version__)"

## Running Python Tools

All Python tools must be run **after activating the virtual environment**:

# ✅ CORRECT - Virtual environment activated
flake8 streamlit_app.py
pylint streamlit_app.py
black streamlit_app.py

# ❌ WRONG - No virtual environment
flake8 streamlit_app.py  # Command not found

## Common Workflows

### Running Streamlit Dashboard

# Activate environment

# Run dashboard
streamlit run streamlit_app.py

# Access at http://localhost:8501

### Linting Python Files

# Activate environment

# Run linters
flake8 streamlit_app.py --count --selectE9,F63,F7,F82
black streamlit_app.py --check

### Formatting Python Files

# Activate environment

# Auto-format with black

# Or use flake8 with autopep8
autopep8 --in-place --aggressive --aggressive streamlit_app.py

### Running Tests

# Activate environment

# Run pytest
pytest tests/

# With coverage
pytest --covstreamlit_app tests/

## Deactivating Virtual Environment

deactivate

# Verify (should not show "(streamlit_env)" in prompt)

## File Structure

