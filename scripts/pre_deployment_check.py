#!/usr/bin/env python3
"""
ABACO Pre-Deployment Validation
Validates production readiness across all components
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class CheckStatus(Enum):
    PASS  "✅ PASS"
    FAIL  "❌ FAIL"
    WARN  "⚠️  WARN"
    SKIP  "⊘ SKIP"


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    details: str  ""


class PreDeploymentChecker:
    def __init__(self, project_root: Path):
        self.project_root  project_root
        self.results: List[CheckResult]  []

    def run_all_checks(self) - Tuple[int, int]:
        """Run all pre-deployment checks"""

        print("\n" + "" * 80)
        print("ABACO PRE-DEPLOYMENT VALIDATION")
        print("" * 80 + "\n")

        self.check_typescript()
        self.check_linting()
        self.check_build()
        self.check_environment()
        self.check_dependencies()
        self.check_migrations()
        self.check_api_routes()
        self.check_python_runtime()
        self.check_secrets()
        self.check_git_status()

        passed  sum(1 for r in self.results if r.status  CheckStatus.PASS)
        failed  sum(1 for r in self.results if r.status  CheckStatus.FAIL)

        self.print_report(passed, failed)
        return passed, failed

    def check_typescript(self):
        """Check TypeScript compilation"""
        try:
            result  subprocess.run(
                ["npm", "run", "type-check"], cwdself.project_root, capture_outputTrue, timeout30
            )
            if result.returncode  0:
                self.results.append(
                    CheckResult(
                        name"TypeScript Type Checking",
                        statusCheckStatus.PASS,
                        message"All TypeScript files compile correctly",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"TypeScript Type Checking",
                        statusCheckStatus.FAIL,
                        message"TypeScript compilation errors detected",
                        detailsresult.stderr.decode()[:200],
                    )
                )
        except subprocess.TimeoutExpired:
            self.results.append(
                CheckResult(
                    name"TypeScript Type Checking",
                    statusCheckStatus.FAIL,
                    message"Type checking timed out",
                )
            )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"TypeScript Type Checking",
                    statusCheckStatus.FAIL,
                    messagef"Error during type checking: {str(e)}",
                )
            )

    def check_linting(self):
        """Check ESLint"""
        try:
            result  subprocess.run(
                ["npm", "run", "lint"], cwdself.project_root, capture_outputTrue, timeout30
            )
            if result.returncode  0:
                self.results.append(
                    CheckResult(
                        name"ESLint Validation",
                        statusCheckStatus.PASS,
                        message"No linting errors or warnings",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"ESLint Validation",
                        statusCheckStatus.WARN,
                        message"Linting issues detected",
                        detailsresult.stdout.decode()[:200],
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"ESLint Validation",
                    statusCheckStatus.WARN,
                    messagef"Could not run linting: {str(e)}",
                )
            )

    def check_build(self):
        """Check Next.js build"""
        try:
            result  subprocess.run(
                ["npm", "run", "build"], cwdself.project_root, capture_outputTrue, timeout120
            )
            if result.returncode  0:
                self.results.append(
                    CheckResult(
                        name"Next.js Build",
                        statusCheckStatus.PASS,
                        message"Production build succeeds",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"Next.js Build",
                        statusCheckStatus.FAIL,
                        message"Build failed",
                        detailsresult.stderr.decode()[:200],
                    )
                )
        except subprocess.TimeoutExpired:
            self.results.append(
                CheckResult(
                    name"Next.js Build", statusCheckStatus.FAIL, message"Build timed out"
                )
            )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"Next.js Build",
                    statusCheckStatus.FAIL,
                    messagef"Error during build: {str(e)}",
                )
            )

    def check_environment(self):
        """Check environment configuration"""
        required_keys  [
            "NEXT_PUBLIC_SUPABASE_URL",
            "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        ]

        missing  [k for k in required_keys if not os.getenv(k)]

        if not missing:
            self.results.append(
                CheckResult(
                    name"Environment Variables",
                    statusCheckStatus.PASS,
                    message"All required environment variables set",
                )
            )
        else:
            self.results.append(
                CheckResult(
                    name"Environment Variables",
                    statusCheckStatus.WARN,
                    messagef"Missing environment variables: {', '.join(missing)}",
                )
            )

    def check_dependencies(self):
        """Check npm dependencies"""
        try:
            result  subprocess.run(
                ["npm", "list", "--depth0"], cwdself.project_root, capture_outputTrue, timeout30
            )
            if result.returncode  0:
                self.results.append(
                    CheckResult(
                        name"NPM Dependencies",
                        statusCheckStatus.PASS,
                        message"All dependencies installed",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"NPM Dependencies",
                        statusCheckStatus.WARN,
                        message"Some dependency issues detected",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"NPM Dependencies",
                    statusCheckStatus.WARN,
                    messagef"Could not check dependencies: {str(e)}",
                )
            )

    def check_migrations(self):
        """Check Supabase migrations"""
        migrations_dir  self.project_root / "supabase" / "migrations"
        if migrations_dir.exists():
            migration_files  list(migrations_dir.glob("*.sql"))
            if migration_files:
                self.results.append(
                    CheckResult(
                        name"Supabase Migrations",
                        statusCheckStatus.PASS,
                        messagef"Found {len(migration_files)} migrations",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"Supabase Migrations",
                        statusCheckStatus.WARN,
                        message"No migration files found",
                    )
                )
        else:
            self.results.append(
                CheckResult(
                    name"Supabase Migrations",
                    statusCheckStatus.WARN,
                    message"Migrations directory not found",
                )
            )

    def check_api_routes(self):
        """Check API routes"""
        api_dir  self.project_root / "app" / "api"
        if api_dir.exists():
            route_files  list(api_dir.rglob("route.ts"))
            if route_files:
                self.results.append(
                    CheckResult(
                        name"API Routes",
                        statusCheckStatus.PASS,
                        messagef"Found {len(route_files)} API routes",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"API Routes", statusCheckStatus.WARN, message"No API routes found"
                    )
                )
        else:
            self.results.append(
                CheckResult(
                    name"API Routes", statusCheckStatus.WARN, message"API directory not found"
                )
            )

    def check_python_runtime(self):
        """Check Python runtime"""
        try:
            result  subprocess.run(
                ["python3", "abaco_runtime/showcase_agents.py"],
                cwdself.project_root,
                capture_outputTrue,
                timeout30,
            )
            if result.returncode  0:
                self.results.append(
                    CheckResult(
                        name"Python Runtime (AI Agents)",
                        statusCheckStatus.PASS,
                        message"AI agent system runs successfully",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"Python Runtime (AI Agents)",
                        statusCheckStatus.FAIL,
                        message"AI agent system error",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"Python Runtime (AI Agents)",
                    statusCheckStatus.WARN,
                    messagef"Could not test Python runtime: {str(e)}",
                )
            )

    def check_secrets(self):
        """Check for exposed secrets"""
        sensitive_patterns  [
            "sk-",
            "xai-",
            "hf_",
            "Bearer ",
        ]

        suspicious_files  []
        for pattern in sensitive_patterns:
            result  subprocess.run(
                ["grep", "-r", pattern, "app/", "lib/", "components/"],
                cwdself.project_root,
                capture_outputTrue,
            )
            if result.returncode  0:
                suspicious_files.extend(result.stdout.decode().split("\n")[:3])

        if not suspicious_files:
            self.results.append(
                CheckResult(
                    name"Secrets Exposure Check",
                    statusCheckStatus.PASS,
                    message"No exposed secrets detected",
                )
            )
        else:
            self.results.append(
                CheckResult(
                    name"Secrets Exposure Check",
                    statusCheckStatus.WARN,
                    message"Potential secrets found (verify not hardcoded)",
                )
            )

    def check_git_status(self):
        """Check git status"""
        try:
            result  subprocess.run(
                ["git", "status", "--short"], cwdself.project_root, capture_outputTrue, timeout10
            )
            modified_count  len([l for l in result.stdout.decode().split("\n") if l.strip()])

            if modified_count  0:
                self.results.append(
                    CheckResult(
                        name"Git Status",
                        statusCheckStatus.PASS,
                        message"Working directory clean",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name"Git Status",
                        statusCheckStatus.WARN,
                        messagef"{modified_count} files with uncommitted changes",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name"Git Status",
                    statusCheckStatus.SKIP,
                    messagef"Could not check git status: {str(e)}",
                )
            )

    def print_report(self, passed: int, failed: int):
        """Print validation report"""
        print("\n" + "" * 80)
        print("VALIDATION RESULTS")
        print("" * 80 + "\n")

        for result in self.results:
            print(f"{result.status.value} {result.name}")
            print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details[:100]}...")
            print()

        print("" * 80)
        print(f"Summary: {passed} passed, {failed} failed")
        print("" * 80 + "\n")

        if failed  0:
            print("❌ DEPLOYMENT NOT READY - Fix the failures above\n")
            sys.exit(1)
        else:
            print("✅ READY FOR DEPLOYMENT\n")
            sys.exit(0)


def main():
    project_root  Path(__file__).parent.parent
    checker  PreDeploymentChecker(project_root)
    passed, failed  checker.run_all_checks()


if __name__  "__main__":
    main()
