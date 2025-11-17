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
                self.results.append(CheckResult(
                    name=TS_CHECK,
                    status=CheckStatus.FAIL,
                    message="TypeScript compilation errors detected",
                    details=result.stderr.decode()[:200],
                ))
        except subprocess.TimeoutExpired:
            self.results.append(CheckResult(
                name=TS_CHECK,
                status=CheckStatus.FAIL,
                message="Type checking timed out"
            ))
        except Exception as e:
            self.results.append(CheckResult(
                name=TS_CHECK,
                status=CheckStatus.FAIL,
                message=f"Error during type checking: {str(e)}"
            ))
    
    def check_linting(self):
        """Check ESLint"""
        try:
            result = subprocess.run(
                ["npm", "run", "lint"],
                cwd=self.project_root,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                self.results.append(CheckResult(
                    name=LINT_CHECK,
                    status=CheckStatus.PASS,
                    message="No linting errors or warnings"
                ))
            else:
                self.results.append(CheckResult(
                    name=LINT_CHECK,
                    status=CheckStatus.WARN,
                    message="Linting issues detected",
                    details=result.stdout.decode()[:200],
                ))
        except Exception as e:
            self.results.append(CheckResult(
                name=LINT_CHECK,
                status=CheckStatus.WARN,
                message=f"Could not run linting: {str(e)}"
            ))
    
    def check_build(self):
        """Check Next.js build"""
        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.project_root,
                capture_output=True,
                timeout=120
            )
            if result.returncode == 0:
                self.results.append(CheckResult(
                    name=BUILD_CHECK,
                    status=CheckStatus.PASS,
                    message="Production build succeeds"
                ))
            else:
                self.results.append(CheckResult(
                    name=BUILD_CHECK,
                    status=CheckStatus.FAIL,
                    message="Build failed",
                    details=result.stderr.decode()[:200],
                ))
        except subprocess.TimeoutExpired:
            self.results.append(CheckResult(
                name=BUILD_CHECK,
                status=CheckStatus.FAIL,
                message="Build timed out"
            ))
        except Exception as e:
            self.results.append(CheckResult(
                name=BUILD_CHECK,
                status=CheckStatus.FAIL,
                message=f"Error during build: {str(e)}"
            ))
    
    def check_environment(self):
        """Check environment configuration"""
        required_keys = [
            "NEXT_PUBLIC_SUPABASE_URL",
            "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        ]
        
        missing = [k for k in required_keys if not os.getenv(k)]
        
        if not missing:
            self.results.append(CheckResult(
                name=ENV_CHECK,
                status=CheckStatus.PASS,
                message="All required environment variables set",
            ))
        else:
            self.results.append(CheckResult(
                name=ENV_CHECK,
                status=CheckStatus.WARN,
                message=f"Missing environment variables: {', '.join(missing)}",
            ))
    
    def check_dependencies(self):
        """Check npm dependencies"""
        try:
            result = subprocess.run(
                ["npm", "list", "--depth=0"],
                cwd=self.project_root,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                self.results.append(CheckResult(
                    name=DEPS_CHECK,
                    status=CheckStatus.PASS,
                    message="All dependencies installed"
                ))
            else:
                self.results.append(CheckResult(
                    name=DEPS_CHECK,
                    status=CheckStatus.WARN,
                    message="Some dependency issues detected"
                ))
        except Exception as e:
            self.results.append(CheckResult(
                name=DEPS_CHECK,
                status=CheckStatus.WARN,
                message=f"Could not check dependencies: {str(e)}",
            ))
    
    def check_migrations(self):
        """Check Supabase migrations"""
        migrations_dir = self.project_root / "supabase" / "migrations"
        if migrations_dir.exists():
            migration_files = list(migrations_dir.glob("*.sql"))
            if migration_files:
                self.results.append(CheckResult(
                    name=MIGRATIONS_CHECK,
                    status=CheckStatus.PASS,
                    message=f"Found {len(migration_files)} migrations",
                ))
            else:
                self.results.append(CheckResult(
                    name=MIGRATIONS_CHECK,
                    status=CheckStatus.WARN,
                    message="No migration files found",
                ))
        else:
            self.results.append(CheckResult(
                name=MIGRATIONS_CHECK,
                status=CheckStatus.WARN,
                message="Migrations directory not found",
            ))
    
    def check_api_routes(self):
        """Check API routes"""
        api_dir = self.project_root / "app" / "api"
        if api_dir.exists():
            route_files = list(api_dir.rglob("route.ts"))
            if route_files:
                self.results.append(CheckResult(
                    name=API_ROUTES_CHECK,
                    status=CheckStatus.PASS,
                    message=f"Found {len(route_files)} API routes",
                ))
            else:
                self.results.append(CheckResult(
                    name=API_ROUTES_CHECK,
                    status=CheckStatus.WARN,
                    message="No API routes found",
                ))
        else:
            self.results.append(CheckResult(
                name=API_ROUTES_CHECK,
                status=CheckStatus.WARN,
                message="API directory not found",
            ))
    
    def check_secrets(self):
        """Check for exposed secrets"""
        sensitive_patterns = [
            "sk-",
            "xai-",
            "hf_",
            "Bearer ",
        ]
        
        suspicious_files = []
        for pattern in sensitive_patterns:
            result = subprocess.run(
                ["grep", "-r", pattern, "app/", "lib/", "components/"],
                cwd=self.project_root,
                capture_output=True
            )
            if result.returncode == 0:
                suspicious_files.extend(result.stdout.decode().split('\n')[:3])
        
        if not suspicious_files:
            self.results.append(CheckResult(
                name=SECRETS_CHECK,
                status=CheckStatus.PASS,
                message="No exposed secrets detected",
            ))
        else:
            self.results.append(CheckResult(
                name=SECRETS_CHECK,
                status=CheckStatus.WARN,
                message="Potential secrets found (verify not hardcoded)",
            ))
    
    def check_git_status(self):
        """Check git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.project_root,
                capture_output=True,
                timeout=10
            )
            modified_count = len([
                line for line in result.stdout.decode().split('\n') if line.strip()
            ])
            
            if modified_count == 0:
                self.results.append(CheckResult(
                    name=GIT_STATUS_CHECK,
                    status=CheckStatus.PASS,
                    message="Working directory clean",
                ))
            else:
                self.results.append(CheckResult(
                    name=GIT_STATUS_CHECK,
                    status=CheckStatus.WARN,
                    message=f"{modified_count} files with uncommitted changes",
                ))
        except Exception as e:
            self.results.append(CheckResult(
                name=GIT_STATUS_CHECK,
                status=CheckStatus.SKIP,
                message=f"Could not check git status: {str(e)}",
            ))
    
    def print_report(self, passed: int, failed: int):
        """Print validation report"""
        print("\n" + "="*80)
        print("VALIDATION RESULTS")
        print("="*80 + "\n")
        
        for result in self.results:
            print(f"{result.status.value} {result.name}")
            print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details[:100]}...")
            print()
        
        print("="*80)
        print(f"Summary: {passed} passed, {failed} failed")
        print("="*80 + "\n")
        
        if failed > 0:
            print("❌ DEPLOYMENT NOT READY - Fix the failures above\n")
            sys.exit(1)
        else:
            print("✅ READY FOR DEPLOYMENT\n")
            sys.exit(0)

def main():
    project_root = Path(__file__).parent.parent
    checker = PreDeploymentChecker(project_root)
    _, _ = checker.run_all_checks()

if __name__ == "__main__":
    main()
