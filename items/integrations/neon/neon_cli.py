#!/usr/bin/env python3
"""Neon CLI for managing serverless Postgres projects, branches, and endpoints."""
import argparse
import json
import os
import sys
import requests


class NeonClient:
    """Client for Neon API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("NEON_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "NEON_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://console.neon.tech/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def list_projects(self):
        """List all projects."""
        try:
            response = requests.get(
                f"{self.base_url}/projects",
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

    def get_project(self, project_id):
        """Get details of a specific project."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}",
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

    def list_branches(self, project_id):
        """List branches for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}/branches",
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

    def create_branch(self, project_id, name=None):
        """Create a new branch in a project."""
        payload = {"branch": {}}
        if name:
            payload["branch"]["name"] = name

        try:
            response = requests.post(
                f"{self.base_url}/projects/{project_id}/branches",
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

    def list_endpoints(self, project_id):
        """List compute endpoints for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}/endpoints",
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
    parser = argparse.ArgumentParser(description="Neon CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List all projects")

    get_parser = subparsers.add_parser("get-project", help="Get project details")
    get_parser.add_argument("--project-id", required=True, help="Neon project ID")

    branches_parser = subparsers.add_parser("list-branches", help="List branches")
    branches_parser.add_argument("--project-id", required=True, help="Neon project ID")

    create_branch_parser = subparsers.add_parser(
        "create-branch", help="Create a branch"
    )
    create_branch_parser.add_argument(
        "--project-id", required=True, help="Neon project ID"
    )
    create_branch_parser.add_argument("--name", help="Branch name")

    endpoints_parser = subparsers.add_parser(
        "list-endpoints", help="List compute endpoints"
    )
    endpoints_parser.add_argument(
        "--project-id", required=True, help="Neon project ID"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NeonClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "get-project":
        result = client.get_project(args.project_id)
    elif args.command == "list-branches":
        result = client.list_branches(args.project_id)
    elif args.command == "create-branch":
        result = client.create_branch(
            args.project_id, name=getattr(args, "name", None)
        )
    elif args.command == "list-endpoints":
        result = client.list_endpoints(args.project_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
