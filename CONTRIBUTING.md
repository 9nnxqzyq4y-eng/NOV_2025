# Contributing to the ABACO Platform

First off, thank you for considering contributing! This document provides guidelines for contributing to this project.

## Local Development Environment Setup

To ensure a smooth development experience, you need several tools and VS Code extensions configured on your local machine.

### 1. Core Dependencies

- **Node.js:** Use version 20.x. We recommend using `nvm` (Node Version Manager).
- **Python:** Use version 3.11.
- **Git:** For version control.

### 2. VS Code Extensions & Configuration

This project is optimized for Visual Studio Code. Please install the following extensions:

- **ESLint:** For JavaScript/TypeScript linting.
- **Prettier - Code formatter:** For consistent code style.
- **SonarLint:** (Optional) To connect to SonarCloud for live issue reporting. In the VS Code settings, configure the connection to the `jenineferderas` organization on SonarCloud.
- **CS-Script:** (Optional, for C# scripting) If you use this extension, you must install the required .NET tools. See the extension's documentation for installation instructions.

### 3. Authenticating CLIs

For full functionality, including deployment and data pipeline runs, you must authenticate several command-line interfaces (CLIs):

- **GitHub CLI:** `gh auth login`
- **Vercel CLI:** `vercel login`
- **Supabase CLI:** `supabase login`
- **Hugging Face CLI:** (Optional) `huggingface-cli login` to avoid API rate limits.
- **Google Cloud CLI:** (Optional) `gcloud auth login` if you need to interact with GCP resources.