#!/usr/bin/env python3
"""Algolia CLI for searching indices, listing indices, and managing objects."""
import argparse
import json
import os
import sys
import requests


class AlgoliaClient:
    """Client for Algolia API interactions."""

    def __init__(self):
        self.app_id = os.environ.get("ALGOLIA_APP_ID", "")
        if not self.app_id:
            print(
                '{"error": "ALGOLIA_APP_ID environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.api_key = os.environ.get("ALGOLIA_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "ALGOLIA_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"https://{self.app_id}-dsn.algolia.net/1/indexes"
        self.headers = {
            "X-Algolia-API-Key": self.api_key,
            "X-Algolia-Application-Id": self.app_id,
            "Content-Type": "application/json",
        }

    def search(self, index, query):
        """Search an index."""
        try:
            response = requests.post(
                f"{self.base_url}/{index}/query",
                headers=self.headers,
                json={"query": query},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_indices(self):
        """List all indices."""
        try:
            response = requests.get(
                self.base_url,
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

    def get_object(self, index, object_id):
        """Get an object by ID from an index."""
        try:
            response = requests.get(
                f"{self.base_url}/{index}/{object_id}",
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

    def add_object(self, index, body):
        """Add an object to an index."""
        try:
            response = requests.post(
                f"{self.base_url}/{index}",
                headers=self.headers,
                json=body,
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
    parser = argparse.ArgumentParser(description="Algolia CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    search_parser = subparsers.add_parser("search", help="Search an index")
    search_parser.add_argument("--index", required=True, help="Index name")
    search_parser.add_argument("--query", required=True, help="Search query")

    subparsers.add_parser("list-indices", help="List all indices")

    get_parser = subparsers.add_parser("get-object", help="Get an object by ID")
    get_parser.add_argument("--index", required=True, help="Index name")
    get_parser.add_argument("--object-id", required=True, help="Object ID")

    add_parser = subparsers.add_parser("add-object", help="Add an object to an index")
    add_parser.add_argument("--index", required=True, help="Index name")
    add_parser.add_argument(
        "--body-json", required=True, help="JSON object to add"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AlgoliaClient()

    if args.command == "search":
        result = client.search(args.index, args.query)
    elif args.command == "list-indices":
        result = client.list_indices()
    elif args.command == "get-object":
        result = client.get_object(args.index, args.object_id)
    elif args.command == "add-object":
        body = json.loads(args.body_json)
        result = client.add_object(args.index, body)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
