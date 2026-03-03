#!/usr/bin/env python3
"""Bitbucket CLI for managing repositories and pull requests."""
import argparse
import json
import os
import sys
import requests


class BitbucketClient:
    """Client for Bitbucket API interactions."""

    def __init__(self):
        self.username = os.environ.get("BITBUCKET_USERNAME", "")
        self.app_password = os.environ.get("BITBUCKET_APP_PASSWORD", "")
        if not self.username or not self.app_password:
            print(
                '{"error": "BITBUCKET_USERNAME and BITBUCKET_APP_PASSWORD environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.default_workspace = os.environ.get("BITBUCKET_WORKSPACE", "")
        self.base_url = "https://api.bitbucket.org/2.0"
        self.auth = (self.username, self.app_password)

    def list_repos(self, workspace):
        """List repositories in a workspace."""
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{workspace}",
                auth=self.auth,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_repo(self, workspace, repo_slug):
        """Get details of a specific repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{workspace}/{repo_slug}",
                auth=self.auth,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_prs(self, workspace, repo_slug, state="OPEN"):
        """List pull requests for a repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{workspace}/{repo_slug}/pullrequests",
                auth=self.auth,
                params={"state": state},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_pr(self, workspace, repo_slug, title, source_branch, dest_branch="main"):
        """Create a pull request."""
        payload = {
            "title": title,
            "source": {"branch": {"name": source_branch}},
            "destination": {"branch": {"name": dest_branch}},
        }

        try:
            response = requests.post(
                f"{self.base_url}/repositories/{workspace}/{repo_slug}/pullrequests",
                auth=self.auth,
                json=payload,
                headers={"Content-Type": "application/json"},
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
    parser = argparse.ArgumentParser(description="Bitbucket CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    repos_parser = subparsers.add_parser("list-repos", help="List repositories")
    repos_parser.add_argument("--workspace", required=True, help="Workspace slug")

    get_parser = subparsers.add_parser("get-repo", help="Get repository details")
    get_parser.add_argument("--workspace", required=True, help="Workspace slug")
    get_parser.add_argument("--repo-slug", required=True, help="Repository slug")

    prs_parser = subparsers.add_parser("list-prs", help="List pull requests")
    prs_parser.add_argument("--workspace", required=True, help="Workspace slug")
    prs_parser.add_argument("--repo-slug", required=True, help="Repository slug")
    prs_parser.add_argument(
        "--state", default="OPEN", help="PR state: OPEN, MERGED, DECLINED, SUPERSEDED"
    )

    create_parser = subparsers.add_parser("create-pr", help="Create a pull request")
    create_parser.add_argument("--workspace", required=True, help="Workspace slug")
    create_parser.add_argument("--repo-slug", required=True, help="Repository slug")
    create_parser.add_argument("--title", required=True, help="PR title")
    create_parser.add_argument(
        "--source-branch", required=True, help="Source branch name"
    )
    create_parser.add_argument(
        "--dest-branch", default="main", help="Destination branch (default: main)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = BitbucketClient()

    if args.command == "list-repos":
        result = client.list_repos(args.workspace)
    elif args.command == "get-repo":
        result = client.get_repo(args.workspace, args.repo_slug)
    elif args.command == "list-prs":
        result = client.list_prs(args.workspace, args.repo_slug, args.state)
    elif args.command == "create-pr":
        result = client.create_pr(
            args.workspace, args.repo_slug, args.title,
            args.source_branch, args.dest_branch,
        )

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
