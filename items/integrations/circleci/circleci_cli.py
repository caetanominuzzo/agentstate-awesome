#!/usr/bin/env python3
"""CircleCI CLI for managing pipelines, workflows, and jobs."""
import argparse
import json
import os
import sys
import requests


class CircleCIClient:
    """Client for CircleCI API interactions."""

    def __init__(self):
        self.token = os.environ.get("CIRCLECI_TOKEN", "")
        if not self.token:
            print(
                '{"error": "CIRCLECI_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://circleci.com/api/v2"
        self.headers = {
            "Circle-Token": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_pipelines(self, project_slug):
        """List pipelines for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/project/{project_slug}/pipeline",
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

    def get_pipeline(self, pipeline_id):
        """Get details of a specific pipeline."""
        try:
            response = requests.get(
                f"{self.base_url}/pipeline/{pipeline_id}",
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

    def list_workflows(self, pipeline_id):
        """List workflows for a pipeline."""
        try:
            response = requests.get(
                f"{self.base_url}/pipeline/{pipeline_id}/workflow",
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

    def trigger_pipeline(self, project_slug, branch="main"):
        """Trigger a new pipeline for a project."""
        payload = {"branch": branch}

        try:
            response = requests.post(
                f"{self.base_url}/project/{project_slug}/pipeline",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_jobs(self, workflow_id):
        """List jobs for a workflow."""
        try:
            response = requests.get(
                f"{self.base_url}/workflow/{workflow_id}/job",
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


def main():
    parser = argparse.ArgumentParser(description="CircleCI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_pipe_parser = subparsers.add_parser(
        "list-pipelines", help="List pipelines for a project"
    )
    list_pipe_parser.add_argument(
        "--project-slug",
        required=True,
        help="Project slug (e.g., gh/org/repo)",
    )

    get_pipe_parser = subparsers.add_parser(
        "get-pipeline", help="Get pipeline details"
    )
    get_pipe_parser.add_argument("--pipeline-id", required=True, help="Pipeline ID")

    wf_parser = subparsers.add_parser(
        "list-workflows", help="List workflows for a pipeline"
    )
    wf_parser.add_argument("--pipeline-id", required=True, help="Pipeline ID")

    trigger_parser = subparsers.add_parser(
        "trigger-pipeline", help="Trigger a new pipeline"
    )
    trigger_parser.add_argument(
        "--project-slug",
        required=True,
        help="Project slug (e.g., gh/org/repo)",
    )
    trigger_parser.add_argument(
        "--branch", default="main", help="Branch to build (default: main)"
    )

    jobs_parser = subparsers.add_parser(
        "list-jobs", help="List jobs for a workflow"
    )
    jobs_parser.add_argument("--workflow-id", required=True, help="Workflow ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = CircleCIClient()

    if args.command == "list-pipelines":
        result = client.list_pipelines(args.project_slug)
    elif args.command == "get-pipeline":
        result = client.get_pipeline(args.pipeline_id)
    elif args.command == "list-workflows":
        result = client.list_workflows(args.pipeline_id)
    elif args.command == "trigger-pipeline":
        result = client.trigger_pipeline(args.project_slug, args.branch)
    elif args.command == "list-jobs":
        result = client.list_jobs(args.workflow_id)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
