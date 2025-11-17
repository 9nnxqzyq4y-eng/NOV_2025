#!/usr/bin/env python3
"""
ABACO AI Trigger Script

This script demonstrates how to trigger a specific AI persona from the
standalone_ai.py engine and generate a response.
"""
import logging
from dataclasses import dataclass, asdict

from standalone_ai import get_ai_engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


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
    """Main function to trigger an AI agent and print its response."""
    logging.info("🚀 Initializing ABACO Standalone AI Engine...")
    ai_engine = get_ai_engine()
    logging.info("✅ Engine Initialized.")

    agent_id_to_trigger = "executive-summary-ai-001"

    request_context = RequestContext(
        task="Generate Q2 portfolio review for board meeting"
    )
    kpi_data = KpiData(
        tpv=3150000,
        clients=280,
        default_rate=0.019,
        npa=0.028,
        growth_mom=0.15,
        default_trend=-0.004,
    )

    input_data = {"kpis": asdict(kpi_data)}

    logging.info(f"🎯 Sending trigger to agent: {agent_id_to_trigger}")
    logging.info("-" * 40)

    response = ai_engine.generate_response(
        agent_id_to_trigger, asdict(request_context), input_data
    )

    logging.info(f"Response received:\n{response}")
    logging.info("-" * 40)
    logging.info("✅ Task Complete.")


if __name__ == "__main__":
    main()
