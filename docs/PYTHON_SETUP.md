# Python Environment Setup (Optional)

## Overview

This is primarily a **Next.js/TypeScript project**. Python support is optional for the Streamlit dashboard and data processing utilities.

## Status

- ✅ **Primary**: Next.js/TypeScript (fully configured)
- ⚠️ **Optional**: Python (Streamlit, ML features)
- 🔇 **Disabled in VS Code**: Flake8, Pylint, Pylance

## Why Python Linting is Disabled

Per the Copilot instructions, Python dependencies are managed separately in a virtual environment. VS Code linting is disabled to avoid:

- Connection errors to unavailable linters
- Conflicts between node and Python environments
- Unnecessary warnings in a TypeScript-first project

## Using Python (Optional)

### Setup Virtual Environment

```bash
# Create Python virtual environment
python3 -m venv streamlit_env

# Activate (macOS/Linux)
source streamlit_env/bin/activate

# Activate (Windows)
streamlit_env\Scripts\activate

### Install Dependencies

# From streamlit_requirements.txt
pip install -r streamlit_requirements.txt

### Run Streamlit Dashboard

# Ensure virtual environment is activated

# Run Streamlit app
streamlit run streamlit_app.py

### Deactivate Environment

deactivate

## Project Structure

