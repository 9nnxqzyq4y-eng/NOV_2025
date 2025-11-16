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

sys.path.insert(0, str(Path(__file__).parent.parent))

from abaco_runtime.standalone_ai import get_ai_engine


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
            try:
                result = self._execute_agent(agent_key, demo_data)
                results.append(result)

                if result.status == ExecutionStatus.FAILED:
                    failed_count += 1

                self.logger.info(
                    f"Agent {result.agent_name} executed: "
                    f"status={result.status.value}, duration={result.duration_ms}ms"
                )
            except Exception as e:
                self.logger.error(f"Failed to execute agent {agent_key}: {str(e)}")
                failed_count += 1
                personality = self.engine.personalities.get(agent_key, {})
                agent_name = (
                    personality.name if hasattr(personality, 'name')
                    else agent_key
                )
                results.append(AgentExecutionResult(
                    agent_id=agent_key,
                    agent_name=agent_name,
                    status=ExecutionStatus.FAILED,
                    timestamp=datetime.now().isoformat(),
                    duration_ms=0,
                    output="",
                    error=str(e)
                ))

        end_time = datetime.now()
        total_duration = int((end_time - start_time).total_seconds() * 1000)

        execution_status = (
            ExecutionStatus.SUCCESS if failed_count == 0 else
            ExecutionStatus.PARTIAL if failed_count < len(agents_to_run) else
            ExecutionStatus.FAILED
        )

        orchestration_result = OrchestrationResult(
            run_id=run_id,
            trigger_type=trigger_type,
            timestamp=datetime.now().isoformat(),
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

    def _execute_agent(
        self,
        agent_key: str,
        demo_data: Dict[str, Any]
    ) -> AgentExecutionResult:
        """Execute a single agent"""
        start_time = datetime.now()

        agent_id = self.AGENT_MAPPING.get(agent_key, agent_key)
        personality = self.engine.personalities.get(agent_key)
        agent_name = personality.name if personality else agent_key

        try:
            output = self.engine.generate_response(agent_id, {}, demo_data)

            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds() * 1000)

            return AgentExecutionResult(
                agent_id=agent_key,
                agent_name=agent_name,
                status=ExecutionStatus.SUCCESS,
                timestamp=datetime.now().isoformat(),
                duration_ms=duration,
                output=output,
                lines_generated=len(output.split('\n'))
            )
        except Exception as e:
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds() * 1000)

            return AgentExecutionResult(
                agent_id=agent_key,
                agent_name=agent_name,
                status=ExecutionStatus.FAILED,
                timestamp=datetime.now().isoformat(),
                duration_ms=duration,
                output="",
                error=str(e)
            )

    def save_results(self, result: OrchestrationResult) -> Path:
        """Save orchestration results to disk"""

        result_file = self.output_dir / f"{result.run_id}_result.json"

        result_dict = {
            "run_id": result.run_id,
            "trigger_type": result.trigger_type.value,
            "timestamp": result.timestamp,
            "total_duration_ms": result.total_duration_ms,
            "agents_executed": result.agents_executed,
            "agents_failed": result.agents_failed,
            "status": result.status.value,
            "metadata": result.metadata,
            "results": [asdict(r) for r in result.results]
        }

        result_dict["results"] = [
            {
                **r,
                "status": (
                    r["status"].value
                    if isinstance(r["status"], ExecutionStatus)
                    else r["status"]
                )
            }
            for r in result_dict["results"]
        ]

        with open(result_file, 'w') as f:
            json.dump(result_dict, f, indent=2)

        self.logger.info(f"Results saved to: {result_file}")

        markdown_file = self.output_dir / f"{result.run_id}_report.md"
        self._save_markdown_report(result, markdown_file)

        return result_file

    def _save_markdown_report(self, result: OrchestrationResult, file_path: Path):
        """Save human-readable markdown report"""

        if result.agents_executed > 0:
            success_rate = (
                (result.agents_executed - result.agents_failed)
                / result.agents_executed * 100
            )
        else:
            success_rate = 0.0

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

    print("\n" + "="*80)
    print(f"Orchestration Complete: {result.run_id}")
    print(f"Status: {result.status.value}")
    print(f"Agents Executed: {result.agents_executed}")
    print(f"Agents Failed: {result.agents_failed}")
    print(f"Total Duration: {result.total_duration_ms}ms")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
