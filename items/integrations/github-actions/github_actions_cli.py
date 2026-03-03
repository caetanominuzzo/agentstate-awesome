#!/usr/bin/env python3
"""GitHub Actions CLI for managing workflows and runs."""
import argparse
import json
import os
import sys
import requests


class GitHubActionsClient:
    """Client for GitHub Actions REST API interactions."""

    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN", "")
        if not self.token:
            print(
                '{"error": "GITHUB_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _actions_url(self, repo):
        """Build the Actions API base URL for a repository."""
        return f"{self.base_url}/repos/{repo}/actions"

    def list_workflows(self, repo):
        """List workflows for a repository."""
        try:
            response = requests.get(
                f"{self._actions_url(repo)}/workflows",
                headers=self.headers,
                params={"per_page": 100},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_runs(self, repo, workflow_id=None):
        """List workflow runs, optionally for a specific workflow."""
        if workflow_id:
            url = f"{self._actions_url(repo)}/workflows/{workflow_id}/runs"
        else:
            url = f"{self._actions_url(repo)}/runs"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": 50},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def trigger_workflow(self, repo, workflow_id, ref="main"):
        """Trigger a workflow dispatch event."""
        try:
            response = requests.post(
                f"{self._actions_url(repo)}/workflows/{workflow_id}/dispatches",
                headers=self.headers,
                json={"ref": ref},
                timeout=30,
            )
            response.raise_for_status()
            return {
                "success": True,
                "message": f"Workflow {workflow_id} triggered on ref '{ref}'",
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_run(self, repo, run_id):
        """Get details of a specific workflow run."""
        try:
            response = requests.get(
                f"{self._actions_url(repo)}/runs/{run_id}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def cancel_run(self, repo, run_id):
        """Cancel a workflow run."""
        try:
            response = requests.post(
                f"{self._actions_url(repo)}/runs/{run_id}/cancel",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "message": f"Run {run_id} cancelled"}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_run_jobs(self, repo, run_id):
        """List jobs for a workflow run."""
        try:
            response = requests.get(
                f"{self._actions_url(repo)}/runs/{run_id}/jobs",
                headers=self.headers,
                params={"per_page": 100},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="GitHub Actions CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    wf_parser = subparsers.add_parser("list-workflows", help="List workflows")
    wf_parser.add_argument("--repo", required=True, help="Repository (owner/repo)")

    runs_parser = subparsers.add_parser("list-runs", help="List workflow runs")
    runs_parser.add_argument("--repo", required=True, help="Repository (owner/repo)")
    runs_parser.add_argument(
        "--workflow-id", help="Workflow ID or filename to filter by"
    )

    trigger_parser = subparsers.add_parser(
        "trigger-workflow", help="Trigger a workflow dispatch"
    )
    trigger_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    trigger_parser.add_argument(
        "--workflow-id", required=True, help="Workflow ID or filename"
    )
    trigger_parser.add_argument(
        "--ref", default="main", help="Git ref to run on (default: main)"
    )

    get_run_parser = subparsers.add_parser("get-run", help="Get run details")
    get_run_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    get_run_parser.add_argument("--run-id", required=True, help="Run ID")

    cancel_parser = subparsers.add_parser("cancel-run", help="Cancel a run")
    cancel_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    cancel_parser.add_argument("--run-id", required=True, help="Run ID")

    jobs_parser = subparsers.add_parser("list-run-jobs", help="List jobs for a run")
    jobs_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    jobs_parser.add_argument("--run-id", required=True, help="Run ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GitHubActionsClient()

    if args.command == "list-workflows":
        result = client.list_workflows(args.repo)
    elif args.command == "list-runs":
        result = client.list_runs(
            args.repo, workflow_id=getattr(args, "workflow_id", None)
        )
    elif args.command == "trigger-workflow":
        result = client.trigger_workflow(args.repo, args.workflow_id, args.ref)
    elif args.command == "get-run":
        result = client.get_run(args.repo, args.run_id)
    elif args.command == "cancel-run":
        result = client.cancel_run(args.repo, args.run_id)
    elif args.command == "list-run-jobs":
        result = client.list_run_jobs(args.repo, args.run_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
