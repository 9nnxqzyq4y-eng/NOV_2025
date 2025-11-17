#!/usr/bin/env python3
"""
ABACO AI Agents Demo - All 15 Personas
Demonstrates each AI persona with realistic outputs
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from abaco_runtime.standalone_ai import get_ai_engine


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "" * 80)
    print(f"  {title}")
    print("" * 80 + "\n")


def print_agent_output(agent_name: str, personality: str, output: str):
    """Print formatted agent output"""
    print(f"🤖 {agent_name} ({personality})")
    print("-" * 80)
    print(output)
    print("\n")


def main():
    """Run all agents with sample context and data"""
    print_header("ABACO AI AGENTS - COMPLETE 15-PERSONA SYSTEM DEMO")

    print("Initializing standalone AI engine...")

    # Initialize AI engine
    engine = get_ai_engine()

    print(f"Loaded {len(engine.personalities)} AI personas:")
    for agent_type, personality in engine.personalities.items():
        print(f"  • {personality.name} - {personality.position} ({personality.level})")

    sample_context  {"task": "portfolio_analysis"}
    sample_data  {
        "kpis": {
            "tpv": 2450000,
            "clients": 245,
            "default_rate": 0.021,
            "npa": 0.032,
            "growth_mom": 0.128,
        },
        "portfolio": {"par30": 0.085, "concentration": 0.382, "avg_pod": 0.18},
        "findings": [
            {"severity": "Must Fix", "description": "Unit Economics violation", "rule_id": 3},
            {"severity": "Info", "description": "All KPIs validated", "rule_id": 1},
        ],
        "dpd_cases": {"over_90": 47, "60_90": 32, "30_60": 58},
        "customer": {"dpd": 45, "balance": 5000, "payment_history": "positive until March 2025"},
        "churn": 0.18,
        "tpv": 2450000,
    }

    for agent_id in engine.personalities.keys():
        print(
            f"\n{''*80}\n🤖 {engine.personalities[agent_id].name} ({engine.personalities[agent_id].position})\n{'-'*80}"
        )
        response  engine.generate_response(agent_id, sample_context, sample_data)
        print(response)


if __name__  "__main__":
    main()
