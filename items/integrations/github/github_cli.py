#!/usr/bin/env python3
"""GitHub CLI for managing repositories, issues, and pull requests."""
import argparse
import json
import os
import sys
import requests


class GitHubClient:
    """Client for GitHub REST API interactions."""

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

    def list_repos(self, org=None, user=None):
        """List repositories for an org or user."""
        if org:
            url = f"{self.base_url}/orgs/{org}/repos"
        elif user:
            url = f"{self.base_url}/users/{user}/repos"
        else:
            url = f"{self.base_url}/user/repos"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": 100, "sort": "updated"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_repo(self, repo):
        """Get details of a repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{repo}",
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

    def create_issue(self, repo, title, body):
        """Create a new issue in a repository."""
        try:
            response = requests.post(
                f"{self.base_url}/repos/{repo}/issues",
                headers=self.headers,
                json={"title": title, "body": body},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_prs(self, repo, state="open"):
        """List pull requests for a repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{repo}/pulls",
                headers=self.headers,
                params={"state": state, "per_page": 100},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_pr(self, repo, title, body, head, base):
        """Create a new pull request."""
        try:
            response = requests.post(
                f"{self.base_url}/repos/{repo}/pulls",
                headers=self.headers,
                json={
                    "title": title,
                    "body": body,
                    "head": head,
                    "base": base,
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

    def get_pr(self, repo, number):
        """Get details of a pull request."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{repo}/pulls/{number}",
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
    parser = argparse.ArgumentParser(description="GitHub CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    repos_parser = subparsers.add_parser("list-repos", help="List repositories")
    repos_parser.add_argument("--org", help="Organization name")
    repos_parser.add_argument("--user", help="Username")

    get_repo_parser = subparsers.add_parser("get-repo", help="Get repository details")
    get_repo_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )

    issue_parser = subparsers.add_parser("create-issue", help="Create an issue")
    issue_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    issue_parser.add_argument("--title", required=True, help="Issue title")
    issue_parser.add_argument("--body", required=True, help="Issue body")

    prs_parser = subparsers.add_parser("list-prs", help="List pull requests")
    prs_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    prs_parser.add_argument(
        "--state", default="open", choices=["open", "closed", "all"],
        help="PR state filter (default: open)",
    )

    create_pr_parser = subparsers.add_parser("create-pr", help="Create a pull request")
    create_pr_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    create_pr_parser.add_argument("--title", required=True, help="PR title")
    create_pr_parser.add_argument("--body", required=True, help="PR body")
    create_pr_parser.add_argument(
        "--head", required=True, help="Head branch (source)"
    )
    create_pr_parser.add_argument(
        "--base", required=True, help="Base branch (target)"
    )

    get_pr_parser = subparsers.add_parser("get-pr", help="Get pull request details")
    get_pr_parser.add_argument(
        "--repo", required=True, help="Repository (owner/repo)"
    )
    get_pr_parser.add_argument(
        "--number", required=True, type=int, help="PR number"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GitHubClient()

    if args.command == "list-repos":
        result = client.list_repos(org=args.org, user=args.user)
    elif args.command == "get-repo":
        result = client.get_repo(args.repo)
    elif args.command == "create-issue":
        result = client.create_issue(args.repo, args.title, args.body)
    elif args.command == "list-prs":
        result = client.list_prs(args.repo, args.state)
    elif args.command == "create-pr":
        result = client.create_pr(
            args.repo, args.title, args.body, args.head, args.base
        )
    elif args.command == "get-pr":
        result = client.get_pr(args.repo, args.number)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
