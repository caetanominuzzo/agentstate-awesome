#!/usr/bin/env python3
"""Docker Hub CLI for listing repositories, tags, and searching images."""
import argparse
import json
import os
import sys
import requests


class DockerHubClient:
    """Client for Docker Hub API interactions."""

    def __init__(self):
        self.username = os.environ.get("DOCKERHUB_USERNAME", "")
        if not self.username:
            print(
                '{"error": "DOCKERHUB_USERNAME environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.token_env = os.environ.get("DOCKERHUB_TOKEN", "")
        if not self.token_env:
            print(
                '{"error": "DOCKERHUB_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://hub.docker.com/v2"
        self.jwt_token = self._login()
        self.headers = {
            "Authorization": f"JWT {self.jwt_token}",
            "Content-Type": "application/json",
        }

    def _login(self):
        """Authenticate and get JWT token."""
        try:
            response = requests.post(
                f"{self.base_url}/users/login/",
                json={
                    "username": self.username,
                    "password": self.token_env,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("token", "")
        except requests.exceptions.RequestException as e:
            print(
                json.dumps({
                    "error": f"Docker Hub login failed: {str(e)}",
                    "status_code": getattr(e.response, "status_code", None),
                }),
                file=sys.stderr,
            )
            sys.exit(1)

    def list_repos(self, namespace=None):
        """List repositories for a namespace."""
        ns = namespace or self.username
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{ns}/",
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

    def list_tags(self, repo):
        """List tags for a repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{repo}/tags/",
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

    def get_repo(self, repo):
        """Get repository details."""
        try:
            response = requests.get(
                f"{self.base_url}/repositories/{repo}/",
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

    def search(self, query):
        """Search Docker Hub for images."""
        try:
            response = requests.get(
                f"{self.base_url}/search/repositories/",
                headers=self.headers,
                params={"query": query},
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
    parser = argparse.ArgumentParser(description="Docker Hub CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    repos_parser = subparsers.add_parser("list-repos", help="List repositories")
    repos_parser.add_argument(
        "--namespace", help="Namespace (defaults to your username)"
    )

    tags_parser = subparsers.add_parser("list-tags", help="List tags for a repository")
    tags_parser.add_argument(
        "--repo", required=True, help="Repository (e.g., library/nginx)"
    )

    get_parser = subparsers.add_parser("get-repo", help="Get repository details")
    get_parser.add_argument(
        "--repo", required=True, help="Repository (e.g., library/nginx)"
    )

    search_parser = subparsers.add_parser("search", help="Search for images")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DockerHubClient()

    if args.command == "list-repos":
        result = client.list_repos(
            namespace=getattr(args, "namespace", None),
        )
    elif args.command == "list-tags":
        result = client.list_tags(args.repo)
    elif args.command == "get-repo":
        result = client.get_repo(args.repo)
    elif args.command == "search":
        result = client.search(args.query)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
