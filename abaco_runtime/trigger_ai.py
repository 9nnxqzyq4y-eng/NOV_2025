#!/usr/bin/env python3
"""
ABACO AI Trigger Script

This script demonstrates how to trigger a specific AI persona from the
standalone_ai.py engine and generate a response.
"""
from dataclasses import dataclass, asdict

from standalone_ai import get_ai_engine

@dataclass
class RequestContext:
    """Defines the context for the AI task."""
    task: str

@dataclass
class KpiData:
    """Key Performance Indicators for the portfolio."""
    tpv: int
    clients: int
    default_rate: float
    npa: float
    growth_mom: float
    default_trend: float

def main():
    """
    Main function to trigger an AI agent and print its response.
    """
    print("🚀 Initializing ABACO Standalone AI Engine...")
    ai_engine = get_ai_engine()
    print("✅ Engine Initialized.")

    # --- Define the Trigger ---
    # We will trigger 'Sofia', the executive summary agent.
    agent_id_to_trigger = "executive-summary-ai-001"
    
    # --- Prepare Context and Data ---
    # This simulates the input data the agent would receive for its task.
    request_context = RequestContext(task="Generate Q2 portfolio review for board meeting")
    kpi_data = KpiData(tpv=3150000, clients=280, default_rate=0.019, npa=0.028, growth_mom=0.15, default_trend=-0.004) # type: ignore
    
    # The engine likely expects dicts, so we convert them back before sending.
    input_data = {"kpis": asdict(kpi_data)}

    print(f"\n🎯 Sending trigger to agent: {agent_id_to_trigger}")
    print("-" * 40)

    # --- Execute the Task ---
    response = ai_engine.generate_response(agent_id_to_trigger, asdict(request_context), input_data)

    print(response)
    print("-" * 40)
    print("✅ Task Complete.")

if __name__ == "__main__":
    main()