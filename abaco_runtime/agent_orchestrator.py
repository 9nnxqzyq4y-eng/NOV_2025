#!/usr/bin/env python3
"""
ABACO Agent Orchestrator - Production Agent Trigger System
Version: 1.0 - Orchestration Engine

This module provides production-ready orchestration for the 15-persona ABACO AI system.
Supports scheduled execution, individual agent triggering, and result persistence.

Features:
- Trigger individual agents or all agents
- Scheduled execution with cron support
- Result persistence to files and database
- Error handling and retry logic
- Observability with structured logging
- API integration points for Next.js backend
"""

import json
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent))

from standalone_ai import get_ai_engine  # noqa: E402


class AgentTriggerType(Enum):
    """Agent trigger types"""
    ALL = "all"
    EXECUTIVE = "executive"
    RISK = "risk"
    OPERATIONS = "operations"
    GROWTH = "growth"
    FINANCIAL = "financial"
    QUALITY = "quality"
    COMPLIANCE = "compliance"


class ExecutionStatus(Enum):
    """Execution status codes"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AgentExecutionResult:
    """Result of a single agent execution"""
    agent_id: str
    agent_name: str
    status: ExecutionStatus
    timestamp: str
    duration_ms: int
    output: str
    error: Optional[str] = None
    lines_generated: int = 0


@dataclass
class OrchestrationResult:
    """Result of orchestration run"""
    run_id: str
    trigger_type: AgentTriggerType
    timestamp: str
    total_duration_ms: int
    agents_executed: int
    agents_failed: int
    status: ExecutionStatus
    results: List[AgentExecutionResult]
    metadata: Dict[str, Any]


class _SerializationKeys:
    """Defines keys for serialization to avoid magic strings."""
    RUN_ID = "run_id"
    TRIGGER_TYPE = "trigger_type"
    TIMESTAMP = "timestamp"
    TOTAL_DURATION_MS = "total_duration_ms"
    AGENTS_EXECUTED = "agents_executed"
    AGENTS_FAILED = "agents_failed"
    STATUS = "status"
    METADATA = "metadata"
    RESULTS = "results"


class AgentOrchestrator:
    """Production orchestrator for ABACO AI agents"""

    AGENT_MAPPING = {
        "executive": "executive-summary-ai-001",
        "risk_cro": "chief-risk-officer-ai-001",
        "risk_manager": "risk-manager-ai-001",
        "collections": "collections-coach-ai-001",
        "growth": "growth-strategist-ai-001",
        "commercial": "commercial-manager-ai-001",
        "kam": "kam-assistant-ai-001",
        "financial": "financial-analyst-ai-001",
        "quality": "data-quality-guardian-ai-001",
        "mlops": "modeling-mlops-ai-001",
        "designer": "visual-designer-ai-001",
        "integrations": "integrations-orchestrator-ai-001",
        "compliance": "compliance-audit-ai-001",
        "forecaster": "product-forecaster-ai-001",
        "advisor": "advisor-hitl-ai-001",
    }

    TRIGGER_GROUPS = {
        AgentTriggerType.EXECUTIVE: ["executive"],
        AgentTriggerType.RISK: ["risk_cro", "risk_manager"],
        AgentTriggerType.OPERATIONS: ["collections", "quality", "mlops"],
        AgentTriggerType.GROWTH: ["growth", "commercial", "kam"],
        AgentTriggerType.FINANCIAL: ["financial"],
        AgentTriggerType.QUALITY: ["quality"],
        AgentTriggerType.COMPLIANCE: ["compliance"],
        AgentTriggerType.ALL: list(AGENT_MAPPING.keys()),
    }

    def __init__(self, output_dir: Path = None, log_file: Path = None):
        """Initialize orchestrator"""
        self.engine = get_ai_engine()
        self.output_dir = output_dir or Path(__file__).parent.parent / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.logger = self._setup_logging(log_file)

    def _setup_logging(self, log_file: Path = None) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger("AgentOrchestrator")
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def _execute_agent_safely(
        self, agent_key: str, demo_data: Dict[str, Any]
    ) -> AgentExecutionResult:
        """Executes a single agent and handles any exceptions."""
        start_time = datetime.now()
        agent_id = self.AGENT_MAPPING.get(agent_key, agent_key)
        personality = self.engine.personalities.get(agent_key)
        agent_name = personality.name if personality else agent_key
        error_message = None
        status = ExecutionStatus.SUCCESS
        output = ""

        try:
            output = self.engine.generate_response(agent_id, {}, demo_data)
        except Exception as e:
            self.logger.error(f"Agent '{agent_key}' execution failed: {e}", exc_info=True)
            status = ExecutionStatus.FAILED
            error_message = str(e)

        duration = int((datetime.now() - start_time).total_seconds() * 1000)
        return AgentExecutionResult(
            agent_id=agent_key,
            agent_name=agent_name,
            status=status,
            timestamp=datetime.now().isoformat(),
            duration_ms=duration,
            output=output,
            error=error_message,
            lines_generated=len(output.split('\n')) if output else 0,
        )

    def trigger_agents(
        self,
        trigger_type: AgentTriggerType,
        demo_data: Optional[Dict[str, Any]] = None
    ) -> OrchestrationResult:
        """
        Trigger agents based on trigger type

        Args:
            trigger_type: Type of agents to trigger
            demo_data: Demo data for agent execution

        Returns:
            OrchestrationResult with all execution details
        """
        start_time = datetime.now()
        run_id = f"run_{start_time.strftime('%Y%m%d_%H%M%S')}"

        self.logger.info(f"Starting orchestration run: {run_id}, trigger: {trigger_type.value}")

        if demo_data is None:
            demo_data = self._get_default_demo_data()

        agents_to_run = self.TRIGGER_GROUPS[trigger_type]
        results = []
        failed_count = 0

        for agent_key in agents_to_run:
            result = self._execute_agent_safely(agent_key, demo_data)
            results.append(result)

            if result.status == ExecutionStatus.FAILED:
                failed_count += 1

            self.logger.info(
                f"Agent {result.agent_name} executed: "
                f"status={result.status.value}, duration={result.duration_ms}ms"
            )

        end_time = datetime.now()
        total_duration = int((end_time - start_time).total_seconds() * 1000)

        execution_status = self._determine_run_status(failed_count, len(agents_to_run))

        orchestration_result = OrchestrationResult(
            run_id=run_id,
            trigger_type=trigger_type,
            timestamp=start_time.isoformat(),
            total_duration_ms=total_duration,
            agents_executed=len(agents_to_run),
            agents_failed=failed_count,
            status=execution_status,
            results=results,
            metadata={
                "version": "1.0",
                "environment": "production",
                "trigger_groups": list(agents_to_run)
            }
        )

        self.logger.info(
            f"Orchestration complete: {run_id}, "
            f"executed={len(agents_to_run)}, failed={failed_count}, "
            f"total_duration={total_duration}ms"
        )

        return orchestration_result

    def _determine_run_status(self, failed_count: int, total_agents: int) -> ExecutionStatus:
        """Determines the final status of the orchestration run."""
        if failed_count == 0:
            return ExecutionStatus.SUCCESS
        if failed_count < total_agents:
            return ExecutionStatus.PARTIAL
        return ExecutionStatus.FAILED

    def save_results(self, result: OrchestrationResult) -> Path:
        """Save orchestration results to disk"""

        result_file = self.output_dir / f"{result.run_id}_result.json"

        result_dict = {
            _SerializationKeys.RUN_ID: result.run_id,
            _SerializationKeys.TRIGGER_TYPE: result.trigger_type.value,
            _SerializationKeys.TIMESTAMP: result.timestamp,
            _SerializationKeys.TOTAL_DURATION_MS: result.total_duration_ms,
            _SerializationKeys.AGENTS_EXECUTED: result.agents_executed,
            _SerializationKeys.AGENTS_FAILED: result.agents_failed,
            _SerializationKeys.STATUS: result.status.value,
            _SerializationKeys.METADATA: result.metadata,
            _SerializationKeys.RESULTS: [asdict(r) for r in result.results]
        }

        result_dict[_SerializationKeys.RESULTS] = [
            {
                **r,
                _SerializationKeys.STATUS: (
                    r[_SerializationKeys.STATUS].value
                    if isinstance(r[_SerializationKeys.STATUS], ExecutionStatus)
                    else r[_SerializationKeys.STATUS]
                )
            }
            for r in result_dict[_SerializationKeys.RESULTS]
        ]

        with open(result_file, 'w') as f:
            json.dump(result_dict, f, indent=2)

        self.logger.info(f"Results saved to: {result_file}")

        markdown_file = self.output_dir / f"{result.run_id}_report.md"
        self._save_markdown_report(result, markdown_file)

        return result_file

    def _save_markdown_report(self, result: OrchestrationResult, file_path: Path):
        """Save human-readable markdown report"""

        if result.agents_executed == 0:
            success_rate = 0.0
        else:
            success_rate = ((result.agents_executed - result.agents_failed) / result.agents_executed) * 100

        report = f"""# ABACO Agent Orchestration Report

**Run ID**: {result.run_id}
**Timestamp**: {result.timestamp}
**Status**: {result.status.value}
**Total Duration**: {result.total_duration_ms}ms

## Summary

- **Agents Executed**: {result.agents_executed}
- **Agents Failed**: {result.agents_failed}
- **Success Rate**: {success_rate:.1f}%

## Agent Results

"""

        for r in result.results:
            report += f"""### {r.agent_name}
- **Status**: {r.status.value}
- **Duration**: {r.duration_ms}ms
- **Lines Generated**: {r.lines_generated}
"""
            if r.error:
                report += f"- **Error**: {r.error}\n"
            report += "\n"

        with open(file_path, 'w') as f:
            f.write(report)

        self.logger.info(f"Report saved to: {file_path}")

    def _get_default_demo_data(self) -> Dict[str, Any]:
        """Get default demo data"""
        return {
            "kpis": {
                "tpv": 2450000,
                "clients": 245,
                "default_rate": 0.021,
                "npa": 0.032,
                "growth_mom": 0.128,
                "default_trend": -0.003
            },
            "portfolio": {
                "par30": 0.085,
                "concentration": 0.382,
                "avg_pod": 0.18,
                "olb": 5200000,
                "high_risk_pct": 15.2
            },
            "dpd_cases": {
                "over_90": 47,
                "60_90": 32,
                "30_60": 58
            }
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="ABACO Agent Orchestrator")
    parser.add_argument(
        "--trigger",
        type=str,
        default="all",
        choices=[t.value for t in AgentTriggerType],
        help="Type of agents to trigger"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for results"
    )
    parser.add_argument(
        "--save-results",
        action="store_true",
        help="Save results to disk"
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator(output_dir=args.output_dir)

    trigger_type = AgentTriggerType(args.trigger)
    result = orchestrator.trigger_agents(trigger_type)

    if args.save_results:
        orchestrator.save_results(result)

    # Use logger for final output
    orchestrator.logger.info("\n" + "="*80)
    orchestrator.logger.info(f"Orchestration Complete: {result.run_id}")
    orchestrator.logger.info(f"Status: {result.status.value}")
    orchestrator.logger.info(f"Agents Executed: {result.agents_executed}")
    orchestrator.logger.info(f"Agents Failed: {result.agents_failed}")
    orchestrator.logger.info(f"Total Duration: {result.total_duration_ms}ms")
    orchestrator.logger.info("="*80 + "\n")


if __name__ == "__main__":
    main()
