#!/usr/bin/env python3
"""Sentry CLI for listing, inspecting, and resolving issues and projects."""
import argparse
import json
import os
import sys
import requests


class SentryClient:
    """Client for Sentry API interactions."""

    def __init__(self):
        self.token = os.environ.get("SENTRY_AUTH_TOKEN", "")
        if not self.token:
            print(
                '{"error": "SENTRY_AUTH_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.org = os.environ.get("SENTRY_ORG", "")
        if not self.org:
            print(
                '{"error": "SENTRY_ORG environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.default_project = os.environ.get("SENTRY_PROJECT", "")
        self.base_url = "https://sentry.io/api/0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_issues(self, project=None):
        """List issues for a project."""
        proj = project or self.default_project
        if not proj:
            return {"error": "Project is required. Use --project or set SENTRY_PROJECT"}

        try:
            response = requests.get(
                f"{self.base_url}/projects/{self.org}/{proj}/issues/",
                headers=self.headers,
                params={"query": "is:unresolved"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_issue(self, issue_id):
        """Get details of a specific issue."""
        try:
            response = requests.get(
                f"{self.base_url}/issues/{issue_id}/",
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

    def list_projects(self):
        """List all projects in the organization."""
        try:
            response = requests.get(
                f"{self.base_url}/organizations/{self.org}/projects/",
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

    def resolve_issue(self, issue_id):
        """Resolve a specific issue."""
        try:
            response = requests.put(
                f"{self.base_url}/issues/{issue_id}/",
                headers=self.headers,
                json={"status": "resolved"},
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
    parser = argparse.ArgumentParser(description="Sentry CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    issues_parser = subparsers.add_parser("list-issues", help="List unresolved issues")
    issues_parser.add_argument("--project", help="Project slug")

    get_parser = subparsers.add_parser("get-issue", help="Get issue details")
    get_parser.add_argument("--issue-id", required=True, help="Sentry issue ID")

    subparsers.add_parser("list-projects", help="List organization projects")

    resolve_parser = subparsers.add_parser("resolve-issue", help="Resolve an issue")
    resolve_parser.add_argument("--issue-id", required=True, help="Sentry issue ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SentryClient()

    if args.command == "list-issues":
        result = client.list_issues(project=getattr(args, "project", None))
    elif args.command == "get-issue":
        result = client.get_issue(args.issue_id)
    elif args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "resolve-issue":
        result = client.resolve_issue(args.issue_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
