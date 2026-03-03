#!/usr/bin/env python3
"""Vercel CLI for managing projects and deployments."""
import argparse
import json
import os
import sys
import requests


class VercelClient:
    """Client for Vercel REST API interactions."""

    def __init__(self):
        self.token = os.environ.get("VERCEL_TOKEN", "")
        if not self.token:
            print(
                '{"error": "VERCEL_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.vercel.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_projects(self):
        """List all projects."""
        try:
            response = requests.get(
                f"{self.base_url}/v9/projects",
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

    def list_deployments(self, project=None):
        """List deployments, optionally filtered by project."""
        params = {"limit": 50}
        if project:
            params["projectId"] = project

        try:
            response = requests.get(
                f"{self.base_url}/v6/deployments",
                headers=self.headers,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_deployment(self, deployment_id):
        """Get details of a specific deployment."""
        try:
            response = requests.get(
                f"{self.base_url}/v13/deployments/{deployment_id}",
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

    def trigger_deploy(self, project):
        """Trigger a new deployment by creating a deploy hook-style request."""
        try:
            response = requests.post(
                f"{self.base_url}/v13/deployments",
                headers=self.headers,
                json={
                    "name": project,
                    "target": "production",
                },
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
    parser = argparse.ArgumentParser(description="Vercel CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List all projects")

    deploys_parser = subparsers.add_parser(
        "list-deployments", help="List deployments"
    )
    deploys_parser.add_argument("--project", help="Project name or ID to filter by")

    get_deploy_parser = subparsers.add_parser(
        "get-deployment", help="Get deployment details"
    )
    get_deploy_parser.add_argument(
        "--deployment-id", required=True, help="Deployment ID or URL"
    )

    trigger_parser = subparsers.add_parser(
        "trigger-deploy", help="Trigger a new deployment"
    )
    trigger_parser.add_argument("--project", required=True, help="Project name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = VercelClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "list-deployments":
        result = client.list_deployments(project=getattr(args, "project", None))
    elif args.command == "get-deployment":
        result = client.get_deployment(args.deployment_id)
    elif args.command == "trigger-deploy":
        result = client.trigger_deploy(args.project)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
