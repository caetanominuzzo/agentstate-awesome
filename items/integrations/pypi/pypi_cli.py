#!/usr/bin/env python3
"""PyPI CLI for searching packages, listing versions, and getting release data."""
import argparse
import json
import sys
import requests


class PyPIClient:
    """Client for PyPI API interactions."""

    def __init__(self):
        self.base_url = "https://pypi.org"
        self.headers = {
            "Accept": "application/json",
        }

    def get_package(self, name):
        """Get package metadata."""
        try:
            response = requests.get(
                f"{self.base_url}/pypi/{name}/json",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            info = data.get("info", {})
            return {
                "name": info.get("name"),
                "version": info.get("version"),
                "summary": info.get("summary"),
                "description": info.get("description"),
                "author": info.get("author"),
                "author_email": info.get("author_email"),
                "license": info.get("license"),
                "home_page": info.get("home_page"),
                "project_url": info.get("project_url"),
                "requires_python": info.get("requires_python"),
                "keywords": info.get("keywords"),
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def search(self, query):
        """Search for packages using the PyPI simple API and XMLRPC fallback."""
        try:
            response = requests.get(
                f"https://pypi.org/search/",
                headers={"Accept": "application/json"},
                params={"q": query},
                timeout=30,
            )
            # PyPI search page returns HTML, so we use a workaround
            # by searching via the warehouse API
            response = requests.get(
                f"https://pypi.org/pypi/{query}/json",
                headers=self.headers,
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                info = data.get("info", {})
                return {
                    "results": [
                        {
                            "name": info.get("name"),
                            "version": info.get("version"),
                            "summary": info.get("summary"),
                        }
                    ]
                }
            # If exact match not found, return helpful message
            return {
                "results": [],
                "note": f"No exact match for '{query}'. Try get-package with the exact name.",
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
                f"{self.base_url}/pypi/{name}/json",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            versions = list(data.get("releases", {}).keys())
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

    def get_release(self, name, version):
        """Get release data for a specific version."""
        try:
            response = requests.get(
                f"{self.base_url}/pypi/{name}/{version}/json",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            info = data.get("info", {})
            urls = data.get("urls", [])
            return {
                "name": info.get("name"),
                "version": info.get("version"),
                "summary": info.get("summary"),
                "requires_python": info.get("requires_python"),
                "requires_dist": info.get("requires_dist"),
                "files": [
                    {
                        "filename": u.get("filename"),
                        "packagetype": u.get("packagetype"),
                        "size": u.get("size"),
                        "upload_time": u.get("upload_time"),
                    }
                    for u in urls
                ],
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="PyPI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    get_parser = subparsers.add_parser("get-package", help="Get package metadata")
    get_parser.add_argument("--name", required=True, help="Package name")

    search_parser = subparsers.add_parser("search", help="Search for packages")
    search_parser.add_argument("--query", required=True, help="Search query")

    versions_parser = subparsers.add_parser(
        "list-versions", help="List package versions"
    )
    versions_parser.add_argument("--name", required=True, help="Package name")

    release_parser = subparsers.add_parser(
        "get-release", help="Get release data for a specific version"
    )
    release_parser.add_argument("--name", required=True, help="Package name")
    release_parser.add_argument("--version", required=True, help="Version string")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = PyPIClient()

    if args.command == "get-package":
        result = client.get_package(args.name)
    elif args.command == "search":
        result = client.search(args.query)
    elif args.command == "list-versions":
        result = client.list_versions(args.name)
    elif args.command == "get-release":
        result = client.get_release(args.name, args.version)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
