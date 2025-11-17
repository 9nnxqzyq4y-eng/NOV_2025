import os
from pathlib import Path

ENV_FILE = Path(".env.local")
REQUIRED_VARS = {
    "SUPABASE_URL": "https://your-project.supabase.co",
    "SUPABASE_ANON_KEY": "your-supabase-anon-key",
    "SUPABASE_SERVICE_ROLE_KEY": "your-supabase-service-role-key",
    "SONAR_TOKEN": "your-sonar-token",
    "OPENAI_API_KEY": "your-openai-api-key",
    "GROK_API_KEY": "your-grok-api-key",
    "CODERABBIT_TOKEN": "your-coderabbit-token"
}
def read_env_file():
    if not ENV_FILE.exists():
        print("No .env.local file found. Creating a new one with placeholders.")
        with open(ENV_FILE, "w") as f:
            for k, v in REQUIRED_VARS.items():
                f.write(f"{k}={v}\n")
        return {k: v for k, v in REQUIRED_VARS.items()}
    env = {}
    with open(ENV_FILE) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env
def update_env_file(env):
    updated = False
    lines = []
    for k, placeholder in REQUIRED_VARS.items():
        v = env.get(k, placeholder)
        if v == placeholder:
            print(f"⚠️  {k} is still a placeholder. Please update it with your real value.")
            updated = True
        lines.append(f"{k}={v}")
    with open(ENV_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")
    if updated:
        print("Some variables are still placeholders. Please update .env.local with your real secrets.")
    else:
        print("✅ All required environment variables are set in .env.local.")
def check_connections(env):
    print("\nChecking connections to all tools:")
    if env.get("SUPABASE_URL", "").startswith("https://") and "supabase.co" in env.get("SUPABASE_URL", ""):
        print("✅ SUPABASE_URL looks valid.")
        print("❌ SUPABASE_URL is missing or invalid.")
    if env.get("SUPABASE_ANON_KEY", "").startswith("ey"):
        print("✅ SUPABASE_ANON_KEY looks present.")
        print("❌ SUPABASE_ANON_KEY is missing or placeholder.")
    if env.get("SUPABASE_SERVICE_ROLE_KEY", "").startswith("ey"):
        print("✅ SUPABASE_SERVICE_ROLE_KEY looks present.")
        print("❌ SUPABASE_SERVICE_ROLE_KEY is missing or placeholder.")
    if env.get("SONAR_TOKEN", "").startswith("sqa_") or len(env.get("SONAR_TOKEN", "")) > 10:
        print("✅ SONAR_TOKEN looks present.")
        print("❌ SONAR_TOKEN is missing or placeholder.")
    if env.get("OPENAI_API_KEY", "").startswith("sk-"):
        print("✅ OPENAI_API_KEY looks present.")
        print("❌ OPENAI_API_KEY is missing or placeholder.")
    if env.get("GROK_API_KEY", "") and env.get("GROK_API_KEY", "") != "your-grok-api-key":
        print("✅ GROK_API_KEY looks present.")
        print("❌ GROK_API_KEY is missing or placeholder.")
    if env.get("CODERABBIT_TOKEN", "") and env.get("CODERABBIT_TOKEN", "") != "your-coderabbit-token":
        print("✅ CODERABBIT_TOKEN looks present.")
        print("❌ CODERABBIT_TOKEN is missing or placeholder.")
def main():
    env = read_env_file()
    update_env_file(env)
    check_connections(env)
if __name__ == "__main__":
    main()
