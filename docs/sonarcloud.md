# SonarCloud Workflow Guide

This project uses SonarCloud to analyze every pull request and track technical debt. The GitHub Action defined in `.github/workflows/sonarcloud.yml` ensures that open pull requests are analyzed sequentially and that the quality gate status is surfaced directly on each PR.

## Required Secrets

Add the following secrets at the repository level before enabling the workflow:

- `SONAR_TOKEN`: A token generated from SonarCloud with permissions to run analyses for the `jenineferderas_abaco-sim-e` project.

The default `GITHUB_TOKEN` provided by Actions is used to report the status back to the pull request.

## How the Workflow Works

1. Each non-draft pull request triggers the **SonarCloud Quality Gate** workflow.
1. The workflow installs dependencies, runs ESLint, and then executes SonarCloud analysis.
1. The second SonarCloud step waits for the quality gate result so the workflow fails if the gate is red.
1. The `concurrency` block serializes analyses per pull request number to prevent overlapping SonarCloud tasks and keep investigations manageable.

## Resolving Issues One by One

To keep remediation disciplined, address SonarCloud findings sequentially:

1. Open the latest SonarCloud report linked from the pull request badge.
1. Start with the highest severity issue (Blocker → Critical → Major → Minor → Info).
1. For each issue:
   - Fix the problem in code.
   - Add or update tests if the change impacts behavior.
   - Push the commit so the workflow re-runs and confirms the fix.
1. Repeat until the quality gate passes.

Document any follow-up tickets created for larger refactors so the team has clear ownership of outstanding debt.

