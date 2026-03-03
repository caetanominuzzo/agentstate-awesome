#!/usr/bin/env python3
"""Confluence CLI for searching, creating, and updating pages and spaces."""
import argparse
import base64
import json
import os
import sys
import requests


class ConfluenceClient:
    """Client for Confluence API interactions."""

    def __init__(self):
        self.base_url = os.environ.get("CONFLUENCE_BASE_URL", "").rstrip("/")
        self.email = os.environ.get("CONFLUENCE_EMAIL", "")
        self.api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")
        if not self.base_url or not self.email or not self.api_token:
            print(
                '{"error": "CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"{self.base_url}/wiki/rest/api"
        auth_str = f"{self.email}:{self.api_token}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def search(self, cql):
        """Search Confluence using CQL."""
        try:
            response = requests.get(
                f"{self.base_url}/content/search",
                headers=self.headers,
                params={"cql": cql},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_page(self, page_id):
        """Get a specific page by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/content/{page_id}",
                headers=self.headers,
                params={"expand": "body.storage,version"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_page(self, space_key, title, body):
        """Create a new page in a space."""
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage",
                }
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}/content",
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

    def update_page(self, page_id, title, body, version):
        """Update an existing page."""
        payload = {
            "type": "page",
            "title": title,
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage",
                }
            },
            "version": {"number": int(version)},
        }

        try:
            response = requests.put(
                f"{self.base_url}/content/{page_id}",
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

    def list_spaces(self):
        """List all accessible spaces."""
        try:
            response = requests.get(
                f"{self.base_url}/space",
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
    parser = argparse.ArgumentParser(description="Confluence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    search_parser = subparsers.add_parser("search", help="Search with CQL")
    search_parser.add_argument("--cql", required=True, help="CQL query string")

    get_parser = subparsers.add_parser("get-page", help="Get page by ID")
    get_parser.add_argument("--page-id", required=True, help="Page ID")

    create_parser = subparsers.add_parser("create-page", help="Create a page")
    create_parser.add_argument("--space-key", required=True, help="Space key")
    create_parser.add_argument("--title", required=True, help="Page title")
    create_parser.add_argument(
        "--body", required=True, help="Page body (Confluence storage format)"
    )

    update_parser = subparsers.add_parser("update-page", help="Update a page")
    update_parser.add_argument("--page-id", required=True, help="Page ID")
    update_parser.add_argument("--title", required=True, help="Page title")
    update_parser.add_argument(
        "--body", required=True, help="Page body (Confluence storage format)"
    )
    update_parser.add_argument(
        "--version", required=True, help="New version number (increment current by 1)"
    )

    subparsers.add_parser("list-spaces", help="List spaces")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ConfluenceClient()

    if args.command == "search":
        result = client.search(args.cql)
    elif args.command == "get-page":
        result = client.get_page(args.page_id)
    elif args.command == "create-page":
        result = client.create_page(args.space_key, args.title, args.body)
    elif args.command == "update-page":
        result = client.update_page(args.page_id, args.title, args.body, args.version)
    elif args.command == "list-spaces":
        result = client.list_spaces()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
