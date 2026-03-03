#!/usr/bin/env python3
"""GitLab CLI for managing projects, merge requests, issues, and pipelines."""
import argparse
import json
import os
import sys
import requests


class GitLabClient:
    """Client for GitLab API interactions."""

    def __init__(self):
        self.token = os.environ.get("GITLAB_TOKEN", "")
        if not self.token:
            print(
                '{"error": "GITLAB_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        base_url = os.environ.get("GITLAB_BASE_URL", "https://gitlab.com").rstrip("/")
        self.base_url = f"{base_url}/api/v4"
        self.headers = {
            "Private-Token": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_projects(self):
        """List projects accessible to the authenticated user."""
        try:
            response = requests.get(
                f"{self.base_url}/projects",
                headers=self.headers,
                params={"membership": True, "per_page": 50},
                timeout=30,
            )
            response.raise_for_status()
            return {"projects": response.json()}
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

    def list_merge_requests(self, project_id, state="opened"):
        """List merge requests for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}/merge_requests",
                headers=self.headers,
                params={"state": state, "per_page": 50},
                timeout=30,
            )
            response.raise_for_status()
            return {"merge_requests": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_issue(self, project_id, title, description=""):
        """Create a new issue in a project."""
        payload = {"title": title, "description": description}

        try:
            response = requests.post(
                f"{self.base_url}/projects/{project_id}/issues",
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

    def list_pipelines(self, project_id):
        """List pipelines for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}/pipelines",
                headers=self.headers,
                params={"per_page": 50},
                timeout=30,
            )
            response.raise_for_status()
            return {"pipelines": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="GitLab CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List accessible projects")

    get_proj_parser = subparsers.add_parser("get-project", help="Get project details")
    get_proj_parser.add_argument(
        "--project-id", required=True, help="Project ID or URL-encoded path"
    )

    mr_parser = subparsers.add_parser(
        "list-merge-requests", help="List merge requests"
    )
    mr_parser.add_argument("--project-id", required=True, help="Project ID")
    mr_parser.add_argument(
        "--state", default="opened", help="MR state: opened, closed, merged, all"
    )

    issue_parser = subparsers.add_parser("create-issue", help="Create an issue")
    issue_parser.add_argument("--project-id", required=True, help="Project ID")
    issue_parser.add_argument("--title", required=True, help="Issue title")
    issue_parser.add_argument("--description", default="", help="Issue description")

    pipe_parser = subparsers.add_parser("list-pipelines", help="List pipelines")
    pipe_parser.add_argument("--project-id", required=True, help="Project ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GitLabClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "get-project":
        result = client.get_project(args.project_id)
    elif args.command == "list-merge-requests":
        result = client.list_merge_requests(args.project_id, args.state)
    elif args.command == "create-issue":
        result = client.create_issue(args.project_id, args.title, args.description)
    elif args.command == "list-pipelines":
        result = client.list_pipelines(args.project_id)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
