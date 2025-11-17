#!/usr/bin/env python3
"""
Master Control Program (MCP) Server
Version: 1.0 - FastAPI-based AI Orchestrator

This server exposes the ABACO AgentOrchestrator via a REST API,
allowing for robust, scalable, and language-agnostic interaction
with the AI agent system.
"""

import logging
from fastapi import FastAPI, HTTPException

from agent_orchestrator import AgentOrchestrator, AgentTriggerType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("MCP_Server")

app = FastAPI(
    title="ABACO Master Control Program",
    description="API for orchestrating the 15-persona AI agent system.",
    version="1.0.0",
)

orchestrator = AgentOrchestrator()


@app.post("/trigger/{trigger_type}", tags=["Orchestration"])
async def trigger_agent_run(trigger_type: AgentTriggerType):
    """
    Triggers a run of a specified group of AI agents.
    """
    logger.info(f"Received request to trigger agent group: {trigger_type.value}")
    try:
        result = orchestrator.trigger_agents(trigger_type)
        # For now, we return a summary. The full result is saved by the orchestrator.
        return {
            "run_id": result.run_id,
            "status": result.status.value,
            "agents_executed": result.agents_executed,
            "agents_failed": result.agents_failed,
        }
    except Exception as e:
        logger.error(f"An error occurred during orchestration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))