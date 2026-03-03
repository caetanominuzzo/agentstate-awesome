#!/usr/bin/env python3
"""Snyk CLI for listing organizations, projects, and security issues."""
import argparse
import json
import os
import sys
import requests


class SnykClient:
    """Client for Snyk API interactions."""

    def __init__(self):
        self.token = os.environ.get("SNYK_TOKEN", "")
        if not self.token:
            print(
                '{"error": "SNYK_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.default_org_id = os.environ.get("SNYK_ORG_ID", "")
        self.base_url = "https://api.snyk.io/rest"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/vnd.api+json",
        }

    def list_orgs(self):
        """List all organizations."""
        try:
            response = requests.get(
                f"{self.base_url}/orgs",
                headers=self.headers,
                params={"version": "2024-04-22"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_projects(self, org_id):
        """List projects in an organization."""
        try:
            response = requests.get(
                f"{self.base_url}/orgs/{org_id}/projects",
                headers=self.headers,
                params={"version": "2024-04-22"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_issues(self, org_id, project_id):
        """List issues for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/orgs/{org_id}/issues",
                headers=self.headers,
                params={
                    "version": "2024-04-22",
                    "scan_item.id": project_id,
                    "scan_item.type": "project",
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

    def test_project(self, org_id, project_id):
        """Get test results for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/orgs/{org_id}/projects/{project_id}",
                headers=self.headers,
                params={"version": "2024-04-22"},
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
    parser = argparse.ArgumentParser(description="Snyk CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-orgs", help="List all organizations")

    projects_parser = subparsers.add_parser("list-projects", help="List projects")
    projects_parser.add_argument("--org-id", required=True, help="Organization ID")

    issues_parser = subparsers.add_parser("list-issues", help="List project issues")
    issues_parser.add_argument("--org-id", required=True, help="Organization ID")
    issues_parser.add_argument("--project-id", required=True, help="Project ID")

    test_parser = subparsers.add_parser("test-project", help="Test a project")
    test_parser.add_argument("--org-id", required=True, help="Organization ID")
    test_parser.add_argument("--project-id", required=True, help="Project ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SnykClient()

    if args.command == "list-orgs":
        result = client.list_orgs()
    elif args.command == "list-projects":
        result = client.list_projects(args.org_id)
    elif args.command == "list-issues":
        result = client.list_issues(args.org_id, args.project_id)
    elif args.command == "test-project":
        result = client.test_project(args.org_id, args.project_id)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
