#!/usr/bin/env python3
"""npm Registry CLI for searching packages, listing versions, and getting download stats."""
import argparse
import json
import os
import sys
import requests


class NpmRegistryClient:
    """Client for npm Registry API interactions."""

    def __init__(self):
        self.base_url = "https://registry.npmjs.org"
        self.headers = {
            "Accept": "application/json",
        }
        npm_token = os.environ.get("NPM_TOKEN", "")
        if npm_token:
            self.headers["Authorization"] = f"Bearer {npm_token}"

    def search(self, query):
        """Search for packages."""
        try:
            response = requests.get(
                f"{self.base_url}/-/v1/search",
                headers=self.headers,
                params={"text": query},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_package(self, name):
        """Get package metadata."""
        try:
            response = requests.get(
                f"{self.base_url}/{name}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "name": data.get("name"),
                "description": data.get("description"),
                "dist-tags": data.get("dist-tags"),
                "license": data.get("license"),
                "homepage": data.get("homepage"),
                "repository": data.get("repository"),
                "maintainers": data.get("maintainers"),
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_versions(self, name):
        """List all versions of a package."""
        try:
            response = requests.get(
                f"{self.base_url}/{name}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            versions = list(data.get("versions", {}).keys())
            return {
                "name": name,
                "versions": versions,
                "total": len(versions),
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_downloads(self, name, period="last-week"):
        """Get download counts for a package."""
        try:
            response = requests.get(
                f"https://api.npmjs.org/downloads/point/{period}/{name}",
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
    parser = argparse.ArgumentParser(description="npm Registry CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    search_parser = subparsers.add_parser("search", help="Search for packages")
    search_parser.add_argument("--query", required=True, help="Search query")

    get_parser = subparsers.add_parser("get-package", help="Get package metadata")
    get_parser.add_argument("--name", required=True, help="Package name")

    versions_parser = subparsers.add_parser(
        "list-versions", help="List package versions"
    )
    versions_parser.add_argument("--name", required=True, help="Package name")

    downloads_parser = subparsers.add_parser(
        "get-downloads", help="Get download counts"
    )
    downloads_parser.add_argument("--name", required=True, help="Package name")
    downloads_parser.add_argument(
        "--period",
        default="last-week",
        help="Period (last-day, last-week, last-month)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NpmRegistryClient()

    if args.command == "search":
        result = client.search(args.query)
    elif args.command == "get-package":
        result = client.get_package(args.name)
    elif args.command == "list-versions":
        result = client.list_versions(args.name)
    elif args.command == "get-downloads":
        result = client.get_downloads(args.name, args.period)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
