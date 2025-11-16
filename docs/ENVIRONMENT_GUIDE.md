# Environment Guide

## Primary Development Environment: Next.js/TypeScript

This is the **main focus** of the project.

### Quick Start

```bash
# Install dependencies
npm install

# Start development
npm run dev

# Quality checks
npm run quality-check

# Build
npm run build

### Key Commands

| Command                 | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `npm run dev`           | Start dev server on port 3000 (or 3001) |
| `npm run build`         | Production build                        |
| `npm run start`         | Start production server                 |
| `npm run lint`          | ESLint validation                       |
| `npm run type-check`    | TypeScript checking                     |
| `npm run quality-check` | All checks (type-check + lint + build)  |
| `npm run sonar`         | SonarQube analysis                      |

### Environment Variables

Create `.env.local` with:

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Optional
GROK_API_KEY=your-grok-key
GDRIVE_FOLDER_ID=your-folder-id

## Optional: Python/Streamlit Environment

Isolated Python environment for dashboard and ML features.

### Setup

# Create virtual environment
python3 -m venv streamlit_env

# Activate
source streamlit_env/bin/activate  # macOS/Linux
# or
streamlit_env\Scripts\activate  # Windows

# Install dependencies
pip install -r streamlit_requirements.txt

### Run Streamlit

# Ensure activated
source streamlit_env/bin/activate

# Run dashboard
streamlit run streamlit_app.py

# Access at http://localhost:8501

### Deactivate

deactivate

## VS Code Configuration

### TypeScript/Next.js (Primary)

- ✅ ESLint enabled and configured
- ✅ Prettier formatting enabled
- ✅ Tailwind CSS intellisense active
- ✅ TypeScript strict mode enforced

### Python (Optional)

- 🔇 Flake8 disabled (expected)
- 🔇 Pylint disabled (expected)
- 🔇 Pylance disabled (expected)
- ✅ Use virtual environment for development

**Why disabled?** Python is optional and managed separately. This prevents connection errors and keeps environments isolated.

## Running Both Simultaneously

Open two terminals:

# Terminal 1: Next.js Development
# → http://localhost:3000

# Terminal 2: Streamlit Dashboard
# → http://localhost:8501

## Common Issues

### Port Already in Use

# Use different port
PORT=3001 npm run dev

### Flake8 Connection Error

- ✅ This is expected and safe
- ✅ Already disabled in VS Code settings
- Use command-line tools if needed: `flake8 streamlit_app.py`

### Python Virtual Environment Not Found

# Create if missing

### Dependencies Issues

# Next.js
npm ci  # Clean install

# Python
pip install --upgrade pip
pip install -r streamlit_requirements.txt --force-reinstall

## Deployment

### Next.js → Vercel

git push origin main
# Auto-deploys via GitHub integration

### Streamlit → (Optional External Service)

# Streamlit Cloud, Render, or Heroku
# See Streamlit documentation for deployment

## References

- [Copilot Instructions](./.github/copilot-instructions.md)
- [Environment Setup](./ENVIRONMENT_SETUP.md)
- [Python Setup](./PYTHON_SETUP.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

