#!/usr/bin/env python3
"""Jira CLI for creating, updating, commenting, and searching tickets."""
import argparse
import json
import os
import sys
import requests


class JiraClient:
    """Client for Jira API interactions."""

    def __init__(self):
        self.base_url = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
        if not self.base_url:
            print(
                '{"error": "JIRA_BASE_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"{self.base_url}/rest/api/3"

        jira_auth = os.environ.get("JIRA_AUTH")
        if jira_auth:
            self.headers = {
                "Authorization": f"Basic {jira_auth}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        else:
            jira_email = os.environ.get("JIRA_EMAIL")
            jira_token = os.environ.get("JIRA_API_TOKEN")
            if not jira_email or not jira_token:
                print(
                    '{"error": "JIRA_AUTH or (JIRA_EMAIL and JIRA_API_TOKEN) required"}',
                    file=sys.stderr,
                )
                sys.exit(1)

            import base64

            auth_str = f"{jira_email}:{jira_token}"
            auth_bytes = base64.b64encode(auth_str.encode()).decode()
            self.headers = {
                "Authorization": f"Basic {auth_bytes}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

    def create_issue(self, project, summary, description, issue_type="Task"):
        """Create a new Jira issue."""
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}],
                        }
                    ],
                },
                "issuetype": {"name": issue_type},
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/issue",
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

    def get_issue(self, issue_key):
        """Get details of a Jira issue."""
        try:
            response = requests.get(
                f"{self.base_url}/issue/{issue_key}",
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

    def update_issue(self, issue_key, fields):
        """Update a Jira issue."""
        payload = {"fields": fields}

        try:
            response = requests.put(
                f"{self.base_url}/issue/{issue_key}",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "issue_key": issue_key}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def add_comment(self, issue_key, comment):
        """Add a comment to a Jira issue."""
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}],
                    }
                ],
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/issue/{issue_key}/comment",
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

    def search_issues(self, jql, max_results=50):
        """Search for Jira issues using JQL."""
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params={"jql": jql, "maxResults": max_results},
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
    parser = argparse.ArgumentParser(description="Jira CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    create_parser = subparsers.add_parser("create", help="Create a new issue")
    create_parser.add_argument(
        "--project", required=True, help="Project key (e.g., PROJ)"
    )
    create_parser.add_argument("--summary", required=True, help="Issue summary")
    create_parser.add_argument(
        "--description", required=True, help="Issue description"
    )
    create_parser.add_argument(
        "--type", default="Task", help="Issue type (default: Task)"
    )

    get_parser = subparsers.add_parser("get", help="Get issue details")
    get_parser.add_argument(
        "--issue-key", required=True, help="Issue key (e.g., PROJ-123)"
    )

    update_parser = subparsers.add_parser("update", help="Update an issue")
    update_parser.add_argument("--issue-key", required=True, help="Issue key")
    update_parser.add_argument("--summary", help="New summary")
    update_parser.add_argument("--description", help="New description")

    comment_parser = subparsers.add_parser("comment", help="Add a comment")
    comment_parser.add_argument("--issue-key", required=True, help="Issue key")
    comment_parser.add_argument("--comment", required=True, help="Comment text")

    search_parser = subparsers.add_parser("search", help="Search issues")
    search_parser.add_argument("--jql", required=True, help="JQL query")
    search_parser.add_argument(
        "--max-results", type=int, default=50, help="Max results"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = JiraClient()

    if args.command == "create":
        result = client.create_issue(
            args.project, args.summary, args.description, args.type
        )
    elif args.command == "get":
        result = client.get_issue(args.issue_key)
    elif args.command == "update":
        fields = {}
        if args.summary:
            fields["summary"] = args.summary
        if args.description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": args.description}],
                    }
                ],
            }
        result = client.update_issue(args.issue_key, fields)
    elif args.command == "comment":
        result = client.add_comment(args.issue_key, args.comment)
    elif args.command == "search":
        result = client.search_issues(args.jql, args.max_results)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
