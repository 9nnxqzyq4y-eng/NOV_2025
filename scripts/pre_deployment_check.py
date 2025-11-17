#!/usr/bin/env python3
"""
ABACO Pre-Deployment Validation
Validates production readiness across all components

import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
class CheckStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARN = "⚠️  WARN"
    SKIP = "⊘ SKIP"
@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    details: str = ""
# Constants for check names
TS_CHECK = "TypeScript Type Checking"
LINT_CHECK = "ESLint Validation"
BUILD_CHECK = "Next.js Build"
DEPS_CHECK = "NPM Dependencies"
ENV_CHECK = "Environment Variables"
MIGRATIONS_CHECK = "Supabase Migrations"
API_ROUTES_CHECK = "API Routes"
SECRETS_CHECK = "Secrets Exposure Check"
GIT_STATUS_CHECK = "Git Status"
class PreDeploymentChecker:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: List[CheckResult] = []
    
    def run_all_checks(self) -> Tuple[int, int]:
        """Run all pre-deployment checks"""
        
        print("\n" + "="*80)
        print("ABACO PRE-DEPLOYMENT VALIDATION")
        print("="*80 + "\n")
        self.check_typescript()
        self.check_linting()
        self.check_build()
        self.check_environment()
        self.check_dependencies()
        self.check_migrations()
        self.check_api_routes()
        self.check_secrets()
        self.check_git_status()
        passed = sum(r.status == CheckStatus.PASS for r in self.results)
        failed = sum(r.status == CheckStatus.FAIL for r in self.results)
        self.print_report(passed, failed)
        return passed, failed
    def check_typescript(self):
        """Check TypeScript compilation"""
        try:
            result = subprocess.run(
                ["npm", "run", "type-check"],
                cwd=self.project_root,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                self.results.append(CheckResult(
                    name=TS_CHECK,
                    status=CheckStatus.PASS,
                    message="All TypeScript files compile correctly",
                ))
            else:
                    status=CheckStatus.FAIL,
                    message="TypeScript compilation errors detected",
                    details=result.stderr.decode()[:200],
        except subprocess.TimeoutExpired:
            self.results.append(CheckResult(
                name=TS_CHECK,
                status=CheckStatus.FAIL,
                message="Type checking timed out"
            ))
        except Exception as e:
                message=f"Error during type checking: {str(e)}"
    def check_linting(self):
        """Check ESLint"""
                ["npm", "run", "lint"],
                    name=LINT_CHECK,
                    message="No linting errors or warnings"
                    status=CheckStatus.WARN,
                    message="Linting issues detected",
                    details=result.stdout.decode()[:200],
                name=LINT_CHECK,
                status=CheckStatus.WARN,
                message=f"Could not run linting: {str(e)}"
    def check_build(self):
        """Check Next.js build"""
                ["npm", "run", "build"],
                timeout=120
                    name=BUILD_CHECK,
                    message="Production build succeeds"
                    message="Build failed",
                name=BUILD_CHECK,
                message="Build timed out"
                message=f"Error during build: {str(e)}"
    def check_environment(self):
        """Check environment configuration"""
        required_keys = [
            "NEXT_PUBLIC_SUPABASE_URL",
            "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        ]
        missing = [k for k in required_keys if not os.getenv(k)]
        if not missing:
                name=ENV_CHECK,
                status=CheckStatus.PASS,
                message="All required environment variables set",
        else:
                message=f"Missing environment variables: {', '.join(missing)}",
    def check_dependencies(self):
        """Check npm dependencies"""
                ["npm", "list", "--depth=0"],
                    name=DEPS_CHECK,
                    message="All dependencies installed"
                    message="Some dependency issues detected"
                name=DEPS_CHECK,
                message=f"Could not check dependencies: {str(e)}",
    def check_migrations(self):
        """Check Supabase migrations"""
        migrations_dir = self.project_root / "supabase" / "migrations"
        if migrations_dir.exists():
            migration_files = list(migrations_dir.glob("*.sql"))
            if migration_files:
                    name=MIGRATIONS_CHECK,
                    message=f"Found {len(migration_files)} migrations",
                    message="No migration files found",
                name=MIGRATIONS_CHECK,
                message="Migrations directory not found",
    def check_api_routes(self):
        """Check API routes"""
        api_dir = self.project_root / "app" / "api"
        if api_dir.exists():
            route_files = list(api_dir.rglob("route.ts"))
            if route_files:
                    name=API_ROUTES_CHECK,
                    message=f"Found {len(route_files)} API routes",
                    message="No API routes found",
                name=API_ROUTES_CHECK,
                message="API directory not found",
    def check_secrets(self):
        """Check for exposed secrets"""
        sensitive_patterns = [
            "sk-",
            "xai-",
            "hf_",
            "Bearer ",
        suspicious_files = []
        for pattern in sensitive_patterns:
                ["grep", "-r", pattern, "app/", "lib/", "components/"],
                capture_output=True
                suspicious_files.extend(result.stdout.decode().split('\n')[:3])
        if not suspicious_files:
                name=SECRETS_CHECK,
                message="No exposed secrets detected",
                message="Potential secrets found (verify not hardcoded)",
    def check_git_status(self):
        """Check git status"""
                ["git", "status", "--short"],
                timeout=10
            modified_count = len([
                line for line in result.stdout.decode().split('\n') if line.strip()
            ])
            
            if modified_count == 0:
                    name=GIT_STATUS_CHECK,
                    message="Working directory clean",
                    message=f"{modified_count} files with uncommitted changes",
                name=GIT_STATUS_CHECK,
                status=CheckStatus.SKIP,
                message=f"Could not check git status: {str(e)}",
    def print_report(self, passed: int, failed: int):
        """Print validation report"""
        print("VALIDATION RESULTS")
        for result in self.results:
            print(f"{result.status.value} {result.name}")
            print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details[:100]}...")
            print()
        print("="*80)
        print(f"Summary: {passed} passed, {failed} failed")
        if failed > 0:
            print("❌ DEPLOYMENT NOT READY - Fix the failures above\n")
            sys.exit(1)
            print("✅ READY FOR DEPLOYMENT\n")
            sys.exit(0)
def main():
    project_root = Path(__file__).parent.parent
    checker = PreDeploymentChecker(project_root)
    _, _ = checker.run_all_checks()
if __name__ == "__main__":
    main()
